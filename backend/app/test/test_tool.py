from app.tools.fraud_tools import analyze_transaction_tool

# replace with a real txn_id from DB
txn_id = "1f5f084e-dcfa-4b42-8aaa-2ac4f2397672"

result = analyze_transaction_tool(txn_id)

print(result)