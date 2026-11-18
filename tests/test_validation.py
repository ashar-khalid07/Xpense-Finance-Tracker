import unittest
from datetime import date
from flask import get_flashed_messages

from app import app, parse_date_or_none, read_filters


class ParseDateTests(unittest.TestCase):
    def test_valid_date_is_parsed(self):
        self.assertEqual(parse_date_or_none("2026-11-18"), date(2026, 11, 18))

    def test_blank_date_returns_none(self):
        self.assertIsNone(parse_date_or_none(""))
        self.assertIsNone(parse_date_or_none(None))

    def test_invalid_date_returns_none(self):
        self.assertIsNone(parse_date_or_none("2026-02-30"))
        self.assertIsNone(parse_date_or_none("not-a-date"))


class AddExpenseValidationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def _post_and_get_flashes(self, data):
        response = self.client.post("/add", data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        with self.client.session_transaction() as session:
            flashes = list(session.get("_flashes", []))
            session["_flashes"] = []

        return flashes

    def test_required_fields_are_rejected(self):
        flashes = self._post_and_get_flashes(
            {
                "description": "",
                "amount": "",
                "category": "",
                "date": "2026-11-18",
            }
        )
        self.assertIn(
            ("error", "Please fill in description, amount and category."),
            flashes,
        )

    def test_unknown_category_is_rejected(self):
        flashes = self._post_and_get_flashes(
            {
                "description": "Lunch",
                "amount": "8.50",
                "category": "Other",
                "date": "2026-11-18",
            }
        )
        self.assertIn(("error", "Please choose a valid category."), flashes)

    def test_non_numeric_amount_is_rejected(self):
        flashes = self._post_and_get_flashes(
            {
                "description": "Lunch",
                "amount": "abc",
                "category": "Food",
                "date": "2026-11-18",
            }
        )
        self.assertIn(("error", "Amount must be a positive number."), flashes)

    def test_zero_and_negative_amounts_are_rejected(self):
        for amount in ("0", "-5"):
            with self.subTest(amount=amount):
                flashes = self._post_and_get_flashes(
                    {
                        "description": "Lunch",
                        "amount": amount,
                        "category": "Food",
                        "date": "2026-11-18",
                    }
                )
                self.assertIn(
                    ("error", "Amount must be a positive number."),
                    flashes,
                )

    def test_invalid_date_is_rejected(self):
        flashes = self._post_and_get_flashes(
            {
                "description": "Lunch",
                "amount": "8.50",
                "category": "Food",
                "date": "2026-02-30",
            }
        )
        self.assertIn(("error", "Please enter a valid date."), flashes)


class FilterValidationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def test_reversed_date_range_is_cleared(self):
        with app.test_request_context("/?start=2026-11-20&end=2026-11-18"):
            values = read_filters()
            flashes = get_flashed_messages(with_categories=True)

        self.assertEqual(values, ("", "", None, None, ""))
        self.assertIn(
            ("error", "End date cannot be before start date."),
            flashes,
        )

    def test_unknown_category_filter_is_ignored(self):
        with app.test_request_context("/?category=Other"):
            values = read_filters()
            flashes = get_flashed_messages(with_categories=True)

        self.assertEqual(values[4], "")
        self.assertIn(
            ("error", "Unknown category filter ignored."),
            flashes,
        )


if __name__ == "__main__":
    unittest.main()
