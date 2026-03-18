import uuid

from sqlalchemy import Column, String, Numeric, ForeignKey, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .connection import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    home_country = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )


class Transaction(Base):
    __tablename__ = "transactions"

    txn_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    merchant = Column(String, nullable=False)

    merchant_category = Column(String, nullable=False)

    country = Column(String, nullable=False)

    city = Column(String)

    payment_method = Column(String)

    device_type = Column(String)

    timestamp = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        Index("idx_transaction_user", "user_id"),
        Index("idx_transaction_timestamp", "timestamp"),
    )


class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    txn_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.txn_id"),
        nullable=False
    )

    risk_score = Column(String, nullable=False)

    decision = Column(String)

    explanation = Column(String)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )