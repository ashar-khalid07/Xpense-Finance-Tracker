"""Prototype 3: accept form data, validate it, then create a database row.

Assumes `app`, `db`, `Expense`, and CATEGORIES already exist.
"""
from datetime import date as dt_date, datetime
from decimal import Decimal, InvalidOperation
from flask import flash, redirect, request, url_for

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Health"]


def parse_date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def add_expense_prototype():
    description = (request.form.get("description") or "").strip()
    amount_text = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_text = (request.form.get("date") or "").strip()

    if not description or not amount_text or not category:
        flash("Description, amount and category are required.", "error")
        return redirect(url_for("index"))

    if category not in CATEGORIES:
        flash("Choose a valid category.", "error")
        return redirect(url_for("index"))

    try:
        amount = Decimal(amount_text).quantize(Decimal("0.01"))
        if amount <= 0:
            raise InvalidOperation
    except (InvalidOperation, ValueError):
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("index"))

    expense_date = parse_date_or_none(date_text) if date_text else dt_date.today()
    if date_text and expense_date is None:
        flash("Enter a valid date.", "error")
        return redirect(url_for("index"))

    return {
        "description": description,
        "amount": amount,
        "category": category,
        "date": expense_date,
    }
