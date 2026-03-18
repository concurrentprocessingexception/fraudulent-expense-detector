from app.database.connection import SessionLocal
from app.database.models import Transaction
from app.tools.risk_engine import FraudRiskEngine

db = SessionLocal()

txn = db.query(Transaction).first()

engine = FraudRiskEngine(db)

result = engine.analyze_transaction(txn)

print(result)