import React from "react";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from "recharts";
import { useGetDashboardStatsQuery } from "../api/dashboardApi";

// ─── Colour palettes ────────────────────────────────────────────────────────
const PREDICTION_COLORS = ["#22c55e", "#ef4444"]; // Normal=green, Fraud=red
const BAR_COLOR         = "#6366f1";               // Indigo for bar charts
const RISK_COLORS       = ["#22c55e", "#84cc16", "#facc15", "#f97316", "#ef4444"];

// ─── Tiny helpers ────────────────────────────────────────────────────────────
function fmt(n)      { return n?.toLocaleString() ?? "—"; }
function fmtAmt(n)   { return n != null ? `$${n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : "—"; }
function fmtPct(n)   { return n != null ? `${n}%` : "—"; }
function fmtDate(s)  {
  if (!s) return "—";
  return new Date(s).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

// ─── Skeleton loader ─────────────────────────────────────────────────────────
function Skeleton({ h = 20, w = "100%", radius = 8 }) {
  return (
    <div
      style={{
        height: h,
        width: w,
        borderRadius: radius,
        background: "linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%)",
        backgroundSize: "200% 100%",
        animation: "shimmer 1.4s infinite linear",
      }}
    />
  );
}

// ─── Stat card ───────────────────────────────────────────────────────────────
function StatCard({ title, value, sub, pillLabel, pillType = "success", loading }) {
  return (
    <article className="stat-card">
      <h3>{title}</h3>
      {loading ? (
        <>
          <Skeleton h={32} w="60%" radius={6} />
          <div style={{ marginTop: 8 }}><Skeleton h={22} w="40%" radius={999} /></div>
        </>
      ) : (
        <>
          <strong style={{ fontSize: 26 }}>{value}</strong>
          {sub && <p className="subtle-text" style={{ marginTop: 2 }}>{sub}</p>}
          {pillLabel && (
            <span className={`status-pill ${pillType}`} style={{ marginTop: 6 }}>
              {pillLabel}
            </span>
          )}
        </>
      )}
    </article>
  );
}

// ─── Section panel wrapper ────────────────────────────────────────────────────
function Panel({ title, subtitle, children, span = 1, action }) {
  return (
    <section className="panel" style={{ gridColumn: span > 1 ? `span ${span}` : undefined }}>
      <div className="panel-header">
        <div>
          <h2 style={{ margin: 0, fontSize: 16 }}>{title}</h2>
          {subtitle && <p className="subtle-text">{subtitle}</p>}
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

// ─── Empty state ─────────────────────────────────────────────────────────────
function EmptyState({ message = "No data yet" }) {
  return (
    <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#94a3b8" }}>
      <div style={{ fontSize: 32, marginBottom: 8 }}>📊</div>
      <p style={{ margin: 0 }}>{message}</p>
    </div>
  );
}

// ─── Main Dashboard ──────────────────────────────────────────────────────────
export default function DashboardPage() {
  // Single consolidated query — all data in one request
  const {
    data: stats,
    isLoading,
    isError,
    error,
  } = useGetDashboardStatsQuery(null, { pollingInterval: 30000 });

  // ── Error state ──────────────────────────────────────────────────────────
  if (isError) {
    return (
      <div className="panel" style={{ textAlign: "center", padding: "3rem" }}>
        <p style={{ color: "#ef4444", fontWeight: 700 }}>
          Failed to load dashboard data.
        </p>
        <p className="subtle-text">
          {error?.data?.detail ?? "Please check your connection and try again."}
        </p>
      </div>
    );
  }

  // ── Derived values ───────────────────────────────────────────────────────
  const s = stats ?? {};

  const statCards = [
    {
      title: "Total Transactions",
      value: fmt(s.total_transactions),
      pillLabel: "All Time",
      pillType: "success",
    },
    {
      title: "Fraud Cases",
      value: fmt(s.fraud_transactions),
      sub: `Fraud rate: ${fmtPct(s.fraud_rate)}`,
      pillLabel: s.fraud_transactions > 0 ? "High Risk" : "Clear",
      pillType: s.fraud_transactions > 0 ? "danger" : "success",
    },
    {
      title: "Normal Transactions",
      value: fmt(s.normal_transactions),
      pillLabel: "Safe Volume",
      pillType: "success",
    },
    {
      title: "Avg. Risk Score",
      value: s.average_risk_score != null ? s.average_risk_score : "—",
      sub: `High: ${s.highest_risk_score ?? "—"} · Low: ${s.lowest_risk_score ?? "—"}`,
      pillLabel: s.average_risk_score > 60 ? "Alerting" : "Stable",
      pillType: s.average_risk_score > 60 ? "warning" : "success",
    },
    {
      title: "Total Amount",
      value: fmtAmt(s.total_amount),
      sub: `Avg: ${fmtAmt(s.average_amount)}`,
      pillLabel: "Volume",
      pillType: "success",
    },
    {
      title: "Largest Transaction",
      value: fmtAmt(s.largest_transaction),
      sub: `Smallest: ${fmtAmt(s.smallest_transaction)}`,
      pillLabel: "Range",
      pillType: "warning",
    },
    {
      title: "Blocked",
      value: fmt(s.blocked_transactions),
      pillLabel: "Blocked by model",
      pillType: s.blocked_transactions > 0 ? "danger" : "success",
    },
    {
      title: "Approved",
      value: fmt(s.approved_transactions),
      pillLabel: "Cleared",
      pillType: "success",
    },
  ];

  const hasMonthly     = s.transactions_by_month?.length > 0;
  const hasPrediction  = s.transactions_by_prediction?.some(d => d.value > 0);
  const hasPayment     = s.transactions_by_payment_method?.length > 0;
  const hasCountry     = s.transactions_by_country?.length > 0;
  const hasRisk        = s.risk_distribution?.some(d => d.count > 0);
  const hasRecent      = s.recent_transactions?.length > 0;

  return (
    <>
      {/* Global shimmer keyframes */}
      <style>{`
        @keyframes shimmer {
          0%   { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>

      <div className="page-grid">

        {/* ── STAT CARDS ─────────────────────────────────────────────── */}
        <section className="stats-grid">
          {statCards.map((card) => (
            <StatCard key={card.title} {...card} loading={isLoading} />
          ))}
        </section>

        {/* ── INSIGHT PILLS ──────────────────────────────────────────── */}
        {!isLoading && (s.most_used_payment_method || s.most_active_country) && (
          <section
            className="panel"
            style={{
              gridColumn: "span 2",
              display: "flex",
              gap: 16,
              flexWrap: "wrap",
              alignItems: "center",
              padding: "14px 20px",
            }}
          >
            <span style={{ fontWeight: 600, color: "#64748b", fontSize: 13 }}>Quick Insights</span>
            {s.most_used_payment_method && (
              <span className="status-pill success">
                💳 Top payment: {s.most_used_payment_method}
              </span>
            )}
            {s.most_active_country && (
              <span className="status-pill warning">
                🌍 Top country: {s.most_active_country}
              </span>
            )}
            <span className="status-pill success">
              🤖 Model v2 · XGBoost
            </span>
          </section>
        )}

        {/* ── FRAUD vs NORMAL PIE ─────────────────────────────────────── */}
        <Panel
          title="Fraud vs Normal"
          subtitle="Prediction distribution"
          action={<span className="status-pill warning">Live</span>}
        >
          {isLoading ? (
            <Skeleton h={220} radius={12} />
          ) : hasPrediction ? (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={s.transactions_by_prediction}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(1)}%`
                  }
                >
                  {s.transactions_by_prediction.map((_, i) => (
                    <Cell key={i} fill={PREDICTION_COLORS[i % PREDICTION_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => fmt(v)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState message="No prediction data yet" />
          )}
        </Panel>

        {/* ── PAYMENT METHOD BAR ─────────────────────────────────────── */}
        <Panel title="Payment Methods" subtitle="Transaction count by method">
          {isLoading ? (
            <Skeleton h={220} radius={12} />
          ) : hasPayment ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart
                data={s.transactions_by_payment_method}
                layout="vertical"
                margin={{ left: 10, right: 20, top: 4, bottom: 4 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis
                  dataKey="name"
                  type="category"
                  width={100}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip />
                <Bar dataKey="value" fill={BAR_COLOR} radius={[0, 6, 6, 0]} name="Transactions" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState message="No payment method data yet" />
          )}
        </Panel>

        {/* ── MONTHLY TRANSACTIONS ────────────────────────────────────── */}
        <Panel
          title="Monthly Transactions"
          subtitle="Normal vs Fraud over time"
          span={2}
        >
          {isLoading ? (
            <Skeleton h={240} radius={12} />
          ) : hasMonthly ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={s.transactions_by_month} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="normal" name="Normal" fill="#22c55e" stackId="a" radius={[0,0,0,0]} />
                <Bar dataKey="fraud"  name="Fraud"  fill="#ef4444" stackId="a" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState message="No monthly data yet. Submit your first transaction!" />
          )}
        </Panel>

        {/* ── RISK SCORE DISTRIBUTION ─────────────────────────────────── */}
        <Panel title="Risk Score Distribution" subtitle="How risky are your transactions?">
          {isLoading ? (
            <Skeleton h={220} radius={12} />
          ) : hasRisk ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={s.risk_distribution} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" name="Transactions" radius={[6, 6, 0, 0]}>
                  {s.risk_distribution.map((_, i) => (
                    <Cell key={i} fill={RISK_COLORS[i % RISK_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState message="No risk data yet" />
          )}
        </Panel>

        {/* ── COUNTRY DISTRIBUTION ────────────────────────────────────── */}
        <Panel title="Top Countries" subtitle="Transaction volume by country">
          {isLoading ? (
            <Skeleton h={220} radius={12} />
          ) : hasCountry ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart
                data={s.transactions_by_country}
                margin={{ top: 8, right: 16, left: 0, bottom: 40 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 11 }}
                  angle={-35}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#8b5cf6" radius={[6, 6, 0, 0]} name="Transactions" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState message="No country data yet" />
          )}
        </Panel>

        {/* ── RECENT TRANSACTIONS TABLE ───────────────────────────────── */}
        <Panel
          title="Recent Transactions"
          subtitle="Latest 10 transactions for your account"
          span={2}
        >
          {isLoading ? (
            <div style={{ display: "grid", gap: 10 }}>
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={i} h={44} radius={10} />
              ))}
            </div>
          ) : hasRecent ? (
            <div className="table-list">
              <table>
                <thead>
                  <tr>
                    <th>Transaction ID</th>
                    <th>Amount</th>
                    <th>Merchant</th>
                    <th>Method</th>
                    <th>Prediction</th>
                    <th>Risk Score</th>
                    <th>Action</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {s.recent_transactions.map((tx) => (
                    <tr key={tx.transaction_id}>
                      <td style={{ fontFamily: "monospace", fontSize: 12 }}>
                        {tx.transaction_id}
                      </td>
                      <td>{tx.currency} {tx.amount?.toLocaleString()}</td>
                      <td>{tx.merchant_name}</td>
                      <td>{tx.payment_method}</td>
                      <td>
                        <span
                          className={`status-pill ${
                            tx.prediction === "Fraud" ? "danger" : "success"
                          }`}
                        >
                          {tx.prediction ?? "—"}
                        </span>
                      </td>
                      <td>
                        <span
                          style={{
                            fontWeight: 700,
                            color:
                              tx.risk_score > 70
                                ? "#ef4444"
                                : tx.risk_score > 40
                                ? "#f97316"
                                : "#22c55e",
                          }}
                        >
                          {tx.risk_score ?? "—"}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`status-pill ${
                            tx.action === "Block" ? "danger" : "success"
                          }`}
                        >
                          {tx.action ?? "—"}
                        </span>
                      </td>
                      <td style={{ color: "#64748b", fontSize: 12 }}>
                        {fmtDate(tx.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState message="No transactions yet. Submit your first transaction to see it here!" />
          )}
        </Panel>

      </div>
    </>
  );
}
