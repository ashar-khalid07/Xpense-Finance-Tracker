# Architecture notes

## Request flow

Browser -> Flask route -> validation/query -> SQLAlchemy -> SQLite -> Flask/Jinja -> HTML -> Chart.js.

## Why the main data model is small

An expense needs only an ID, description, amount, category and date for the current feature set. The ID is an implementation identity; the other four fields are user/business data.

## Why Decimal/Numeric for money

Binary floating-point values cannot exactly represent many decimal fractions. `Numeric(10, 2)` in the database and `Decimal` in Python better match currency semantics.

## Why GET for filters

Filtering is read-only and should be bookmarkable/shareable. Query strings such as `?start=2026-10-01&category=Food` expose the current view in the URL and do not mutate data.

## Why POST for add/update/delete

Those actions change server state. Using POST separates mutations from read-only navigation and avoids destructive actions being represented as ordinary links.

## Why aggregate in SQL

`SUM(...) GROUP BY category` and `SUM(...) GROUP BY date` let the database reduce many expense rows into a small result set. That is generally preferable to loading every row into Python solely to calculate chart totals.

## Current complexity characteristics

The application has no custom database indexes beyond the primary key. For a small personal tracker that is acceptable. As data grows, indexes on `date`, `category`, or a composite `(category, date)` index could improve filtered queries. The exact benefit depends on workload and should be measured rather than assumed.

## Production hardening ideas

Move the secret key to an environment variable; add CSRF protection; add user accounts/ownership if multi-user; use database migrations; add automated tests; paginate long expense lists; consider a production WSGI server; introduce blueprints/service modules when `app.py` becomes too large; consider a category table if users can create categories.
