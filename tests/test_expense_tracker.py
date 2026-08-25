import tempfile
import unittest
from pathlib import Path

from expense_tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_directory.name) / "test_expenses.json"
        self.tracker = ExpenseTracker(str(self.data_file))

    def tearDown(self):
        self.temp_directory.cleanup()

    def add_sample_expense(
        self,
        amount=250.00,
        category="Food",
        description="Lunch",
    ):
        return self.tracker.add_expense(
            amount=amount,
            category=category,
            description=description,
            expense_date="2026-08-25",
        )

    def test_add_expense(self):
        expense = self.add_sample_expense()

        self.assertEqual(expense["id"], 1)
        self.assertEqual(expense["amount"], 250.00)
        self.assertEqual(expense["category"], "Food")
        self.assertEqual(expense["description"], "Lunch")
        self.assertEqual(expense["date"], "2026-08-25")
        self.assertTrue(self.data_file.exists())

    def test_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense(
                amount=0,
                category="Food",
                description="Invalid expense",
            )

    def test_edit_expense(self):
        expense = self.add_sample_expense()

        updated = self.tracker.edit_expense(
            expense_id=expense["id"],
            amount=300.50,
            category="Travel",
            description="Bus ticket",
        )

        edited_expense = self.tracker.find_expense_by_id(expense["id"])

        self.assertTrue(updated)
        self.assertEqual(edited_expense["amount"], 300.50)
        self.assertEqual(edited_expense["category"], "Travel")
        self.assertEqual(edited_expense["description"], "Bus ticket")

    def test_delete_expense(self):
        expense = self.add_sample_expense()

        deleted = self.tracker.delete_expense(expense["id"])

        self.assertTrue(deleted)
        self.assertEqual(self.tracker.get_all_expenses(), [])

    def test_filter_and_search_expenses(self):
        self.add_sample_expense(
            amount=200,
            category="Food",
            description="Dinner",
        )
        self.add_sample_expense(
            amount=500,
            category="Travel",
            description="Petrol",
        )

        food_expenses = self.tracker.filter_by_category("food")
        search_results = self.tracker.search_expenses("petrol")

        self.assertEqual(len(food_expenses), 1)
        self.assertEqual(food_expenses[0]["description"], "Dinner")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["category"], "Travel")

    def test_total_and_category_summary(self):
        self.add_sample_expense(
            amount=200,
            category="Food",
            description="Lunch",
        )
        self.add_sample_expense(
            amount=150,
            category="Food",
            description="Dinner",
        )
        self.add_sample_expense(
            amount=500,
            category="Travel",
            description="Petrol",
        )

        summary = self.tracker.get_category_summary()

        self.assertEqual(self.tracker.calculate_total(), 850.00)
        self.assertEqual(summary["Food"], 350.00)
        self.assertEqual(summary["Travel"], 500.00)

    def test_expenses_persist_between_sessions(self):
        self.add_sample_expense()

        reloaded_tracker = ExpenseTracker(str(self.data_file))
        expenses = reloaded_tracker.get_all_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Lunch")


if __name__ == "__main__":
    unittest.main()