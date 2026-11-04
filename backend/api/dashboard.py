from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from db.session import get_db
from models.transaction import Transaction
from api.transactions import get_current_user
from schemas.transaction import TransactionResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# ---------------------------------------------------------------------------
# Helper: risk score bucket label
# ---------------------------------------------------------------------------
def _risk_bucket(score: float) -> str:
    if score < 20:
        return "0-20"
    elif score < 40:
        return "20-40"
    elif score < 60:
        return "40-60"
    elif score < 80:
        return "60-80"
    else:
        return "80-100"


# ---------------------------------------------------------------------------
# Consolidated stats endpoint — returns EVERYTHING the dashboard needs
# in a single request so the frontend doesn't make 5 separate calls.
# All queries are filtered to the currently authenticated user.
# ---------------------------------------------------------------------------
@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    uid = current_user.id

    # ── Scalar aggregations (one round-trip) ────────────────────────────
    totals = (
        db.query(
            func.count(Transaction.id).label("total"),
            func.sum(Transaction.amount).label("total_amount"),
            func.avg(Transaction.amount).label("avg_amount"),
            func.max(Transaction.amount).label("max_amount"),
            func.min(Transaction.amount).label("min_amount"),
            func.avg(Transaction.risk_score).label("avg_risk"),
            func.max(Transaction.risk_score).label("max_risk"),
            func.min(Transaction.risk_score).label("min_risk"),
        )
        .filter(Transaction.user_id == uid)
        .one()
    )

    # Prediction counts
    fraud_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == uid, Transaction.prediction == "Fraud")
        .scalar()
        or 0
    )
    normal_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == uid, Transaction.prediction == "Normal")
        .scalar()
        or 0
    )

    # Action counts
    blocked_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == uid, Transaction.action == "Block")
        .scalar()
        or 0
    )
    approved_count = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.user_id == uid, Transaction.action == "Approve")
        .scalar()
        or 0
    )

    total = totals.total or 0
    fraud_rate = round((fraud_count / total) * 100, 1) if total > 0 else 0.0

    # ── Recent transactions (last 10, user-scoped) ──────────────────────
    recent_rows = (
        db.query(Transaction)
        .filter(Transaction.user_id == uid)
        .order_by(desc(Transaction.created_at))
        .limit(10)
        .all()
    )

    # ── Monthly breakdown ───────────────────────────────────────────────
    # Group by year-month so chart covers the actual data range
    monthly_rows = (
        db.query(
            func.to_char(Transaction.created_at, "Mon YYYY").label("month"),
            func.date_trunc("month", Transaction.created_at).label("month_start"),
            func.count(Transaction.id).label("total"),
        )
        .filter(Transaction.user_id == uid)
        .group_by("month", "month_start")
        .order_by("month_start")
        .all()
    )

    # Build month→fraud count via Python (avoids cast dialect issues)
    month_fraud: dict[str, int] = defaultdict(int)
    for t in (
        db.query(
            func.to_char(Transaction.created_at, "Mon YYYY").label("month"),
        )
        .filter(Transaction.user_id == uid, Transaction.prediction == "Fraud")
        .all()
    ):
        month_fraud[t.month] += 1

    transactions_by_month = [
        {
            "month": row.month,
            "total": row.total,
            "fraud": month_fraud.get(row.month, 0),
            "normal": row.total - month_fraud.get(row.month, 0),
        }
        for row in monthly_rows
    ]

    # ── Payment method distribution ─────────────────────────────────────
    pm_rows = (
        db.query(Transaction.payment_method, func.count(Transaction.id).label("cnt"))
        .filter(Transaction.user_id == uid)
        .group_by(Transaction.payment_method)
        .order_by(desc("cnt"))
        .all()
    )
    transactions_by_payment_method = [
        {"name": r.payment_method or "Unknown", "value": r.cnt} for r in pm_rows
    ]

    most_used_pm = pm_rows[0].payment_method if pm_rows else None

    # ── Prediction distribution ─────────────────────────────────────────
    transactions_by_prediction = [
        {"name": "Normal", "value": normal_count},
        {"name": "Fraud", "value": fraud_count},
    ]

    # ── Country distribution (top 10) ───────────────────────────────────
    country_rows = (
        db.query(Transaction.country, func.count(Transaction.id).label("cnt"))
        .filter(Transaction.user_id == uid)
        .group_by(Transaction.country)
        .order_by(desc("cnt"))
        .limit(10)
        .all()
    )
    transactions_by_country = [
        {"name": r.country or "Unknown", "value": r.cnt} for r in country_rows
    ]

    most_active_country = country_rows[0].country if country_rows else None

    # ── Risk score distribution ─────────────────────────────────────────
    # Fetch all risk scores for the user, then bucket in Python
    risk_scores = (
        db.query(Transaction.risk_score)
        .filter(Transaction.user_id == uid, Transaction.risk_score.isnot(None))
        .all()
    )

    bucket_counts: dict[str, int] = {
        "0-20": 0,
        "20-40": 0,
        "40-60": 0,
        "60-80": 0,
        "80-100": 0,
    }
    for (score,) in risk_scores:
        bucket_counts[_risk_bucket(score)] += 1

    risk_distribution = [
        {"range": k, "count": v} for k, v in bucket_counts.items()
    ]

    # ── Build response ──────────────────────────────────────────────────
    return {
        # Core counts
        "total_transactions": total,
        "normal_transactions": normal_count,
        "fraud_transactions": fraud_count,
        "fraud_rate": fraud_rate,

        # Amount stats
        "total_amount": round(totals.total_amount or 0, 2),
        "average_amount": round(totals.avg_amount or 0, 2),
        "largest_transaction": round(totals.max_amount or 0, 2),
        "smallest_transaction": round(totals.min_amount or 0, 2),

        # Action counts
        "blocked_transactions": blocked_count,
        "approved_transactions": approved_count,

        # Risk stats
        "average_risk_score": round(totals.avg_risk or 0, 2),
        "highest_risk_score": round(totals.max_risk or 0, 2),
        "lowest_risk_score": round(totals.min_risk or 0, 2),

        # Top values
        "most_used_payment_method": most_used_pm,
        "most_active_country": most_active_country,

        # Recent transactions (full objects for the table)
        "recent_transactions": [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "currency": t.currency,
                "merchant_name": t.merchant_name,
                "payment_method": t.payment_method,
                "prediction": t.prediction,
                "risk_score": t.risk_score,
                "action": t.action,
                "country": t.country,
                "created_at": t.created_at.isoformat(),
            }
            for t in recent_rows
        ],

        # Chart data
        "transactions_by_month": transactions_by_month,
        "transactions_by_payment_method": transactions_by_payment_method,
        "transactions_by_prediction": transactions_by_prediction,
        "transactions_by_country": transactions_by_country,
        "risk_distribution": risk_distribution,
    }


