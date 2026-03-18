from typing import TypedDict, List, Optional


class FraudState(TypedDict):
    txn_id: str

    risk_score: int
    risk_level: str
    reasons: list[str]

    summary: str
    key_risks: list[str]
    explanation: str
    recommended_actions: list[str]