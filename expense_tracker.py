import json
from datetime import date
from pathlib import Path


class ExpenseTracker:
    def __init__(self, file_path: str = "expenses.json"):
        self.file_path = Path(file_path)
        self.expenses = self._load_expenses()

    def _load_expenses(self) -> list[dict]:
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            normalized_expenses = []

            for index, expense in enumerate(data, start=1):
                if not isinstance(expense, dict):
                    continue

                normalized_expenses.append(
                    {
                        "id": expense.get("id", index),
                        "amount": float(expense.get("amount", 0)),
                        "category": str(
                            expense.get("category", "Other")
                        ).strip().title(),
                        "description": str(
                            expense.get("description", "")
                        ).strip(),
                        "date": expense.get("date", "Not recorded"),
                    }
                )

            return normalized_expenses

        except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
            return []

    def _save_expenses(self) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.expenses, file, indent=4)

    def _get_next_id(self) -> int:
        existing_ids = [
            expense["id"]
            for expense in self.expenses
            if isinstance(expense.get("id"), int)
        ]

        return max(existing_ids, default=0) + 1

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        expense_date: str | None = None,
    ) -> dict:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        category = category.strip().title()
        description = description.strip()

        if not category:
            raise ValueError("Category cannot be empty.")

        expense = {
            "id": self._get_next_id(),
            "amount": round(amount, 2),
            "category": category,
            "description": description,
            "date": expense_date or date.today().isoformat(),
        }

        self.expenses.append(expense)
        self._save_expenses()

        return expense

    def get_all_expenses(self) -> list[dict]:
        return self.expenses.copy()

    def find_expense_by_id(self, expense_id: int) -> dict | None:
        for expense in self.expenses:
            if expense["id"] == expense_id:
                return expense

        return None

    def edit_expense(
        self,
        expense_id: int,
        amount: float | None = None,
        category: str | None = None,
        description: str | None = None,
        expense_date: str | None = None,
    ) -> bool:
        expense = self.find_expense_by_id(expense_id)

        if expense is None:
            return False

        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            expense["amount"] = round(amount, 2)

        if category is not None:
            category = category.strip().title()

            if not category:
                raise ValueError("Category cannot be empty.")

            expense["category"] = category

        if description is not None:
            expense["description"] = description.strip()

        if expense_date is not None:
            expense["date"] = expense_date

        self._save_expenses()
        return True

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.find_expense_by_id(expense_id)

        if expense is None:
            return False

        self.expenses.remove(expense)
        self._save_expenses()

        return True

    def filter_by_category(self, category: str) -> list[dict]:
        category = category.strip().casefold()

        return [
            expense
            for expense in self.expenses
            if expense["category"].casefold() == category
        ]

    def search_expenses(self, keyword: str) -> list[dict]:
        keyword = keyword.strip().casefold()

        return [
            expense
            for expense in self.expenses
            if keyword in expense["category"].casefold()
            or keyword in expense["description"].casefold()
        ]

    def calculate_total(self, expenses: list[dict] | None = None) -> float:
        selected_expenses = self.expenses if expenses is None else expenses

        return round(
            sum(expense["amount"] for expense in selected_expenses),
            2,
        )

    def get_category_summary(self) -> dict[str, float]:
        summary: dict[str, float] = {}

        for expense in self.expenses:
            category = expense["category"]
            summary[category] = summary.get(category, 0) + expense["amount"]

        return {
            category: round(total, 2)
            for category, total in sorted(summary.items())
        }