# ---------------------------------------------------------------------------
# Keep the existing separate endpoints but fix them to filter by user
# (backwards-compat — dashboardApi.js still defines hooks for them)
# ---------------------------------------------------------------------------

@router.get("/recent-transactions", response_model=list[TransactionResponse])
def get_recent_transactions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(desc(Transaction.created_at))
        .limit(10)
        .all()
    )


@router.get("/fraud-trend")
def get_fraud_trend(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Weekly fraud % trend for the last 7 days (user-scoped)."""
    from datetime import timedelta

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    txns = (
        db.query(Transaction.created_at, Transaction.prediction)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.created_at >= seven_days_ago,
        )
        .all()
    )

    trend: dict[str, dict] = {}
    for t in txns:
        day_str = t.created_at.strftime("%a")
        if day_str not in trend:
            trend[day_str] = {"total": 0, "fraud": 0}
        trend[day_str]["total"] += 1
        if t.prediction == "Fraud":
            trend[day_str]["fraud"] += 1

    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    result = []
    for day in days_order:
        if day in trend:
            val = trend[day]
            percent = (
                round((val["fraud"] / val["total"]) * 100) if val["total"] > 0 else 0
            )
            result.append({"label": day, "value": percent})
        else:
            result.append({"label": day, "value": 0})

    return result


@router.get("/payment-methods")
def get_payment_methods(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    txns = (
        db.query(Transaction.payment_method, func.count(Transaction.id))
        .filter(Transaction.user_id == current_user.id)
        .group_by(Transaction.payment_method)
        .all()
    )
    return [{"name": t[0], "value": t[1]} for t in txns]


@router.get("/device-distribution")
def get_device_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    txns = (
        db.query(Transaction.device_type, func.count(Transaction.id))
        .filter(Transaction.user_id == current_user.id)
        .group_by(Transaction.device_type)
        .all()
    )
    return [{"name": t[0], "value": t[1]} for t in txns]


@router.get("/country-distribution")
def get_country_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    txns = (
        db.query(Transaction.country, func.count(Transaction.id))
        .filter(Transaction.user_id == current_user.id)
        .group_by(Transaction.country)
        .all()
    )
    return [{"name": t[0], "value": t[1]} for t in txns]
