# Xpense – Development Prototypes

> **Portfolio note:** These files are supplementary reference snapshots retained for learning/interview review. They are not intended to reconstruct the project's historical Git commits or original development timeline.

These files are educational snapshots showing how the final Xpense Flask application can be decomposed into progressively more capable prototypes. They are designed for interview revision: each prototype isolates one concept before the concepts are combined in the final application.

## Suggested order

1. `00_minimal_flask.py` – prove Flask routing works.
2. `01_in_memory_expenses.py` – model expenses with basic Python data structures before adding a database.
3. `02_sqlalchemy_model.py` – replace temporary data with persistent SQLite storage.
4. `03_add_expense_validation.py` – accept and validate form input.
5. `04_list_total_and_sort.py` – retrieve, order and total expenses.
6. `05_filter_pipeline.py` – parse and apply date/category filters.
7. `06_category_chart_backend.py` – aggregate spend by category for a pie chart.
8. `07_daily_bar_chart_backend.py` – aggregate spend by day for a bar chart.
9. `templates/chart_prototype.html` – convert Python chart data safely into JavaScript/Chart.js.
10. `08_edit_delete.py` – CRUD update/delete prototypes.
11. `09_csv_export.py` – export filtered data safely with Python's CSV writer.
12. `10_seed_test_data.py` – representative manual test data.
13. `11_test_plan.md` – functional, validation and edge-case test cases.
14. `12_architecture_notes.md` – final architecture, data flow and future improvements.

These are prototypes rather than separate production applications. Some files deliberately omit unrelated boilerplate so the idea being demonstrated is easy to see.
