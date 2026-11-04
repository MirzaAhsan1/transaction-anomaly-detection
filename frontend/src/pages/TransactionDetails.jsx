export default function TransactionDetailsPage() {
  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Transaction details</h2>
            <p className="subtle-text">Full record and fraud decision metadata</p>
          </div>
          <span className="status-pill danger">Requires review</span>
        </div>

        <div className="metric-row">
          <div>Transaction ID: TXN-18572</div>
          <div>Customer: D. Walker</div>
          <div>Amount: $7,200.00</div>
        </div>

        <div className="metric-row" style={{ marginTop: 12 }}>
          <div>Prediction: Suspicious</div>
          <div>Risk score: 86.4</div>
          <div>Alert sent: Yes</div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Model reasoning snapshot</h2>
            <p className="subtle-text">Feature signals behind the decision</p>
          </div>
        </div>

        <div className="bar-stack">
          <div className="bar-row">
            <span>Geo inconsistency</span>
            <div className="bar-track"><div className="bar-fill" style={{ width: "82%" }}></div></div>
            <span>82%</span>
          </div>

          <div className="bar-row">
            <span>Velocity</span>
            <div className="bar-track"><div className="bar-fill" style={{ width: "68%" }}></div></div>
            <span>68%</span>
          </div>

          <div className="bar-row">
            <span>Device trust</span>
            <div className="bar-track"><div className="bar-fill" style={{ width: "57%" }}></div></div>
            <span>57%</span>
          </div>
        </div>
      </section>
    </div>
  );
}
