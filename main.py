from datetime import datetime
from pathlib import Path

from expense_tracker import ExpenseTracker


DATA_FILE = Path(__file__).with_name("expenses.json")


def get_expense_id(prompt: str) -> int:
    while True:
        try:
            expense_id = int(input(prompt).strip())

            if expense_id <= 0:
                raise ValueError

            return expense_id

        except ValueError:
            print("Please enter a valid positive ID.")


def get_amount(
    prompt: str,
    allow_blank: bool = False,
) -> float | None:
    while True:
        value = input(prompt).strip()

        if allow_blank and not value:
            return None

        try:
            amount = float(value)

            if amount <= 0:
                raise ValueError

            return amount

        except ValueError:
            print("Please enter a valid amount greater than zero.")


def get_required_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_date(
    prompt: str,
    allow_blank: bool = True,
) -> str | None:
    while True:
        value = input(prompt).strip()

        if allow_blank and not value:
            return None

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value

        except ValueError:
            print("Please enter the date in YYYY-MM-DD format.")


def display_expenses(expenses: list[dict]) -> None:
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "-" * 82)
    print(
        f"{'ID':<6}"
        f"{'DATE':<16}"
        f"{'CATEGORY':<18}"
        f"{'AMOUNT':>12}  "
        f"DESCRIPTION"
    )
    print("-" * 82)

    for expense in expenses:
        print(
            f"{expense['id']:<6}"
            f"{expense['date']:<16}"
            f"{expense['category'][:16]:<18}"
            f"{expense['amount']:>12.2f}  "
            f"{expense['description']}"
        )

    print("-" * 82)


def add_expense(tracker: ExpenseTracker) -> None:
    print("\nADD EXPENSE")

    amount = get_amount("Enter amount: ")
    category = get_required_text("Enter category: ")
    description = input("Enter description: ").strip()
    expense_date = get_date(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    )

    expense = tracker.add_expense(
        amount=amount,
        category=category,
        description=description,
        expense_date=expense_date,
    )

    print(f"Expense added successfully with ID {expense['id']}.")


def view_expenses(tracker: ExpenseTracker) -> None:
    expenses = tracker.get_all_expenses()
    display_expenses(expenses)

    if expenses:
        print(f"Total expenses: Rs. {tracker.calculate_total():.2f}")


def edit_expense(tracker: ExpenseTracker) -> None:
    expenses = tracker.get_all_expenses()
    display_expenses(expenses)

    if not expenses:
        return

    expense_id = get_expense_id("Enter the expense ID to edit: ")
    expense = tracker.find_expense_by_id(expense_id)

    if expense is None:
        print("Expense ID not found.")
        return

    print("Press Enter to keep the existing value.")

    amount = get_amount(
        f"Amount [{expense['amount']:.2f}]: ",
        allow_blank=True,
    )
    category = input(
        f"Category [{expense['category']}]: "
    ).strip()
    description = input(
        f"Description [{expense['description']}]: "
    ).strip()
    expense_date = get_date(
        f"Date [{expense['date']}] (YYYY-MM-DD): "
    )

    updated = tracker.edit_expense(
        expense_id=expense_id,
        amount=amount,
        category=category or None,
        description=description or None,
        expense_date=expense_date,
    )

    if updated:
        print("Expense updated successfully.")


def delete_expense(tracker: ExpenseTracker) -> None:
    expenses = tracker.get_all_expenses()
    display_expenses(expenses)

    if not expenses:
        return

    expense_id = get_expense_id("Enter the expense ID to delete: ")
    expense = tracker.find_expense_by_id(expense_id)

    if expense is None:
        print("Expense ID not found.")
        return

    confirmation = input(
        f"Delete '{expense['description']}' for "
        f"Rs. {expense['amount']:.2f}? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion cancelled.")
        return

    tracker.delete_expense(expense_id)
    print("Expense deleted successfully.")


def filter_expenses(tracker: ExpenseTracker) -> None:
    category = get_required_text("Enter category to filter: ")
    expenses = tracker.filter_by_category(category)

    display_expenses(expenses)

    if expenses:
        total = tracker.calculate_total(expenses)
        print(f"Filtered total: Rs. {total:.2f}")


def search_expenses(tracker: ExpenseTracker) -> None:
    keyword = get_required_text(
        "Enter category or description keyword: "
    )
    expenses = tracker.search_expenses(keyword)

    display_expenses(expenses)

    if expenses:
        total = tracker.calculate_total(expenses)
        print(f"Search result total: Rs. {total:.2f}")


def show_category_summary(tracker: ExpenseTracker) -> None:
    summary = tracker.get_category_summary()

    if not summary:
        print("\nNo expenses found.")
        return

    print("\nCATEGORY-WISE SUMMARY")
    print("-" * 36)

    for category, total in summary.items():
        print(f"{category:<22} Rs. {total:>10.2f}")

    print("-" * 36)
    print(f"{'Overall total':<22} Rs. {tracker.calculate_total():>10.2f}")


def show_menu() -> None:
    print(
        "\nEXPENSE TRACKER\n"
        "1. Add expense\n"
        "2. View all expenses\n"
        "3. Edit expense\n"
        "4. Delete expense\n"
        "5. Filter by category\n"
        "6. Search expenses\n"
        "7. Category-wise summary\n"
        "8. Exit"
    )


def main() -> None:
    tracker = ExpenseTracker(str(DATA_FILE))

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        try:
            if choice == "1":
                add_expense(tracker)
            elif choice == "2":
                view_expenses(tracker)
            elif choice == "3":
                edit_expense(tracker)
            elif choice == "4":
                delete_expense(tracker)
            elif choice == "5":
                filter_expenses(tracker)
            elif choice == "6":
                search_expenses(tracker)
            elif choice == "7":
                show_category_summary(tracker)
            elif choice == "8":
                print("Exiting Expense Tracker.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")

        except OSError as error:
            print(f"Unable to access the expense data file: {error}")
        except ValueError as error:
            print(f"Invalid data: {error}")


if __name__ == "__main__":
    main()