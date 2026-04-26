# interface
# FinTrack - CLI interface
# My section(part 4): menu system, user flow, validation and spending visualisation


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
    print("7. Save and exit")

def get_fintrack_menu_choice():
    valid_choices = ["1", "2", "3", "4", "5", "6", "7"]

    while True:
        user_choice = input("\nChoose an option from 1 to 7: ").strip()
        if user_choice in valid_choices:
            return user_choice
        print("That option is not on the menu. Please enter a number from 1 to 7.")

def return_to_menu():
    input("\nPress Enter when you are ready to go back to the main menu...")

# checks user input so the app does not crash
def get_text_input(prompt, error_message):
    while True:
        user_input = input(prompt).strip()
        if user_input != "":
            return user_input
        print(error_message)


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

# screen / UI functions
def open_all_transactions_screen():
    print_fintrack_header("All Transactions")
    print("This page will show all income and expense records in one place.")
    print("This will show the saved income and expenses once it is linked up.")
    return_to_menu()


def open_category_summary_screen():
    print_fintrack_header("Spending by Category")
    print("This page will group expenses into categories so the user can see where money is going.")
    print("The final version will use the real expense data from the transaction manager.")
    return_to_menu()


def open_forecast_screen():
    print_fintrack_header("30-Day Forecast")
    print("This page will show whether the user is likely to stay financially safe over the next month.")
    print("The final version will use recurring bills and the balance forecast logic.")
    return_to_menu()

# simple text-based bar chart that gives a quick visual summary of the user's spending across different categories. 
def open_spending_chart_screen():
    print_fintrack_header("Spending Chart")

    # Temporary test data so the interface can be tested before backend integration.
    example_spending = {
        "Food": 120,
        "Travel": 60,
        "Shopping": 35,
        "Bills": 180,
        "Social": 75
    }
    print("Quick visual summary of spending:\n")
    
    for category, amount in example_spending.items():
        bar_length = int(amount / 10)
        spending_bar = "#" * bar_length
        print(f"{category:12} | {spending_bar:<20} £{amount:.2f}")
    print("\nEach # represents roughly £10.")
    return_to_menu()

# The open_income_screen and open_expense_screen functions will have more detailed prompts and validation to ensure the user enters the correct information. They will also print a summary of the recorded transaction before returning to the menu.
def open_income_screen():
    print_fintrack_header("Add Income")
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
    print("\nIncome recorded successfully.")
    print(f"{description} | £{amount:.2f} | {source} | Taxable: {taxable}")
    return_to_menu()

def open_expense_screen():
    print_fintrack_header("Add Expense")
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
    print("\nExpense recorded successfully.")
    print(f"{description} | £{amount:.2f} | {category} | Importance: {importance}")
    return_to_menu()

# main loop of the application, showing the menu and responding to user choices until they choose to exit. 
def run_fintrack_interface():
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
            print_fintrack_header("Exit")
            print("FinTrack is closing now.")
            print("Final version will save the latest data before exiting.")
            print("Goodbye.")
            app_is_running = False

if __name__ == "__main__":
    run_fintrack_interface()

