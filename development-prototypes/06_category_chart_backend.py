"""Prototype 6: prepare category totals for a Chart.js pie chart."""
from sqlalchemy import func


def category_chart_data(db, Expense, apply_filters, start_date=None, end_date=None, category=""):
    query = db.session.query(
        Expense.category,
        func.sum(Expense.amount),
    )

    query = apply_filters(
        query,
        Expense,
        start_date,
        end_date,
        category,
    )

    rows = query.group_by(Expense.category).all()
    labels = [category_name for category_name, _ in rows]
    values = [round(float(total or 0), 2) for _, total in rows]

    return labels, values
