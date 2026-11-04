const inboxEmails = [
  {
    id: "EML-2041",
    sender: "priority-support@bank.example",
    subject: "Urgent payout confirmation request",
    risk: "Fraud",
  },
  {
    id: "EML-2042",
    sender: "alerts@securepay.example",
    subject: "Login verification for new device",
    risk: "Spam",
  },
  {
    id: "EML-2043",
    sender: "finance-team@merchant.example",
    subject: "Invoice resubmission for Q3 settlement",
    risk: "Safe",
  },
  {
    id: "EML-2044",
    sender: "support@banking.co",
    subject: "Account activity summary",
    risk: "Safe",
  },
];

export default function EmailsPage() {
  return (
    <div className="page-grid">
      <section className="panel panel-wide">
        <div className="panel-header">
          <div>
            <h2>Email intelligence</h2>
            <p className="subtle-text">All incoming emails and their risk labels</p>
          </div>
        </div>

        <div className="table-list">
          <table>
            <thead>
              <tr>
                <th>Email ID</th>
                <th>Sender</th>
                <th>Subject</th>
                <th>Classification</th>
              </tr>
            </thead>
            <tbody>
              {inboxEmails.map((email) => (
                <tr key={email.id}>
                  <td>{email.id}</td>
                  <td>{email.sender}</td>
                  <td>{email.subject}</td>
                  <td>
                    <span className={`status-pill ${email.risk === "Fraud" ? "danger" : email.risk === "Spam" ? "warning" : "success"}`}>
                      {email.risk}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Fraud / spam queue</h2>
            <p className="subtle-text">High-priority email messages requiring review</p>
          </div>
        </div>

        <div className="email-list">
          {inboxEmails
            .filter((email) => email.risk !== "Safe")
            .map((email) => (
              <div key={email.id} className="email-item">
                <strong>{email.subject}</strong>
                <p className="subtle-text">{email.sender}</p>
                <div className="email-badges">
                  <span>{email.risk}</span>
                  <span>{email.id}</span>
                </div>
              </div>
            ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Inbox summary</h2>
            <p className="subtle-text">Current classification snapshot</p>
          </div>
        </div>

        <div className="metric-row">
          <div>Total emails: 128</div>
          <div>Fraud flagged: 12</div>
          <div>Spam identified: 19</div>
        </div>
      </section>
    </div>
  );
}
