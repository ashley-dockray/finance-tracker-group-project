#few changes - in order for the view transactions fucntion to work with my interface make it just return transactions 


import json
from core_classes import Income, Expense, RecurringBill, Transaction
from datetime import datetime
transactions = []

def add_transaction():
    id = input("Enter transaction id: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    source = input("Enter source: ")
    taxable_input = input("Enter true or false for taxable or not: ").lower()
    taxable = taxable_input == "true"
    transaction = Income(id, datetime.now(), amount, description, source, taxable)
    transactions.append(transaction)

def add_expense():
    valid = False
    while not valid:
        try:
            id = int(input("Enter expense id: "))
            valid = True
        except:
            print("not a valid id ")
    valid = False
    while not valid:
        try:
            amount = float(input("Enter amount: "))
            valid = True
        except:
            print("Not a valid amount ")
    valid = False
    description = input("Enter description: ")
    category = input("Enter category: ")
    while not valid:
        importance = input("Enter importance, (need or want): ").lower()
        if importance not in ["need", "want"]:
            print("Not a valid input, needs to be need or want ")
        else:
            valid = True
    transaction = Expense(id, datetime.now(), amount, description, category, importance)
    transactions.append(transaction)

def add_recurring_bill():
    valid = False
    while not valid:
        try:
            id = input("Enter bill id: ")
            if id == "":
                raise ValueError
            valid = True
        except:
            print("Not a valid id")

    valid = False
    while not valid:
        try:
            amount = float(input("Enter amount: "))
            if amount < 0:
                raise ValueError
            valid = True
        except:
            print("Not a valid amount")

    description = input("Enter description: ")
    frequency = input("Enter frequency: ")
    valid = False
    while not valid:
        try:
            next_due_input = input("Enter next due date (YYYY-MM-DD): ")
            next_due = datetime.fromisoformat(next_due_input)
            valid = True
        except:
            print("Invalid date format. Use YYYY-MM-DD")
    transaction = RecurringBill(id, datetime.now(), amount, description, frequency, next_due)
    transactions.append(transaction)

# def view_transactions():
#     if not transactions:
#         print("No transactions found.")
#         return
#     for transaction in transactions:
#         print(transaction.display_details())
# so this would be removed for: 
def view_transactions(): 
    return transactions 
    
def categorise():
    income_list = []
    expense_categories = {}
    for transaction in transactions:
        transaction_type = type(transaction).__name__

        if transaction_type == "Income":
            income_list.append(transaction)

        elif transaction_type == "Expense":
            category = transaction.get_category()

            if category not in expense_categories:
                expense_categories[category] = []
            expense_categories[category].append(transaction)

    print("INCOME")
    if not income_list:
        print("No income recorded.")
    else:
        for transaction in income_list:
            print(transaction.display_details())

    print("EXPENSES BY CATEGORY")
    if not expense_categories:
        print("No expenses ")
    else:
        for category, items in expense_categories.items():
            print(f"Category: {category}")
            for transaction in items:
                print(transaction.display_details())

def save(filename="transactions.json"):
    data = []
    for transaction in transactions:
        transaction_type = type(transaction).__name__

        if transaction_type == "Income":
            data.append({
                "type": "Income",
                "id": transaction.get_id(),
                "date": transaction._Transaction__date.isoformat(),
                "amount": transaction.get_amount(),
                "description": transaction.get_description(),
                "source": transaction.get_source(),
                "is_taxable": transaction.get_is_taxable()
            })

        elif transaction_type == "Expense":
            data.append({
                "type": "Expense",
                "id": transaction.get_id(),
                "date": transaction._Transaction__date.isoformat(),
                "amount": transaction.get_amount(),
                "description": transaction.get_description(),
                "category": transaction.get_category(),
                "importance": transaction.get_importance()
            })

        elif transaction_type == "RecurringBill":
            data.append({
                "type": "RecurringBill",
                "id": transaction.get_id(),
                "date": transaction._Transaction__date.isoformat(),
                "amount": transaction.get_amount(),
                "description": transaction.get_description(),
                "frequency": transaction.get_frequency(),
                "next_due": transaction.get_next_due().isoformat()
            })

        else:
            data.append({
                "type": "Transaction",
                "id": transaction.get_id(),
                "date": transaction._Transaction__date.isoformat(),
                "amount": transaction.get_amount(),
                "description": transaction.get_description()
            })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    
def load(filename="transactions.json"):
    global transactions
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        transactions = []
        for transaction_data in data:
            date = datetime.fromisoformat(transaction_data["date"])

            if transaction_data["type"] == "Income":
                transaction = Income(transaction_data["id"], date, transaction_data["amount"], transaction_data["description"], transaction_data["source"], transaction_data["is_taxable"])
            elif transaction_data["type"] == "Expense":
                transaction = Expense(transaction_data["id"], date, transaction_data["amount"], transaction_data["description"], transaction_data["category"], transaction_data["importance"])
            elif transaction_data["type"] == "RecurringBill":
                next_due = datetime.fromisoformat(transaction_data["next_due"])
                transaction = RecurringBill(transaction_data["id"], date, transaction_data["amount"], transaction_data["description"], transaction_data["frequency"], next_due)
            else:
                transaction = Transaction(transaction_data["id"], date, transaction_data["amount"], transaction_data["description"])

            transactions.append(transaction)

    except FileNotFoundError:
        transactions = []

load()
if __name__ == "__main__":
    exit = False
    while not exit:
        print("1. Add a transaction")
        print("2 Add an expense")
        print("3. Categorise ")
        print("4. view transactions ")
        print("5. save to JSON ")
        print("6. Add recurring bill")
        print("7. exit")
        choice = input("Enter numbered choice:")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            categorise()
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            save()
        elif choice == "6":
            add_recurring_bill()
        elif choice == "7":
            print("Thank you for using the transaction manager ") 
            exit = True
        else:
            print("not a valid input")
