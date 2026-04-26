import json
from datetime import datetime, timedelta
from transaction_manager import transactions
from core_classes import Income, Expense, RecurringBill

def Bill_filter(): # this filteres the dat to make sure we get only the bills from the saved data
    jason_file_data = transactions
    filtered_data = []

    current_date = datetime.now().date() # we use the date as one form of filtering the data, ensuring all the bills are in date
    due_date = current_date + timedelta(days=30)

    for data in jason_file_data: 
        if isinstance(data, RecurringBill): #checks if the object is a recurring bill
            next_due = data.get_next_due()
            if isinstance(next_due, datetime): # this gets the next due date and converts it into an actual date format
                next_due = next_due.date()
            if current_date <= next_due <= due_date:#this checks that the date is within the next 30 days
                filtered_data.append(data)

    return filtered_data

def balance_calculator(): # knowing the current ballance is important so this function works it out based on expenses and income
    jason_file_data = transactions
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

    for day in range(30): #iterates through each day
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
    for date, balance in forecast_list: # iterates through a list
        if balance < safety_limit:
            return True # returns true if they are below the limit
    return False 

def needs_vs_wants_report(): # this function returns a report on the relationship between the needed and wanted expenses
    jason_file_data = transactions
    needs = []
    needs_count = 0
    wants = []
    wants_count = 0
    for data  in jason_file_data: 
        if isinstance(data, Expense): # it itterates through each bit of data and ignores anything which isnt an expense 
            importance = data.get_importance()
            if importance == "need": # it seperates the needs and the wants keeping a running tally of the overall spendage
                needs.append(data)
                needs_count  += data.get_amount()
            elif importance == "want":
                wants.append(data)  
                wants_count += data.get_amount()

    total = needs_count + wants_count
    if total > 0 :   #  it also works out the precentage of of the needs spendage against the wants
        needs_percent = (needs_count / total) * 100
        wants_percent = (wants_count / total) * 100
    else:
        needs_percent = wants_percent = 0
    return {"needs_list": needs, "wants_list": wants, "needs_total": needs_count, "wants_total": wants_count, "needs_percentage": needs_percent, "wants_percentage": wants_percent}
        





    







