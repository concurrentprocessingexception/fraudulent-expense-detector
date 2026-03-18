from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.repositories import get_transaction_by_id
from app.tools.risk_engine import FraudRiskEngine


def analyze_transaction_tool(txn_id: str):

    db: Session = SessionLocal()

    try:
        txn = get_transaction_by_id(db, txn_id)

        if not txn:
            return {"error": "Transaction not found"}

        engine = FraudRiskEngine(db)
        result = engine.analyze_transaction(txn)

        return {
            "txn_id": txn_id,
            **result
        }

    finally:
        db.close()