from fastapi import FastAPI
from app.api.routes import router as ledger_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Expense Fraud Detector", 
    version="1.0"
)

app.include_router(ledger_router, prefix="/ledger", tags=["Ledger"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Fraud Detector backend is running"}
