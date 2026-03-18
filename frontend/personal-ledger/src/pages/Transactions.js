import React, { useEffect, useState } from "react";
import { getTransactions } from "../api/fraudApi";
import { useNavigate } from "react-router-dom";

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    const data = await getTransactions();
    setTransactions(data);
  };

  const handleRowClick = (txnId) => {
    navigate(`/analyze?txn_id=${txnId}`);
  };

  return (
    <div>
      <h2>Transactions</h2>

      <table style={styles.table}>
        <thead>
          <tr>
            <th>Amount</th>
            <th>Merchant</th>
            <th>Category</th>
            <th>Country</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t) => (
            <tr
              key={t.txn_id}
              onClick={() => handleRowClick(t.txn_id)}
              style={styles.row}
              onMouseEnter={(e) => e.currentTarget.style.background = "#f1f5f9"}
              onMouseLeave={(e) => e.currentTarget.style.background = "white"}
            >
              <td>€{t.amount}</td>
              <td>{t.merchant}</td>
              <td>{t.category}</td>
              <td>{t.country}</td>
              <td>{new Date(t.timestamp).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  table: {
    width: "100%",
    background: "white",
    borderRadius: "8px",
    overflow: "hidden",
  },
  row: {
    cursor: "pointer",
    transition: "0.2s"
  },
};

export default Transactions;