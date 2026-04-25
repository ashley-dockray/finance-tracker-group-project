import json
import core_classes
from core_classes import Income, Expense, RecurringBill

transactions = []

def add_transaction():
    id = input("Enter transaction id: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    source = input("Enter source: ")
    taxable = input("Enter true or false for taxable or not: ")
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
    category = input("Enter category: ") #Income, Expense, RecurringBill, Transaction
    while not valid:
        importance = input("Enter importance, (need or want): ").lower()
        if importance != "need" or "want":
            print("Not a valid input, needs to be need or want ")
        else:
            valid = True
    transaction = Expense(id, datetime.now(), amount, description, category, importance)
    transactions.append(transaction)

def view_transactions():
    if not transactions:
        print("No transactions found.")
        return
    for transaction in transactions:
        print(transaction.display_details())

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

    print("\nINCOME")
    if not income_list:
        print("No income recorded.")
    else:
        for transaction in income_list:
            print(transaction.display_details())

    print("\nEXPENSES BY CATEGORY")
    if not expense_categories:
        print("No expenses ")
    else:
        for category, items in expense_categories.items():
            print(f"\nCategory: {category}")
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
                "next_due": transaction.get_next_due()
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
                transaction = Income(
                    transaction_data["id"], date, transaction_data["amount"],
                    transaction_data["description"], transaction_data["source"],
                    transaction_data["is_taxable"]
                )

            elif transaction_data["type"] == "Expense":
                transaction = Expense(
                    transaction_data["id"], date, transaction_data["amount"],
                    transaction_data["description"], transaction_data["category"],
                    transaction_data["importance"]
                )

            elif transaction_data["type"] == "RecurringBill":
                transaction = RecurringBill(
                    transaction_data["id"], date, transaction_data["amount"],
                    transaction_data["description"], transaction_data["frequency"],
                    transaction_data["next_due"]
                )

            else:
                transaction = Transaction(
                    transaction_data["id"], date,
                    transaction_data["amount"], transaction_data["description"]
                )

            transactions.append(transaction)

    except FileNotFoundError:
        transactions = []
