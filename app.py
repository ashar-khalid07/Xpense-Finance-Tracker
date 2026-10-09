from __future__ import annotations

import csv
import io
import os
from datetime import date as dt_date, datetime
from decimal import Decimal, InvalidOperation

from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Health"]


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=dt_date.today)

    def __repr__(self) -> str:
        return f"<Expense {self.id}: {self.description}>"


def parse_date_or_none(value: str | None) -> dt_date | None:
    """Convert YYYY-MM-DD text into a date object, or return None."""
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def read_filters():
    """Read and validate the dashboard filters from the query string."""
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_str and not start_date:
        flash("Start date is invalid.", "error")
        start_str = ""

    if end_str and not end_date:
        flash("End date is invalid.", "error")
        end_str = ""

    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date.", "error")
        start_date = None
        end_date = None
        start_str = ""
        end_str = ""

    if selected_category and selected_category not in CATEGORIES:
        flash("Unknown category filter ignored.", "error")
        selected_category = ""

    return start_str, end_str, start_date, end_date, selected_category


def apply_filters(query, start_date, end_date, selected_category):
    """Apply the same optional filters to any Expense-based SQLAlchemy query."""
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if selected_category:
        query = query.filter(Expense.category == selected_category)
    return query


@app.route("/")
def index():
    start_str, end_str, start_date, end_date, selected_category = read_filters()

    query = apply_filters(Expense.query, start_date, end_date, selected_category)
    expenses = query.order_by(Expense.date.desc(), Expense.id.desc()).all()

    total = sum((expense.amount for expense in expenses), Decimal("0.00"))

    category_query = db.session.query(
        Expense.category,
        func.sum(Expense.amount),
    )
    category_query = apply_filters(
        category_query,
        start_date,
        end_date,
        selected_category,
    )
    category_rows = category_query.group_by(Expense.category).all()
    cat_labels = [category for category, _ in category_rows]
    cat_values = [round(float(value or 0), 2) for _, value in category_rows]

    day_query = db.session.query(
        Expense.date,
        func.sum(Expense.amount),
    )
    day_query = apply_filters(day_query, start_date, end_date, selected_category)
    day_rows = (
        day_query.group_by(Expense.date)
        .order_by(Expense.date.asc())
        .all()
    )
    day_labels = [day.isoformat() for day, _ in day_rows]
    day_values = [round(float(value or 0), 2) for _, value in day_rows]

    return render_template(
        "index.html",
        expenses=expenses,
        categories=CATEGORIES,
        total=total,
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        today=dt_date.today().isoformat(),
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values,
    )


@app.route("/add", methods=["POST"])
def add():
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Please fill in description, amount and category.", "error")
        return redirect(url_for("index"))

    if category not in CATEGORIES:
        flash("Please choose a valid category.", "error")
        return redirect(url_for("index"))

    try:
        amount = Decimal(amount_str).quantize(Decimal("0.01"))
        if amount <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("index"))

    expense_date = parse_date_or_none(date_str) if date_str else dt_date.today()
    if date_str and not expense_date:
        flash("Please enter a valid date.", "error")
        return redirect(url_for("index"))

    expense = Expense(
        description=description,
        amount=amount,
        category=category,
        date=expense_date or dt_date.today(),
    )
    db.session.add(expense)
    db.session.commit()

    flash("Expense added.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id: int):
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


@app.route("/edit/<int:expense_id>", methods=["GET"])
def edit(expense_id: int):
    expense = db.get_or_404(Expense, expense_id)
    return render_template(
        "edit.html",
        expense=expense,
        categories=CATEGORIES,
        today=dt_date.today().isoformat(),
    )


@app.route("/edit/<int:expense_id>/update", methods=["POST"])
def edit_expense(expense_id: int):
    expense = db.get_or_404(Expense, expense_id)

    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Please fill in description, amount and category.", "error")
        return redirect(url_for("edit", expense_id=expense.id))

    if category not in CATEGORIES:
        flash("Please choose a valid category.", "error")
        return redirect(url_for("edit", expense_id=expense.id))

    try:
        amount = Decimal(amount_str).quantize(Decimal("0.01"))
        if amount <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("edit", expense_id=expense.id))

    if date_str:
        expense_date = parse_date_or_none(date_str)
        if not expense_date:
            flash("Please enter a valid date.", "error")
            return redirect(url_for("edit", expense_id=expense.id))
    else:
        expense_date = dt_date.today()

    expense.description = description
    expense.amount = amount
    expense.category = category
    expense.date = expense_date

    db.session.commit()
    flash("Expense updated.", "success")
    return redirect(url_for("index"))


@app.route("/export/csv")
def export_csv():
    start_str, end_str, start_date, end_date, selected_category = read_filters()

    query = apply_filters(Expense.query, start_date, end_date, selected_category)
    expenses = query.order_by(Expense.date.asc(), Expense.id.asc()).all()

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Category", "Amount"])

    for expense in expenses:
        writer.writerow(
            [
                expense.date.isoformat(),
                expense.description,
                expense.category,
                f"{expense.amount:.2f}",
            ]
        )

    start_name = start_str or "all"
    end_name = end_str or "all"
    filename = f"expenses_{start_name}_to_{end_name}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
