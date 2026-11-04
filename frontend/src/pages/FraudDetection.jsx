export default function FraudDetectionPage() {
  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>New transaction review</h2>
            <p className="subtle-text">Enter transaction details to calculate anomaly probability</p>
          </div>
        </div>

        <div className="form-grid">
          <label className="field">
            <span>Transaction ID</span>
            <input type="text" defaultValue="TXN-18427" />
          </label>

          <label className="field">
            <span>Amount</span>
            <input type="text" defaultValue="$12,450.00" />
          </label>

          <label className="field">
            <span>Channel</span>
            <select defaultValue="mobile">
              <option value="mobile">Mobile App</option>
              <option value="web">Web Portal</option>
              <option value="ivr">IVR</option>
            </select>
          </label>

          <label className="field">
            <span>Merchant category</span>
            <select defaultValue="travel">
              <option value="travel">Travel</option>
              <option value="retail">Retail</option>
              <option value="banking">Banking</option>
            </select>
          </label>

          <label className="field">
            <span>Customer country</span>
            <input type="text" defaultValue="United States" />
          </label>

          <label className="field">
            <span>Device trust score</span>
            <input type="text" defaultValue="41" />
          </label>

          <label className="field single-field">
            <span>Reason code / notes</span>
            <textarea defaultValue="Repeated transfers to a newly linked beneficiary with inconsistent geolocation activity." />
          </label>
        </div>

        <div className="topbar-actions" style={{ marginTop: 18 }}>
          <button type="button" className="primary-button">Run fraud check</button>
          <button type="button" className="ghost-button">Clear form</button>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Prediction outcome</h2>
            <p className="subtle-text">ML output from Isolation Forest</p>
          </div>
          <span className="status-pill danger">High priority</span>
        </div>

        <div className="score-card">
          <div className="score-number">87.4%</div>
          <p className="subtle-text">Fraud confidence overlap</p>
        </div>

        <div className="mini-grid" style={{ marginTop: 16 }}>
          <div className="metric-row">
            <div>Risk level: High</div>
            <div>Anomaly score: 0.91</div>
          </div>
          <div className="metric-row">
            <div>Confidence: 0.88</div>
            <div>Decision: Hold review</div>
          </div>
        </div>
      </section>
    </div>
  );
}
