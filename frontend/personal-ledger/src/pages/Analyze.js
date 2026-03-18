import React, { useEffect, useState } from "react";
import { analyzeTransaction } from "../api/fraudApi";
import { useSearchParams } from "react-router-dom";

const Analyze = () => {
    const [searchParams] = useSearchParams();
    const [txnId, setTxnId] = useState("");
    const [result, setResult] = useState(null);

    useEffect(() => {
        const id = searchParams.get("txn_id");
        if (id) {
            setTxnId(id);
            handleAnalyze(id);
        }
    }, []);

    const handleAnalyze = async (idParam) => {
        const id = idParam || txnId;
        if (!id) return;

        const res = await analyzeTransaction(id);
        setResult(res);
    };

    const cleanText = (text) => {
        return text
            .replace(/[#*]/g, "")   // remove markdown
            .replace(/\n/g, " ")
            .trim();
    };

    const formatReason = (r) => {
        return r.replace(/\d+\.\s*/, "");
    };

    return (
        <div>
            <h2>Analyze Transaction</h2>

            <div style={styles.card}>
                <input
                    value={txnId}
                    onChange={(e) => setTxnId(e.target.value)}
                    placeholder="Enter txn id"
                />
                <button onClick={() => handleAnalyze()}>Analyze</button>
            </div>

            {result && (
                <div style={styles.result}>

                    {/* HEADER */}
                    <div style={styles.header}>
                        <span style={{
                            ...styles.badge,
                            background: getColor(result.risk_level)
                        }}>
                            {result.risk_level}
                        </span>

                        <span style={styles.score}>
                            Score: {result.risk_score}
                        </span>
                    </div>

                    {/* SUMMARY */}
                    <div style={styles.section}>
                        <h4>🧾 Summary</h4>
                        <p>{result.summary}</p>
                    </div>

                    {/* RISKS */}
                    <div style={styles.section}>
                        <h4>🚨 Key Risks</h4>
                        <ul>
                            {result.key_risks.map((r, i) => (
                                <li key={i}>{r}</li>
                            ))}
                        </ul>
                    </div>

                    {/* EXPLANATION */}
                    <div style={styles.section}>
                        <h4>📊 Explanation</h4>
                        <p>{result.explanation}</p>
                    </div>

                    {/* ACTIONS */}
                    <div style={styles.section}>
                        <h4>🧭 Recommended Actions</h4>
                        <ul>
                            {result.recommended_actions.map((a, i) => (
                                <li key={i}>{a}</li>
                            ))}
                        </ul>
                    </div>

                </div>
            )}
        </div>
    );
};

const getColor = (level) => {
    if (level === "HIGH") return "#ef4444";     // red
    if (level === "MEDIUM") return "#f59e0b";   // orange
    return "#22c55e";                           // green
};

const styles = {
    result: {
        marginTop: "20px",
        background: "white",
        padding: "24px",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
    },

    header: {
        display: "flex",
        alignItems: "center",
        gap: "12px",
        marginBottom: "16px"
    },

    badge: {
        color: "white",
        padding: "6px 12px",
        borderRadius: "6px",
        fontWeight: "bold"
    },

    score: {
        fontSize: "14px",
        color: "#64748b"
    },

    section: {
        marginTop: "16px"
    }
};

export default Analyze;