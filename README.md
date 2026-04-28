# FinTrack - Personal Finance & Budget Forecaster
A command-line budgeting application built in Python for CIS1703 Programming 2 Group Project.

## Requirements
- Python 3.10 or above
- No external libraries required - only built-in Python modules are used

## How to Run
1. Download or clone the project folder
2. Open a terminal and navigate to the project folder
3. Run the following command:

   python CLI_interface.py

## File Structure
- CLI_interface.py        - Main entry point, run this to start the app
- core_classes.py         - Base Transaction class and all subclasses (Income, Expense, RecurringBill)
- transaction_manager.py  - Handles saving, loading and managing transactions
- balance_forecaster.py   - 30-day forecast, budget alerts and needs vs wants report
- transactions.json       - Created automatically when you first save data

## How to Use
- Option 1:  Add a new income
- Option 2:  Add a new expense
- Option 3:  View all recorded transactions
- Option 4:  View spending grouped by category
- Option 5:  Check 30-day balance forecast
- Option 6:  Show spending chart
- Option 7:  Add a recurring bill
- Option 8:  Needs vs Wants report
- Option 9:  Budget alert check
- Option 10: Save and exit

## Notes
- Data is saved automatically when adding transactions and on exit
- If transactions.json does not exist it will be created automatically on first save
- All file paths are relative so the app will work from any machine
