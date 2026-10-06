"""Prototype 7: aggregate expenses by calendar day for the daily bar chart."""
from sqlalchemy import func


def daily_chart_data(db, Expense, apply_filters, start_date=None, end_date=None, category=""):
    query = db.session.query(
        Expense.date,
        func.sum(Expense.amount),
    )

    query = apply_filters(
        query,
        Expense,
        start_date,
        end_date,
        category,
    )

    rows = (
        query
        .group_by(Expense.date)
        .order_by(Expense.date.asc())
        .all()
    )

    labels = [day.isoformat() for day, _ in rows]
    values = [round(float(total or 0), 2) for _, total in rows]

    return labels, values
