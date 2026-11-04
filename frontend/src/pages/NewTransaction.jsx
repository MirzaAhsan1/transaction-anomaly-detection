import React, { useState } from "react";

import { useCreateTransactionMutation } from "../api/transactionApi";
import { useAccountValidation } from "../hooks/useAccountValidation";
import { getDeviceInfo } from "../utils/deviceInfo";

export default function NewTransactionPage() {
  const [formData, setFormData] = useState({
    amount: "",
    currency: "",
    transaction_type: "",
    payment_method: "",
    transaction_time: new Date().toISOString().slice(0, 16),
    sender_name: "",
    sender_account_number: "",
    sender_bank: "",
    receiver_name: "",
    receiver_account_number: "",
    receiver_bank: "",
    merchant_name: "",
    merchant_category: "",
  });

  const [createTransaction, { isLoading }] = useCreateTransactionMutation();
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState("");

  // ── Account Validation ──────────────────────────────────────────────────
  // Each hook call encapsulates: debounce + RTK Query + status normalisation.
  // status: 'idle' | 'loading' | 'found' | 'not_found' | 'error'
  const senderValidation = useAccountValidation(formData.sender_account_number);
  const receiverValidation = useAccountValidation(formData.receiver_account_number);

  // Submission is only allowed when both accounts are confirmed to exist.
  const canSubmit =
    senderValidation.status === "found" && receiverValidation.status === "found";
  // ───────────────────────────────────────────────────────────────────────

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "amount" ? Number(value) : value,
    }));
  };

  const handleReceiptUpload = async (file) => {
    setError("");

    const form = new FormData();
    form.append("image", file);

    try {
      const token = localStorage.getItem("accessToken");
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/receipt/parse`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: form,
      });

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || "Failed to parse receipt");
      }

      const data = await res.json();

      // Map receipt fields -> existing form fields
      setFormData((prev) => ({
        ...prev,
        amount: typeof data.amount === "number" ? data.amount : prev.amount,
        currency: data.currency ?? prev.currency,
        transaction_time: data.transaction_time
          ? new Date(data.transaction_time).toISOString().slice(0, 16)
          : prev.transaction_time,
        sender_name: data.sender_name ?? prev.sender_name,
        sender_account_number: data.sender_account_number ?? prev.sender_account_number,
        sender_bank: data.sender_bank ?? prev.sender_bank,
        receiver_name: data.receiver_name ?? prev.receiver_name,
        receiver_account_number: data.receiver_account_number ?? prev.receiver_account_number,
        receiver_bank: data.receiver_bank ?? prev.receiver_bank,
        merchant_name: data.merchant_name ?? prev.merchant_name,
        merchant_category: data.merchant_category ?? prev.merchant_category,
        payment_method: data.payment_method ? String(data.payment_method) : prev.payment_method,
        transaction_type: data.transaction_type ? String(data.transaction_type) : prev.transaction_type,
      }));
    } catch (e) {
      console.error("Receipt upload parse failed:", e);
      setError("Could not parse receipt. Please enter details manually.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setPredictionResult(null);

    // Frontend guard (UX) — backend enforces this too as source of truth.
    if (!canSubmit) {
      setError(
        "Please ensure both sender and receiver account numbers are valid before submitting."
      );
      return;
    }

    try {
      // Backend expects full ISO string with seconds
      const deviceInfo = getDeviceInfo();
      const payload = {
        ...formData,
        transaction_time: formData.transaction_time + ":00",
        ...deviceInfo,
      };

      const response = await createTransaction(payload).unwrap();
      setPredictionResult(response);
    } catch (err) {
      console.error("Failed to create transaction:", err);
      setError("An error occurred while analyzing the transaction.");
    }
  };

  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>New transaction</h2>
            <p className="subtle-text">Create a transaction record and submit it for fraud analysis</p>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="receipt-upload" style={{ gridColumn: "span 2", marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 8, color: "#111827" }}>Upload receipt</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleReceiptUpload(file);
              }}
            />
            <p className="subtle-text" style={{ marginTop: 8 }}>
              Receipt data will be extracted and used to auto-fill the form.
            </p>
          </div>

          <div className="form-grid">
            <h3
              style={{
                gridColumn: "span 2",
                marginTop: "1rem",
                borderBottom: "1px solid #e2e8f0",
                paddingBottom: "0.25rem",
                color: "#4f46e5",
              }}
            >
              Transaction Details
            </h3>

            <label className="field">
              <span>Amount</span>
              <input type="number" step="0.01" name="amount" value={formData.amount} onChange={handleChange} required placeholder="5200" />
            </label>

            <label className="field">
              <span>Currency</span>
              <select name="currency" value={formData.currency} onChange={handleChange}>
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="PKR">PKR</option>
                <option value="GBP">GBP</option>
                <option value="CAD">CAD</option>
                <option value="AUD">AUD</option>
              </select>
            </label>

            <label className="field">
              <span>Transaction Type</span>
              <select name="transaction_type" value={formData.transaction_type} onChange={handleChange}>
                <option value="Transfer">Transfer</option>
                <option value="Payment">Payment</option>
                <option value="Withdrawal">Withdrawal</option>
                <option value="Deposit">Deposit</option>
              </select>
            </label>

            <label className="field">
              <span>Payment Method</span>
              <select name="payment_method" value={formData.payment_method} onChange={handleChange}>
                <option value="Credit Card">Credit Card</option>
                <option value="Debit Card">Debit Card</option>
                <option value="Bank Transfer">Bank Transfer</option>
                <option value="Digital Wallet">Digital Wallet</option>
              </select>
            </label>

            <label className="field" style={{ gridColumn: "span 2" }}>
              <span>Transaction Time</span>
              <input type="datetime-local" name="transaction_time" value={formData.transaction_time} onChange={handleChange} required />
            </label>

            <h3
              style={{
                gridColumn: "span 2",
                marginTop: "1rem",
                borderBottom: "1px solid #e2e8f0",
                paddingBottom: "0.25rem",
                color: "#4f46e5",
              }}
            >
              Sender Information
            </h3>

            <label className="field">
              <span>Sender Name</span>
              <input type="text" name="sender_name" value={formData.sender_name} onChange={handleChange} required placeholder="John Doe" />
            </label>

            <label className="field">
              <span>Sender Account Number</span>
              <input type="text" name="sender_account_number" value={formData.sender_account_number} onChange={handleChange} required  placeholder="1000071" />
              {formData.sender_account_number && (
                <small
                  style={{
                    color:
                      senderValidation.status === "found"
                        ? "#16a34a"
                        : senderValidation.status === "not_found" || senderValidation.status === "error"
                          ? "#dc2626"
                          : "#6b7280",
                    display: "block",
                    marginTop: 6,
                    fontWeight: 500,
                  }}
                >
                  {/* {senderValidation.status === "loading" && "Checking..."} */}
                  {/* {senderValidation.status === "found" && "✔ Account Found"} */}
                  {senderValidation.status === "not_found" && "❌ Account Not Found"}
                  {senderValidation.status === "error" && "❌ Validation error"}
                </small>
              )}
            </label>

            <label className="field" style={{ gridColumn: "span 2" }}>
              <span>Sender Bank</span>
              <input type="text" name="sender_bank" value={formData.sender_bank} onChange={handleChange} required placeholder="Chase Bank" />
            </label>

            <h3
              style={{
                gridColumn: "span 2",
                marginTop: "1rem",
                borderBottom: "1px solid #e2e8f0",
                paddingBottom: "0.25rem",
                color: "#4f46e5",
              }}
            >
              Receiver Information
            </h3>

            <label className="field">
              <span>Receiver Name</span>
              <input type="text" name="receiver_name" value={formData.receiver_name} onChange={handleChange} required placeholder="Jane Smith" />
            </label>

            <label className="field">
              <span>Receiver Account Number</span>
              <input type="text" name="receiver_account_number" value={formData.receiver_account_number} onChange={handleChange} required placeholder="987654321" />
              {formData.receiver_account_number && (
                <small
                  style={{
                    color:
                      receiverValidation.status === "found"
                        ? "#16a34a"
                        : receiverValidation.status === "not_found" || receiverValidation.status === "error"
                          ? "#dc2626"
                          : "#6b7280",
                    display: "block",
                    marginTop: 6,
                    fontWeight: 500,
                  }}
                >
                  {/* {receiverValidation.status === "loading" && "Checking..."} */}
                  {/* {receiverValidation.status === "found" && "✔ Account Found"} */}
                  {receiverValidation.status === "not_found" && "❌ Account Not Found"}
                  {receiverValidation.status === "error" && "❌ Validation error"}
                </small>
              )}
            </label>

            <label className="field" style={{ gridColumn: "span 2" }}>
              <span>Receiver Bank</span>
              <input type="text" name="receiver_bank" value={formData.receiver_bank} onChange={handleChange} required placeholder="Bank of America" />
            </label>

            <h3
              style={{
                gridColumn: "span 2",
                marginTop: "1rem",
                borderBottom: "1px solid #e2e8f0",
                paddingBottom: "0.25rem",
                color: "#4f46e5",
              }}
            >
              Merchant Information
            </h3>

            <label className="field">
              <span>Merchant Name</span>
              <input type="text" name="merchant_name" value={formData.merchant_name} onChange={handleChange} required placeholder="Amazon Store" />
            </label>

            <label className="field">
              <span>Merchant Category</span>
              <input type="text" name="merchant_category" value={formData.merchant_category} onChange={handleChange} required placeholder="Retail" />
            </label>
          </div>

          {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

          {/* Inform user why submit is blocked when accounts are pending/invalid */}
          {!canSubmit && (senderValidation.status !== "idle" || receiverValidation.status !== "idle") && (
            <p style={{ color: "#b45309", marginTop: "0.5rem", fontSize: "0.875rem" }}>
              Both sender and receiver accounts must be verified before submitting.
            </p>
          )}

          <div className="topbar-actions" style={{ marginTop: 18 }}>
            <button
              type="submit"
              className="primary-button"
              disabled={!canSubmit || isLoading}
              title={!canSubmit ? "Verify both account numbers first" : undefined}
            >
              {isLoading ? "Analyzing..." : "Submit transaction"}
            </button>
            <button type="button" className="ghost-button" disabled={isLoading}>
              Save draft
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Workflow preview</h2>
            <p className="subtle-text">Outcome after model evaluation</p>
          </div>
          {predictionResult ? (
            <span className={`status-pill ${predictionResult.action === "Block" ? "danger" : "success"}`}>Analyzed</span>
          ) : (
            <span className="status-pill warning">Queued for review</span>
          )}
        </div>

        <div className="score-card">
          <div className="score-number">{predictionResult ? predictionResult.action : "Pending"}</div>
          <p className="subtle-text">
            {predictionResult
              ? `Decision state: Transaction ${predictionResult.action === "Block" ? "Blocked" : "Approved"}`
              : "Awaiting submission..."}
          </p>
        </div>

        <div className="metric-row" style={{ marginTop: 14 }}>
          <div>Save transaction in database</div>
          <div>{predictionResult ? (predictionResult.action === "Block" ? "Alert Sent" : "Receipt Sent") : "Send confirmation email"}</div>
          <div>Refresh dashboard automatically</div>
        </div>

        <div className="metric-row" style={{ marginTop: 12, paddingBottom: 12, borderBottom: "1px solid #eee" }}>
          <div>
            Transaction ID: <br />
            <strong>{predictionResult ? predictionResult.transaction_id : "--"}</strong>
          </div>
          <div>
            Amount: <br />
            <strong>{predictionResult ? `${predictionResult.currency} ${predictionResult.amount}` : "--"}</strong>
          </div>
          <div>
            Action: <br />
            <strong>{predictionResult ? predictionResult.action : "--"}</strong>
          </div>
        </div>

        <div className="metric-row" style={{ marginTop: 12 }}>
          <div>
            Prediction: <br />
            <strong>{predictionResult ? predictionResult.prediction : "--"}</strong>
          </div>
          <div>
            Risk Score: <br />
            <strong>{predictionResult ? predictionResult.risk_score : "--"}</strong>
          </div>
          <div>
            Confidence: <br />
            <strong>{predictionResult ? `${predictionResult.confidence_score}%` : "--"}</strong>
          </div>
        </div>
      </section>
    </div>
  );
}

