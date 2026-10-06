"""Prototype 5: parse query-string filters once and reuse the same pipeline."""
from datetime import datetime


def parse_date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def apply_filters(query, Expense, start_date=None, end_date=None, category=""):
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if category:
        query = query.filter(Expense.category == category)
    return query
