# interface
# FinTrack - CLI interface
# My section(part 4): menu system, user flow, validation and spending visualisation

from datetime import datetime
from core_classes import Income, Expense
import transaction_manager as tm
import balance_forecaster as bf

def print_fintrack_header(screen_name):
    print("\n" + "-" * 55)
    print(f" FinTrack | {screen_name}")
    print("-" * 55)

# main menu showing options for user to choose from.
def show_fintrack_menu():
    print_fintrack_header("Main Menu")
    print("1. Add a new income")
    print("2. Add a new expense")
    print("3. View all recorded transactions")
    print("4. View spending grouped by category")
    print("5. Check 30-day balance forecast")
    print("6. Show spending chart")
    print("7. Add recurring bill")              
    print("8. Needs vs Wants report")          
    print("9. Budget alert check") 
    print("10. Save and exit")
# menu choice function thats validates user input 
def get_fintrack_menu_choice():
    valid_choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    while True:
        user_choice = input("\nChoose an option from 1 to 10: ").strip()
        if user_choice in valid_choices:
            return user_choice
        print("That option is not on the menu. Please enter a number from 1 to 10.")

def return_to_menu():
    input("\nPress Enter when you are ready to go back to the main menu...")

# checks user input so the app does not crash
def get_text_input(prompt, error_message):
    while True:
        user_input = input(prompt).strip()
        if user_input != "":
            return user_input
        print(error_message)

