from typing import Dict, Any

import uuid
import json
import re

from langchain_aws import ChatBedrock
from sqlalchemy.orm import Session

from app.tools.fraud_tools import analyze_transaction_tool
from app.database.connection import SessionLocal
from app.database.models import FraudAlert
from app.database.repositories import save_fraud_alert


# -------------------------------
# LLM CONFIG (AWS Bedrock)
# -------------------------------

# AWS credentials needs to be configured in the environment:
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - AWS_DEFAULT_REGION

llm = ChatBedrock(
    model_id="eu.amazon.nova-2-lite-v1:0",
    model_kwargs={
        "temperature": 0.2,
        "max_tokens": 500
    }
)


# -------------------------------
# NODE 1: ANALYZE TRANSACTION
# -------------------------------

def analyze_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calls the fraud risk engine via tool layer.
    """

    txn_id = state["txn_id"]

    result = analyze_transaction_tool(txn_id)

    if "error" in result:
        return {
            "risk_score": 0,
            "risk_level": "ERROR",
            "reasons": [result["error"]]
        }

    return {
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "reasons": result["reasons"]
    }


# -------------------------------
# NODE 2: EXPLANATION (LLM)
# -------------------------------

def explanation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses LLM to generate human-readable fraud explanation.
    """

    prompt = f"""
    You are a fraud analyst.

    Return ONLY valid JSON. No markdown, no explanation outside JSON.

    Schema:
    {{
    "summary": string,
    "key_risks": string[],
    "explanation": string,
    "recommended_actions": string[]
    }}

    Data:
    Risk Level: {state['risk_level']}
    Risk Score: {state['risk_score']}
    Reasons: {state['reasons']}
    """

    response = llm.invoke(prompt)
    
    raw = response.content.strip()
    
    cleaned = extract_json(raw)
    
    try:
        parsed = json.loads(cleaned)
        
    except Exception as e:
        parsed = {
            "summary": "Unable to parse structured response",
            "key_risks": state.get("reasons", []),
            "explanation": raw,
            "recommended_actions": []
        }

    return {
        "summary": parsed.get("summary"),
        "key_risks": parsed.get("key_risks"),
        "explanation": parsed.get("explanation"),
        "recommended_actions": parsed.get("recommended_actions"),
    }


# -------------------------------
# NODE 3: PERSIST FRAUD ALERT
# -------------------------------
def persist_node(state):

    db = SessionLocal()

    try:
        save_fraud_alert(
            db=db,
            txn_id=state["txn_id"],
            risk_score=state["risk_score"],
            decision=state["risk_level"],
            explanation=state.get("explanation", "")
        )

    finally:
        db.close()

    return state

def extract_json(raw: str):

    # Remove markdown code block if present
    raw = raw.strip()

    # Case 1: ```json ... ```
    if raw.startswith("```"):
        raw = re.sub(r"^```json", "", raw)
        raw = re.sub(r"^```", "", raw)
        raw = re.sub(r"```$", "", raw)

    # Remove any leftover backticks
    raw = raw.strip("` \n")

    return raw