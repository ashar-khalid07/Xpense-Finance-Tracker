"""Prototype 8: CRUD update/delete patterns.

Assumes Flask/SQLAlchemy objects are available from the main application.
"""


def delete_pattern(db, Expense, expense_id):
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()


def update_pattern(db, Expense, expense_id, validated_data):
    expense = db.get_or_404(Expense, expense_id)

    expense.description = validated_data["description"]
    expense.amount = validated_data["amount"]
    expense.category = validated_data["category"]
    expense.date = validated_data["date"]

    db.session.commit()
    return expense
