from app.agents.fraud_graph import build_graph

graph = build_graph()

# replace with real txn_id from DB
result = graph.invoke({
    "txn_id": "1f5f084e-dcfa-4b42-8aaa-2ac4f2397672"
})

print(result)