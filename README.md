# Expense Tracker CLI

A menu-driven command-line application built with Python to record, manage, search, and summarize daily expenses. Data is stored locally in JSON format and remains available between application sessions.

## Features

- Add expenses with amount, category, description, and date
- Automatically generate a unique ID for each expense
- View all expenses in a formatted table
- Edit existing expenses using their ID
- Delete expenses with confirmation
- Filter expenses by category
- Search using category or description keywords
- Calculate overall and filtered totals
- Generate category-wise expense summaries
- Validate user input and handle invalid data safely
- Persist expense data using JSON

## Technologies and Concepts

- Python
- Object-Oriented Programming
- JSON serialization
- File handling
- Exception handling
- Input validation
- CRUD operations
- Modular programming
- Unit testing
- Git and GitHub

## Project Structure

```text
expense_tracker/
├── main.py
├── expense_tracker.py
├── tests/
│   ├── __init__.py
│   └── test_expense_tracker.py
├── .gitignore
└── README.md
```

The `expenses.json` file is automatically created locally when the first expense is added. It is excluded from Git to prevent personal expense data from being committed.

## Requirements

- Python 3.10 or later
- No external packages required

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/Dhuvaraha/python-expense-tracker.git
```

2. Navigate to the project directory:

```bash
cd python-expense-tracker
```

3. Run the application:

```bash
python main.py
```

## Running the Tests

Run all automated unit tests using:

```bash
python -m unittest discover -s tests -v
```

The test suite verifies:

- Adding expenses
- Invalid amount handling
- Editing expenses
- Deleting expenses
- Category filtering
- Keyword search
- Total and category summary calculations
- JSON persistence between sessions

## Future Improvements

- Date-range filtering
- CSV report export
- SQLite database support
- FastAPI-based REST API

## Author

Dhuvaraha Prasath A
