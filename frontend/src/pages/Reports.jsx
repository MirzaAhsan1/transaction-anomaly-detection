const reports = [
  { title: "Daily fraud summary", period: "Today", value: "31 flagged cases" },
  { title: "Risk by region", period: "This week", value: "North America 44%" },
  { title: "Merchant anomaly recap", period: "30 days", value: "17 suspicious channels" },
];

export default function ReportsPage() {
  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Executive reports</h2>
            <p className="subtle-text">Prepared summaries for the fraud investigation team</p>
          </div>
        </div>

        <div className="report-list">
          {reports.map((item) => (
            <div key={item.title} className="report-item">
              <strong>{item.title}</strong>
              <p className="subtle-text">{item.period}</p>
              <p>{item.value}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Fraud insights</h2>
            <p className="subtle-text">Highlights from current surveillance</p>
          </div>
        </div>

        <div className="metric-row">
          <div>Spike in international payout attempts</div>
          <div>Three accounts currently under review</div>
          <div>71% of alerts came from mobile-first events</div>
        </div>
      </section>
    </div>
  );
}
