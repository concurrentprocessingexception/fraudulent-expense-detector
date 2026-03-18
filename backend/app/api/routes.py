from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    AnalyzeTransactionRequest,
    AnalyzeTransactionResponse
)
from app.agents.fraud_graph import build_graph
from app.database.connection import SessionLocal
from app.database.models import Transaction

router = APIRouter()

# Build graph once, better for performance
graph = build_graph()


@router.post("/analyze_transaction", response_model=AnalyzeTransactionResponse)
def analyze_transaction(request: AnalyzeTransactionRequest):

    try:
        result = graph.invoke({
            "txn_id": request.txn_id
        })

        return AnalyzeTransactionResponse(
            txn_id=result["txn_id"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            summary=result["summary"],
            key_risks=result["key_risks"],
            explanation=result["explanation"],
            recommended_actions=result["recommended_actions"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/transactions")
def get_transactions():

    db = SessionLocal()

    try:
        txns = (
            db.query(Transaction)
            .order_by(Transaction.timestamp.desc())
            .limit(50)
            .all()
        )

        return [
            {
                "txn_id": str(t.txn_id),
                "amount": float(t.amount),
                "merchant": t.merchant,
                "category": t.merchant_category,
                "country": t.country,
                "timestamp": t.timestamp
            }
            for t in txns
        ]

    finally:
        db.close()