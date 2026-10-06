"""Prototype 9: serialize expenses to a standards-compliant CSV response."""
import csv
import io
from flask import Response


def csv_response(expenses, filename="expenses.csv"):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Category", "Amount"])

    for expense in expenses:
        writer.writerow([
            expense.date.isoformat(),
            expense.description,
            expense.category,
            f"{expense.amount:.2f}",
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
