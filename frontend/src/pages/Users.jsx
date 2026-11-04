const users = [
  { name: "Aisha Khan", role: "Senior Fraud Analyst", status: "Online" },
  { name: "Rahul Mehta", role: "Risk Operations Lead", status: "Reviewing" },
  { name: "Nora Silva", role: "Case Manager", status: "Offline" },
];

export default function UsersPage() {
  return (
    <div className="page-grid">
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Users</h2>
            <p className="subtle-text">Team members assigned to fraud operations</p>
          </div>
        </div>

        <div className="list-stack">
          {users.map((user) => (
            <div key={user.name} className="user-item">
              <strong>{user.name}</strong>
              <p className="subtle-text">{user.role}</p>
              <span className={`status-pill ${user.status === "Online" ? "success" : user.status === "Reviewing" ? "warning" : "danger"}`}>
                {user.status}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Access controls</h2>
            <p className="subtle-text">Permissions for dashboard and case queues</p>
          </div>
        </div>

        <div className="metric-row">
          <div>Admin access: 2 users</div>
          <div>Investigator access: 6 users</div>
          <div>Read-only access: 4 users</div>
        </div>
      </section>
    </div>
  );
}
