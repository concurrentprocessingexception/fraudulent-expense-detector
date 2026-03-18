from langchain.tools import tool
from app.tools.fraud_tools import analyze_transaction_tool


@tool
def analyze_transaction(txn_id: str):
    """
    Analyze a transaction for fraud risk.
    Input: transaction ID
    Output: risk score, level, and reasons
    """
    return analyze_transaction_tool(txn_id)