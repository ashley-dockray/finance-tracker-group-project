import json
from datetime import datetime, timedelta
from transaction_manager import view_transactions

def Bill_filter():
    jason_file_data = view_transactions()
    filtered_data = []

    current_date = datetime.now().date()
    due_date = current_date + timedelta(days=30)

    for data in jason_file_data:
        if type(data).__name__ == "RecurringBill": #checks if the object is a recurring bill
            next_due = data.get_next_due()
            if isinstance(next_due, datetime): # this gets the next due date and converts it into an actual date format
                next_due = next_due.date()
            if current_date <= next_due <= due_date:#this checks that the date is within the next 30 days
                filtered_data.append(data)

    return filtered_data
