import json
from datetime import datetime, timedelta
from transaction_manager import view_transactions
from core_classes import Income, Expense, RecurringBill

def Bill_filter(): # this filteres the dat to make sure we get only the bills from the saved data
    jason_file_data = view_transactions()
    filtered_data = []

    current_date = datetime.now().date() # we use the date as one form of filtering the data, ensuring all the bills are in date
    due_date = current_date + timedelta(days=30)

    for data in jason_file_data: 
        if type(data).__name__ == "RecurringBill": #checks if the object is a recurring bill
            next_due = data.get_next_due()
            if isinstance(next_due, datetime): # this gets the next due date and converts it into an actual date format
                next_due = next_due.date()
            if current_date <= next_due <= due_date:#this checks that the date is within the next 30 days
                filtered_data.append(data)

    return filtered_data

def balance_calculator(): # knowing the current ballance is important so this function works it out based on expenses and income
    jason_file_data = view_transactions()
    balance= 0 
    for data in jason_file_data: # this for loop checks if the data is income or expense and decides weather or not to add or subtract the money from the ballance
        if isinstance(data, Income):
            balance += data.get_amount()
        elif isinstance(data, Expense):
            balance -= data.get_amount()
    return balance # and overall balance is returned


def forcast_over_next_30_days(): #  this runs through the next 30 days and keeps a running total of the balance over the next 30 days
    bills = Bill_filter()
    running_balance = balance_calculator() 
    current_date = datetime.now().date()
    forecast = []

    for day in range(31): #interates through each day
        date = current_date + timedelta(days=day)
        
        for bill in bills: #this checks the dates and works out weather or not the cost should be subtracted from the balance
            due = bill.get_next_due()
            if isinstance(due, datetime):
                due = due.date()
            if due == date:
                running_balance -= bill.get_amount() 
        
        forecast.append((date, running_balance)) #this list is to save the dates of the spendage over the next 30 days and how it impacts the balance
    
    return forecast

def alarm_system(forecast_list, safety_limit): # this is an alarm sytem function which compares each peice of data in the forcast list to a pre determined limmit
    for date, balance in forecast_list: #iterates through the list
        if balance < safety_limit: 
            return True #returns true is the they are below the limit
    return False 





