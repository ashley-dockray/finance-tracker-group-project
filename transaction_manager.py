#import libraries like json for saving and loading, datetime and linking to the OOP file
import json
from core_classes import Income, Expense, RecurringBill, Transaction
from datetime import datetime
#transactions stored as a list, made as a constant at the top of the code
transactions = []

def add_income():
    valid = False
    #my code uses the same sort of error handling throughout, I set valid equal to False and do a while loop to ensure that it keeps asking the user for an answer even if they input the wrong data type
    valid = False
    while not valid:
        try:
            transaction_id = int(input("Enter transaction id: ")) #converts input to an integer using int, if it fails, try and except block prevents it from crashing
            if transaction_id <= 0: #makes sure the user enters an id above zero, otherwise raises an error
                raise ValueError
            valid = True #breaks the while loop
        except ValueError: #if a value error is raised then it will run the code below and restart the loop
            print("Not a valid id ")
    valid = False
    while not valid:
        try:
            amount = float(input("Enter amount: ")) #amount must be a float
            if amount < 0: #amount must be greater than zero
                raise ValueError
            valid = True
        except ValueError:
            print("Not a valid amount ")
    description = input("Enter description: ")
    source = input("Enter source: ")
    valid = False
    while not valid:
        taxable_input = input("is it taxable (enter true or false): ").lower() #converts users answer to lowercase
        if taxable_input in ["true", "false"]: #checks if the user inputted true or false
            taxable = taxable_input == "true" #converts it to a boolean by a comparison if they enter True as it will be true, and false if they entered false
            valid = True
        else:
            print("Please enter true or false ")
    transaction = Income(transaction_id, datetime.now(), amount, description, source, taxable) #calls Income class from the OOP core classes
    transactions.append(transaction) #adds all of the inputs into the transactions list
    print("transaction added ")

def add_expense():
    valid = False
    while not valid:
        try:
            id = int(input("Enter expense id: "))
            if id <= 0: #makes sure the user enters an id above zero, otherwise raises an error
                raise ValueError
            valid = True
        except ValueError:
            print("not a valid id ")
    valid = False
    while not valid:
        try:
            amount = float(input("Enter amount: "))
            if amount < 0: 
                raise ValueError
            valid = True
        except ValueError:
            print("Not a valid amount ")
    valid = False
    description = input("Enter description: ")
    category = input("Enter category: ")
    while not valid:
        importance = input("Enter importance, (need or want): ").lower()
        if importance not in ["need", "want"]: #same idea as with the taxable input, checks if the user inputted need or want and doesnt accept anything else
            print("Not a valid input, has to be either need or want ")
        else:
            valid = True
    transaction = Expense(id, datetime.now(), amount, description, category, importance) #calls Expense class from the OOP core classes
    transactions.append(transaction) #adds the inputs into the list with other transactions
    print("expense added ")

def add_recurring_bill():
    valid = False
    while not valid:
        try:
            id = int(input("Enter bill id: "))
            if id <= 0: 
                raise ValueError
            valid = True
        except ValueError:
            print("not a valid id ")

    valid = False
    while not valid:
        try:
            amount = float(input("Enter amount: "))
            if amount < 0:
                raise ValueError
            valid = True
        except:
            print("Not a valid amount ")

    description = input("Enter description: ")
    frequency = input("Enter frequency: ")
    valid = False
    while not valid:
        try:
            next_due_input = input("Enter next due date (YYYY-MM-DD): ")
            next_due = datetime.fromisoformat(next_due_input) #fromisoformat ensures its converted into YYYY-MM-DD, which is ISO format, and if its not it wont accept it
            valid = True
        except:
            print("Invalid date format, Use YYYY-MM-DD ")
    transaction = RecurringBill(id, datetime.now(), amount, description, frequency, next_due) #calls RecuringBill from OOP
    transactions.append(transaction)

# extra code that needed to be changed for the UI section
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
    income_list = [] #list of income objects
    expense_categories = {} #dictionary of categories
    for transaction in transactions: #goes through each transaction one by one
        transaction_type = type(transaction).__name__ #gets the class name to compare in if statements
        if transaction_type == "Income":
            income_list.append(transaction) #adds all income objects into a list
        elif transaction_type == "Expense":
            category = transaction.get_category() #uses get_category from OOP to get the category type
            if category not in expense_categories:
                expense_categories[category] = []
            expense_categories[category].append(transaction)

    print("INCOME") #acts as a heading, same with the other print
    if not income_list:
        print("No income recorded ") #in case no incomes exist prints this to user
    else:
        for transaction in income_list:
            print(transaction.display_details())

    print("EXPENSES BY CATEGORY")
    if not expense_categories:
        print("No expenses ") #in case no expenses exist prints no expenses
    else:
        for category, items in expense_categories.items(): #loops through dictionary 
            print(f"Category: {category}") #prints each category one by one when looping
            for transaction in items:
                print(transaction.display_details()) #then prints the item details

def save(filename="transactions.json"):
    data = [] #used to store the list of dictionaries about to be made
    for transaction in transactions:
        transaction_type = type(transaction).__name__ #gets the transaction type in order to compared
        #since JSON cant store objects, each of the different transaction types need to be converted into dictionaries
        #so the code below checks the type of transaction, then gets each bit of information and converts it into a dictionary format
        if transaction_type == "Income":
            data.append({
                "type": "Income",
                "id": transaction.get_id(),
                "date": transaction._Transaction__date.isoformat(), #isoformat makes sure that all of the dates are strings instead of objects so they can actually be stored
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

    with open(filename, "w") as f: #opens the transactions.json file in write mode
        json.dump(data, f, indent=4) #writes all of the data into the file, with an indent to make it more readable
    
def load(filename="transactions.json"):
    global transactions #makes transactions a global variable so it is being modified inside this function and needs to be used outside of it
    try:
        with open(filename, "r") as f: #opens the file in read mode
            data = json.load(f) #loads the transaction data and converts it into a list of dictionaries from json
        transactions = [] #resets the transactions list so any old data is deleted
        #all of this code just converts all of the strings back into objects for the OOP to work, by retrieving all of the information in each class
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

            transactions.append(transaction) #adds all of the converted data into the transactions list again

    except FileNotFoundError: #used in case the filename isnt found, just resets transactions
        transactions = []

#own menu for testing my functions
#load()
#if __name__ == "__main__":
#    exit = False
#    while not exit:
#        print("1. Add an income ")
#        print("2 Add an expense ")
#        print("3. Categorise ")
#        print("4. view transactions ")
#        print("5. save to JSON ")
#        print("6. Add recurring bill")
#        print("7. exit ")
#        choice = input("Enter numbered choice: ")
#        if choice == "1":
#            add_income()
#        elif choice == "2":
#            add_expense()
#        elif choice == "3":
#            categorise()
#        elif choice == "4":
#            view_transactions()
#        elif choice == "5":
#            save()
#        elif choice == "6":
#            add_recurring_bill()
#        elif choice == "7":
#            print("Thank you for using the transaction manager ") 
#            exit = True
#        else:
#            print("not a valid input")
