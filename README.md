# Xpense

Xpense is a personal expense tracker I built with Flask. It lets you record expenses, filter spending by date or category, view totals and charts, and export the current view to CSV.

## Features

- Add, edit and delete expenses
- Store description, amount, category and date in SQLite
- Filter expenses by date range and category
- Show totals for the current filtered view
- Visualise spending by category and by day
- Export filtered expenses to CSV
- Validate form input on the server

## Technologies

- Python
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- Jinja
- Chart.js
- Tailwind CSS via CDN


## Getting Started

Clone the repository, create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

The database is created automatically at `instance/expenses.db`.

## Project Structure

```text
app.py             Flask routes, validation, model and queries
templates/         Jinja templates for the dashboard and edit form
testing/           Manual test plan and representative test data
requirements.txt   Python dependencies
```

## Testing

`testing/11_test_plan.md` contains a manual test plan covering start-up, validation, filtering, editing, deletion, CSV export and decimal currency behaviour.

`testing/10_seed_test_data.py` contains representative data and expected totals for checking those cases.

These are manual testing resources rather than an automated test suite.

## What I Built

I built the Flask routes, SQLAlchemy expense model, validation, CRUD operations, filtering, chart data, CSV export and the Jinja-based interface.

## Possible Next Steps

- Add automated tests
- Add CSRF protection
- Add pagination if the amount of stored data grows