# money input function ensuring that valid number amounts and is positive.
def get_money_input(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            amount = float(user_input)
            if amount > 0:
                return amount
            else:
                print("Please enter a positive amount.")
        except ValueError:
            print("Please type a number like 12.50.")

# yes or no function - boolean values 
def get_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        print("Please answer yes or no.")

# function will ask the user whether the expense is a "Need" or a "Want". 
def get_importance_level():
    while True:
        level = input("Is this a NEED or a WANT? ").strip().lower()
        if level in ["need", "n"]:
            return "Need"
        elif level in ["want", "w"]:
            return "Want"
        print("Please enter 'Need' or 'Want'.")
# It will return a list of dates and corresponding balances, which can be used to identify potential cash flow issues in advance.
def open_recurring_bill_screen():
    print_fintrack_header("Add Recurring Bill")

    transaction_id = get_text_input("Enter bill ID: ", "ID cannot be empty.")
    description = get_text_input("Enter description: ", "Cannot be empty.")
    amount = get_money_input("Enter amount: £")
    frequency = get_text_input("Enter frequency: ", "Cannot be empty.")

    next_due_input = get_text_input("Enter next due date (YYYY-MM-DD): ", "Invalid date.")

    try:
        next_due = datetime.fromisoformat(next_due_input)
    except:
        print("Invalid date format.")
        return_to_menu()
        return

    from core_classes import RecurringBill
    bill = RecurringBill(transaction_id, datetime.now(), amount, description, frequency, next_due)

    tm.transactions.append(bill)
    tm.save()

    print("Recurring bill added.")
    return_to_menu()
    
# This report will calculate the total amount spent on needs and wants, and the percentage of total expenses that each category represents.
def open_needs_wants_screen():
    print_fintrack_header("Needs vs Wants Report")

    report = bf.needs_vs_wants_report()

    print(f"Needs total: £{report['needs_total']:.2f}")
    print(f"Wants total: £{report['wants_total']:.2f}")
    print(f"Needs %: {report['needs_percentage']:.1f}%")
    print(f"Wants %: {report['wants_percentage']:.1f}%")

    return_to_menu()
# This function will use the 30-day forecast to check if the user's balance is projected to drop below a certain threshold, which they can set as a "safety limit".
def open_budget_alert_screen():
    print_fintrack_header("Budget Alert")

    forecast = bf.forcast_over_next_30_days()

    safety_limit = get_money_input("Enter minimum safe balance: £")

    alert = bf.alarm_system(forecast, safety_limit)

    if alert:
        print("WARNING: Your balance may drop below your limit.")
    else:
        print("Your balance looks safe.")

    return_to_menu()

# screen / UI functions
def open_all_transactions_screen():
    print_fintrack_header("All Transactions")
    transactions = tm.view_transactions()
    if not transactions:
        print("No transactions have been saved yet.")
    else:
        for transaction in transactions:
            print(transaction.display_details())
    return_to_menu()

#total amount in each category 
def open_category_summary_screen():
    print_fintrack_header("Spending by Category")
    transactions = tm.view_transactions()
    if not transactions:
        print("No transactions have been saved yet.")
        return_to_menu()
        return
    
    category_totals = {}
    for transaction in transactions:
        if isinstance(transaction, Expense):
            category = transaction.get_category()
            amount = transaction.get_amount()
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += amount

    if not category_totals:
        print("No expenses have been recorded yet.")
    else:
        print("Total spending by category:\n")
        for category, total in category_totals.items():
            print(f"{category:12} | £{total:.2f}")
    return_to_menu()

# forecast of next 30 days based on past and current transactions 
def open_forecast_screen():
    print_fintrack_header("30-Day Forecast")
    forecast = bf.forcast_over_next_30_days()

    if forecast is None or not forecast:
        print("No forecast data available.")
    else:
        for date, balance in forecast:
            print(f"{date} | £{balance:.2f}")
    return_to_menu()

# simple text-based bar chart that gives a quick visual summary of the user's spending across different categories. 
def open_spending_chart_screen():
    print_fintrack_header("Spending Chart")

    transactions = tm.view_transactions()
    category_totals = {}

    for transaction in transactions:
        if type(transaction).__name__ == "Expense":
            category = transaction.get_category()
            amount = transaction.get_amount()
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += amount

    if not category_totals:
        print("No expense data available for the spending chart.")
    else:
        print("Spending by category:\n")
        for category, total in category_totals.items():
            bar_length = int(total / 10)
            if bar_length == 0:
                bar_length = 1
            spending_bar = "*" * bar_length
            print(f"{category:12} | {spending_bar:<20} £{total:.2f}")
        print("\nEach * represents roughly £10.")
    return_to_menu()

# The open_income_screen and open_expense_screen functions will have more detailed prompts and validation to ensure the user enters the correct information. They will also print a summary of the recorded transaction before returning to the menu.
def open_income_screen():
    print_fintrack_header("Add Income")

    transaction_id = get_text_input(
        "Enter income ID: ",
        "Income ID cannot be empty. Example: INC001."
    )

    description = get_text_input(
        "Enter income description: ",
        "Description cannot be empty. Example: wages, student loan."
    )

    amount = get_money_input("Enter income amount: £")
    source = get_text_input(
        "Enter income source: ",
        "Source cannot be empty. Example: job, loan, family."
    )

    taxable = get_yes_or_no("Is this income taxable? (yes/no): ")
    income = Income(transaction_id, datetime.now(), amount, description, source, taxable)
    tm.transactions.append(income)
    tm.save()
    print("\nIncome saved successfully.")
    print(f"{transaction_id} | {description} | £{amount:.2f} | {source} | Taxable: {taxable}")
    return_to_menu()

# expense details 
def open_expense_screen():
    print_fintrack_header("Add Expense")
    transaction_id = get_text_input(
        "Enter expense ID: ",
        "Expense ID cannot be empty. Example: EXP001."
    )
    description = get_text_input(
        "Enter expense description: ",
        "Description cannot be empty. Example: food shop, rent, gym."
    )
    amount = get_money_input("Enter expense amount: £")
    category = get_text_input(
        "Enter category (e.g. Food, Travel, Bills): ",
        "Category cannot be empty."
    )

    importance = get_importance_level()
    expense = Expense(transaction_id, datetime.now(), amount, description, category, importance)
    tm.transactions.append(expense)
    tm.save()
    print("\nExpense saved successfully.")
    print(f"{transaction_id} | {description} | £{amount:.2f} | {category} | Importance: {importance}")
    return_to_menu()

# main loop of the application, showing the menu and responding to user choices until they choose to exit. 
def run_fintrack_interface():
    tm.load()
    app_is_running = True

    while app_is_running:
        show_fintrack_menu()
        user_choice = get_fintrack_menu_choice()
        if user_choice == "1":
            open_income_screen()
        elif user_choice == "2":
            open_expense_screen()
        elif user_choice == "3":
            open_all_transactions_screen()
        elif user_choice == "4":
            open_category_summary_screen()
        elif user_choice == "5":
            open_forecast_screen()
        elif user_choice == "6":
            open_spending_chart_screen()
        elif user_choice == "7":
            open_recurring_bill_screen()
        elif user_choice == "8":
            open_needs_wants_screen()
        elif user_choice == "9":
            open_budget_alert_screen()
        elif user_choice == "10":
                print_fintrack_header("Exit")
                tm.save()
                print("Latest FinTrack data has been saved.")
                print("Goodbye.")
                app_is_running = False
if __name__ == "__main__":
    run_fintrack_interface()

