import React from "react";
import { useGetTransactionsQuery } from "../api/transactionApi";

export default function TransactionsPage() {
  const { data: transactions, isLoading, error } = useGetTransactionsQuery(null, { pollingInterval: 30000 });
  const [selectedTx, setSelectedTx] = React.useState(null);

  if (isLoading) return <div style={{ padding: "2rem" }}>Loading transactions...</div>;
  if (error) return <div style={{ padding: "2rem", color: "red" }}>Error loading transactions.</div>;

  return (
    <section className="panel" style={{ position: 'relative' }}>
      <div className="panel-header">
        <div>
          <h2>Transaction history</h2>
          <p className="subtle-text">Latest user-submitted and system-reviewed records</p>
        </div>
        <button type="button" className="secondary-button">Export CSV</button>
      </div>

      <div className="table-list">
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Transaction ID</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Amount</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Merchant</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Prediction</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Risk Score</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Action</th>
              <th style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>Details</th>
            </tr>
          </thead>
          <tbody>
            {transactions?.map((item) => (
              <tr key={item.id}>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>{item.transaction_id}</td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>{item.currency} {item.amount}</td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>{item.merchant_name}</td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>
                  <span className={`status-pill ${item.prediction === "Normal" ? "success" : "danger"}`}>
                    {item.prediction || "Unknown"}
                  </span>
                </td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>{item.risk_score}</td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>{item.action}</td>
                <td style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>
                  <button className="secondary-button" onClick={() => setSelectedTx(item)} style={{ padding: "0.25rem 0.5rem", fontSize: "0.8rem" }}>
                    View
                  </button>
                </td>
              </tr>
            ))}
            {transactions?.length === 0 && (
              <tr>
                <td colSpan="7" style={{ padding: '1rem', textAlign: 'center', color: '#64748b' }}>No transactions found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {selectedTx && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, 
          backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', 
          justifyContent: 'center', alignItems: 'center', zIndex: 1000
        }}>
          <div style={{
            backgroundColor: '#fff', padding: '2rem', borderRadius: '8px', 
            width: '100%', maxWidth: '600px', maxHeight: '90vh', overflowY: 'auto'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid #eee', paddingBottom: '0.5rem' }}>
              <h2 style={{ margin: 0 }}>Transaction Details</h2>
              <button onClick={() => setSelectedTx(null)} style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer' }}>&times;</button>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>Core Info</h4>
                <p><strong>ID:</strong> {selectedTx.transaction_id}</p>
                <p><strong>Amount:</strong> {selectedTx.currency} {selectedTx.amount}</p>
                <p><strong>Type:</strong> {selectedTx.transaction_type}</p>
                <p><strong>Time:</strong> {new Date(selectedTx.transaction_time).toLocaleString()}</p>
              </div>
              
              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>ML Analysis</h4>
                <p><strong>Prediction:</strong> <span className={`status-pill ${selectedTx.prediction === "Normal" ? "success" : "danger"}`}>{selectedTx.prediction}</span></p>
                <p><strong>Risk Score:</strong> {selectedTx.risk_score}</p>
                <p><strong>Confidence:</strong> {selectedTx.confidence_score}%</p>
                <p><strong>System Action:</strong> {selectedTx.action}</p>
                <p><strong>Model:</strong> {selectedTx.model_version}</p>
              </div>

              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>Sender</h4>
                <p><strong>Name:</strong> {selectedTx.sender_name}</p>
                <p><strong>Account:</strong> {selectedTx.sender_account_number}</p>
                <p><strong>Bank:</strong> {selectedTx.sender_bank}</p>
              </div>

              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>Receiver</h4>
                <p><strong>Name:</strong> {selectedTx.receiver_name}</p>
                <p><strong>Account:</strong> {selectedTx.receiver_account_number}</p>
                <p><strong>Bank:</strong> {selectedTx.receiver_bank}</p>
              </div>
              
              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>Merchant</h4>
                <p><strong>Name:</strong> {selectedTx.merchant_name}</p>
                <p><strong>Category:</strong> {selectedTx.merchant_category}</p>
                <p><strong>Location:</strong> {selectedTx.city}, {selectedTx.country}</p>
              </div>
              
              <div>
                <h4 style={{ color: '#4f46e5', marginBottom: '0.5rem' }}>Device & Network</h4>
                <p><strong>IP:</strong> {selectedTx.ip_address}</p>
                <p><strong>Device:</strong> {selectedTx.device_type}</p>
                <p><strong>OS:</strong> {selectedTx.operating_system} {selectedTx.os_version}</p>
                <p><strong>Browser:</strong> {selectedTx.browser}</p>
              </div>
            </div>
            
            <div style={{ marginTop: '2rem', textAlign: 'right' }}>
              <button className="primary-button" onClick={() => setSelectedTx(null)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
