import json

try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
                
except (FileNotFoundError, json.JSONDecodeError):
    expenses = []


    
def add_expense():
    amount = int(input("Enter the amount:"))
    category = input("Enter the category:").strip().title() #to convert the category to uppercase and remove any leading/trailing whitespace
    description = input("Enter description:").strip()

    expense = {
        "amount" : amount ,
        "category" : category ,
        "description" : description
    }

    expenses.append(expense)
    save_expenses()

    print("Expense added successfully!")
    print("Current expenses:", expenses)
    


def view_expenses():
    
    if not expenses:
        print("No expenses found.")
        return
    print("\nAll expenses:")

    for expense in expenses:
        print(f"Amount: {expense['amount']}")
        print(f"Category: {expense['category']}")
        print(f"Description: {expense['description']}")

def view_total_expenses():
    
    total = 0

    for expense in expenses:
        total += expense["amount"]
    print("\nTotal expenses:", total) 

def delete_expense():

    n = int(input("Enter the number of expenses to delete: "))

    if 1<= n <= len(expenses):
        expenses.pop(n-1)
        save_expenses()
        
        print(f"Expense at index {n} deleted successfully.")

    else:
        print(f"Invalid index. Please enter a valid index from 1 to {len(expenses)}.")  


def summary_by_category():
    
    category_totals = {}
    
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
            
    print("\nSummary of Expenses by Category:")
    for category, total in category_totals.items():
        print(f"{category}: {total}")
        
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def exit_program():
    print("Exiting the program.")
    

while True:
    print("\nExpense Tracker Menu:")
    print("1. Add Expense:")
    print("2. View Expenses:")
    print("3. View Total Expenses:")
    print("4. Delete Expense:")
    print("5. Summary of Expenses by Category:")
    print("6. Exit")
    
    choice = input("Enter your choice (1/2/3/4/5/6):").strip()
    
    if choice == "1":
        add_expense()
    
    elif choice == "2":
        view_expenses()
        
    elif choice == "3":
        view_total_expenses()
        
    elif choice == "4":
        delete_expense()
    
    elif choice == "5":
        summary_by_category()
        
    elif choice == "6":
        exit_program()
        break
    else:
        print("Invalid choice. Please enter 1-6.")