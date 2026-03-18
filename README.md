# Fraudulent Expense Detector

This repository contains a modular AI-powered expense fraud detector with frontend and backend components.

## Project Layout

- `fraudulent-expense-detector/`
  - `backend/` - FastAPI backend, agents, tools for fraud scoring and rules.
  - `frontend/personal-ledger/` - React app for ledger management (tabs UI with `Sidebar.js`).

## How to Use

### 1) Backend (FastAPI)

```bash
cd fraudulent-expense-detector/backend
pip install -r requirements.txt  # if you create one
uvicorn main:app --reload
```

### 2) React Frontend (Personal Ledger)

```bash
cd frontend/personal-ledger
npm install
npm start
```

## Notes

- If a folder has its own README, please check it for local run instructions.
- Root-level README is the main entry point; each app folder contains more details.