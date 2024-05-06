#!/usr/bin/env python3

'''
OPS445 Assignment 1 - Fall 2023
Program: assignment1.py 
The python code in this file is original work written by Lukas Millar.
No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''

'''
Author: Lukas Millar
Description: This script has multiple functions which accept user input and process it to return a correct day in the future or past, based on the arguments the user provided.
'''
# we can work only with the sys function
import sys

def day_of_week(date: str) -> str:
    '''
    day_of_week() -> day of the week as string

    Based on the algorithm by Tomohiko Sakamoto
    '''
    day, month, year = (int(x) for x in date.split('/'))
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] 
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + day) % 7
    return days[num]

def leap_year(year: int) -> bool:
    '''
    leap_year() -> true if year is a leap year, false if not

    Return true if the year is a leap year
    '''
    lyear = year % 4       # test if year is divisible by 4
    if lyear == 0:
        leap_flag = True   # this is a leap year
    else:
        leap_flag = False  # this is not a leap year

    lyear = year % 100
    if lyear == 0:
        leap_flag = False  # this is not a leap year

    lyear = year % 400
    if lyear == 0:
        leap_flag = True   # this is a leap year
    return leap_flag

def mon_max(month:int, year:int) -> int:
    '''
    mon_max() -> maximum number of days in a given month as int

    Returns the maximum day for a given month. Includes leap year check
    '''
    leap_flag = leap_year(year) # leap year check

    mon_dict= {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    if month == 2 and leap_flag: # February has 29 days in leap year
        mon_max = 29
    else:
        mon_max = mon_dict[month]
    return mon_max

def after(date: str) -> str: 
    '''
    after() -> date for next day in DD/MM/YYYY string format

    Return the date for the next day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    
    day, mon, year = (int(x) for x in date.split('/')) # split date to day month and year
    day += 1  # next day

    mon_max_var = mon_max(mon, year)
    
    if day > mon_max_var: # checking if we crossed to next month
        mon += 1
        if mon > 12: # checking if we crossed to next year
            year += 1
            mon = 1
        day = 1  # if tmp_day > this month's max, reset to 1 
    return f"{day:02}/{mon:02}/{year}"

def before(date: str) -> str:
    '''
    before() -> date for previous day in DD/MM/YYYY string format

    Returns previous day's date as DD/MM/YYYY for the given date. 
    '''

    day, mon, year = (int(x) for x in date.split('/')) # split date to day month and year
    day -= 1  # previous day
    
    if day == 0: # checking if we crossed to previous month  
        mon -= 1
        if mon < 1: # checking if we crossed to previous year
            year -= 1
            mon = 12
        mon_max_var = mon_max(mon, year)
        day = mon_max_var  # if tmp_day < 1, set to previous month max

    return f"{day:02}/{mon:02}/{year}"

def usage():
    '''
    Print a usage message to the user
    '''
    print('This script returns previous or future date, based on the number given.\n')
    print("Usage: " + str(sys.argv[0]) + " DD/MM/YYYY NN\n")
    print('You have entered: ' + sys.argv[1] + ' as a date. Make sure it is a valid date in the right format.')
    print('You have entered: ' + sys.argv[2] + ' as a number. This must be a valid integer (positive or negative)')

def valid_date(date: str) -> bool:
    '''
    valid_date() -> true if string is a valid date, false if not

    Check validity of date
    '''
    try: 
        day, mon, year = ((int(x)) for x in date.split('/')) # split date to day month and year
        if mon < 1 or mon > 12: # check if month is valid
            return False
        
        if day < 1 or day > mon_max(mon, year): # check if day is valid
            return False

        return True

    except:
        return False

def day_iter(start_date: str, num: int) -> str:
    '''
    day_iter() -> date num days before or after start_date as string in DD/MM/YYYY format

    Iterates from start date by num to return end date in DD/MM/YYYY
    '''
    new_date = start_date
    if num < 0: # going backwards
        # we need to use absolute value of num, because we can't iterate with negative integers.  
        for i in range(abs(num)):
            new_date = before(new_date)

    elif num > 0: # going forwards
        for i in range(num):
            new_date = after(new_date)
    
    return new_date

if __name__ == "__main__":
    if len(sys.argv) != 3: # check length of arguments
        usage()

    elif valid_date(sys.argv[1]):    # check first arg is a valid date
        try: 
            number = int(sys.argv[2])  # check that second arg is a valid number (+/-)
            result_date = day_iter(sys.argv[1], number) # call day_iter function to get end date, save to result_date
            print(f'The end date is {day_of_week(result_date)}, {result_date}.') # print result
        except: 
            usage()
    else: 
        usage() # if user put wrong date, return usage

