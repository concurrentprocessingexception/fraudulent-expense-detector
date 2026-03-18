import axios from "axios";

const API_BASE = "http://localhost:8000/ledger";

export const analyzeTransaction = async (txnId) => {
  const response = await axios.post(`${API_BASE}/analyze_transaction`, {
    txn_id: txnId,
  });

  return response.data;
};

export const getTransactions = async () => {
  const res = await axios.get(`${API_BASE}/transactions`);
  return res.data;
};