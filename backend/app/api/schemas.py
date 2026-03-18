from pydantic import BaseModel

"""
Request Schema
"""
class AnalyzeTransactionRequest(BaseModel):
    txn_id: str


"""
Response Schema
"""
class AnalyzeTransactionResponse(BaseModel):
    txn_id: str
    risk_score: int
    risk_level: str

    summary: str
    key_risks: list[str]
    explanation: str
    recommended_actions: list[str]