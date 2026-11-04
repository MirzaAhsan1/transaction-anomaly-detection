import { NavLink, Outlet, useLocation } from "react-router-dom";

const navigationItems = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/fraud", label: "Fraud Detection" },
  { path: "/new-transaction", label: "New Transaction" },
  { path: "/transactions", label: "Transactions" },
  { path: "/transaction-details", label: "Transaction Details" },
  { path: "/reports", label: "Reports" },
  { path: "/users", label: "Users" },
  { path: "/emails", label: "Emails" },
  { path: "/profile", label: "Profile" },
];

export default function DashboardLayout() {
  const location = useLocation();

  const activeLabel =
    navigationItems.find((item) => item.path === location.pathname)?.label ?? "Dashboard";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-chip">TXN AI</div>
          <p className="sidebar-title">Transaction Anomaly Desk</p>
        </div>

        <nav className="nav-stack">
          {navigationItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-button ${isActive ? "active" : ""}`}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="content-area">
        <header className="topbar">
          <div>
            <p className="eyebrow">Fraud analyst workspace</p>
            <h1>{activeLabel}</h1>
          </div>

          <div className="topbar-actions">
            <span className="status-pill success">Live monitoring</span>
            <button type="button" className="ghost-button">
              View alerts
            </button>
          </div>
        </header>

        <Outlet />
      </main>
    </div>
  );
}
