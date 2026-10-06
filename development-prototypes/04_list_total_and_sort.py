"""Prototype 4: retrieve rows in a useful order and calculate a total."""
from decimal import Decimal


def build_dashboard_data(Expense):
    expenses = Expense.query.order_by(
        Expense.date.desc(),
        Expense.id.desc(),
    ).all()

    total = sum(
        (expense.amount for expense in expenses),
        Decimal("0.00"),
    )

    return expenses, total
