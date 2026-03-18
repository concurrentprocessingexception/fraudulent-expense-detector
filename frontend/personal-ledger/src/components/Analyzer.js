import React, { useState } from "react";
import { analyzeTransaction } from "../api/fraudApi";

const Analyzer = () => {
  const [txnId, setTxnId] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!txnId) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeTransaction(txnId);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Error analyzing transaction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Fraud Detector</h2>

      <input
        type="text"
        placeholder="Enter Transaction ID"
        value={txnId}
        onChange={(e) => setTxnId(e.target.value)}
        style={{ width: "400px", marginRight: "10px" }}
      />

      <button onClick={handleAnalyze}>
        Analyze
      </button>

      {loading && <p>Analyzing...</p>}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Result</h3>

          <p><b>Risk Score:</b> {result.risk_score}</p>
          <p><b>Risk Level:</b> {result.risk_level}</p>

          <p><b>Reasons:</b></p>
          <ul>
            {result.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>

          <p><b>Explanation:</b></p>
          <p>{result.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default Analyzer;