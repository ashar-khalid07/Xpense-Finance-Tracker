# Xpense – Personal Expense Tracker

Xpense is a Flask web application for recording personal expenses, filtering spending data and visualising totals. It stores expense records in SQLite through Flask-SQLAlchemy and renders category and daily-spend charts with Chart.js.

## Features

- Add, edit and delete expenses with server-side validation
- Store description, amount, category and date in SQLite
- Filter by date range and category
- Recalculate filtered totals and chart data from the same query conditions
- Category spending pie chart and daily spending bar chart
- Export the currently filtered expense data to CSV
- Flash messages for validation errors and successful changes

## Technologies

- Python
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- Jinja templates
- Chart.js
- Tailwind CSS via CDN

## Screenshots

No generated or mock screenshot is included. Run the application locally to view the current interface.

## Getting Started

Clone the repository, create a virtual environment and install the declared dependencies:

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

The database is created automatically at `instance/expenses.db`. The application generates an ephemeral Flask secret key when `SECRET_KEY` is not supplied. For a persistent deployment, set `SECRET_KEY` in the environment. Flask debug mode is off by default; set `FLASK_DEBUG=1` only for local development.

## Project Structure

```text
app.py                    Flask routes, validation, model and queries
templates/                Jinja templates for the dashboard and edit form
testing/                  Manual test plan and representative test data
development-prototypes/   Supplementary reference prototypes and notes
requirements.txt          Python dependencies
```

The numbered files under `development-prototypes/` are supplementary learning/reference material retained with the project. They should not be interpreted as reconstructed Git history or historical commits from the original development period.

## Testing

`testing/11_test_plan.md` contains a manual functional test plan covering start-up, validation, sorting, filtering, editing, deletion, CSV export and decimal currency behaviour. `testing/10_seed_test_data.py` contains representative data and expected totals for exercising those cases.

These are manual testing resources; they are not an automated test suite.

## What I Worked On

This was an individual project. My implementation work represented in this repository includes the Flask routes, SQLAlchemy expense model, validation, CRUD operations, filter pipeline, SQL aggregation for charts, CSV export and the Jinja-based interface.

## Further Improvements

Potential future improvements include adding automated tests, CSRF protection for state-changing forms, database migrations, pagination for larger datasets and user accounts if the application were expanded beyond a single-user local tool.
