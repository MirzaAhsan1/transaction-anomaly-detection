export default function ProfilePage() {
  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Profile</h2>
            <p className="subtle-text">Fraud analyst account profile</p>
          </div>
        </div>

        <div className="metric-row">
          <div>Name: Aisha Khan</div>
          <div>Role: Senior Fraud Analyst</div>
          <div>Team: Risk Operations</div>
        </div>

        <div className="metric-row" style={{ marginTop: 12 }}>
          <div>Cases reviewed: 146</div>
          <div>Accuracy: 94%</div>
          <div>Access level: Full</div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Preferences</h2>
            <p className="subtle-text">Workspace settings for analyst focus</p>
          </div>
        </div>

        <div className="metric-row">
          <div>Email alerts: Enabled</div>
          <div>Dashboard auto-refresh: Enabled</div>
          <div>Theme: Dark workspace</div>
        </div>
      </section>
    </div>
  );
}
