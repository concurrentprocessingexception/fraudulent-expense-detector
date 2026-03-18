from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import uuid

from app.database.models import Transaction, User, FraudAlert


# -------------------------------
# TRANSACTION QUERIES
# -------------------------------

def get_transaction_by_id(db: Session, txn_id: str):
    return db.query(Transaction).filter(
        Transaction.txn_id == txn_id
    ).first()


def get_user_by_id(db: Session, user_id):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


def get_user_avg_amount(db: Session, user_id):
    return (
        db.query(func.avg(Transaction.amount))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )


def get_user_category_stats(db: Session, user_id):
    return (
        db.query(Transaction.merchant_category, func.count())
        .filter(Transaction.user_id == user_id)
        .group_by(Transaction.merchant_category)
        .all()
    )


def get_recent_transactions_count(db: Session, user_id, minutes=60):
    cutoff = datetime.now() - timedelta(minutes=minutes)

    return (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id,
            Transaction.timestamp >= cutoff
        )
        .count()
    )


# -------------------------------
# FRAUD ALERT
# -------------------------------

def save_fraud_alert(
    db: Session,
    txn_id: str,
    risk_score: int,
    decision: str,
    explanation: str
):
    alert = FraudAlert(
        alert_id=uuid.uuid4(),
        txn_id=txn_id,
        risk_score=str(risk_score),
        decision=decision,
        explanation=explanation
    )

    db.add(alert)
    db.commit()

    return alert