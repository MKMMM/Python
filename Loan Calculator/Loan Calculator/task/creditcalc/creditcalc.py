import math
import argparse

def calculate_diff_payments(principal, periods, interest):
    total_payment = 0
    i = interest / (12 * 100)
    for month in range(1, periods+1):
        diff_payment = math.ceil(principal/periods + i * (principal - (principal*(month-1))/periods))
        total_payment += diff_payment
        print(f"Month {month}: payment is {diff_payment}")
    overpayment = total_payment - principal
    print(f"\nOverpayment = {overpayment}")

def calculate_annuity_payment(principal, periods, interest):
    i = interest / (12 * 100)
    annuity_payment = math.ceil(principal * (i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1))
    total_payment = annuity_payment * periods
    overpayment = total_payment - principal
    print(f"\nYour annuity payment = {annuity_payment}!")
    print(f"\nOverpayment = {overpayment}")

def calculate_principal(payment, periods, interest):
    i = interest / (12 * 100)
    principal = math.floor(payment / ((i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1)))
    total_payment = payment * periods
    overpayment = total_payment - principal
    print(f"\nYour loan principal = {principal}!")
    print(f"\nOverpayment = {overpayment}")

def calculate_periods(principal, payment, interest):
    i = interest / (12 * 100)
    periods = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
    years, months = divmod(periods, 12)
    if years == 1:
        year_str = "1 year"
    else:
        year_str = f"{years} years"
    if months == 1:
        month_str = "1 month"
    else:
        month_str = f"{months} months"
    if years == 0:
        print(f"\nIt will take {month_str} to repay this loan!")
    elif months == 0:
        print(f"\nIt will take {year_str} to repay this loan!")
    else:
        print(f"\nIt will take {year_str} and {month_str} to repay this loan!")
    total_payment = payment * periods
    overpayment = total_payment - principal
    print(f"\nOverpayment = {overpayment}")


parser = argparse.ArgumentParser(description='Loan calculator')
parser.add_argument('--type', choices=['annuity', 'diff'], help='Indicates the type of payment.')
parser.add_argument('--principal', type=int, help='Used for calculations of both types of payment.')
parser.add_argument('--periods', type=int, help='Denotes the number of months needed to repay the loan.')
parser.add_argument('--interest', type=float, help='Specified without a percent sign.')
parser.add_argument('--payment', type=float, help='The monthly payment amount.')

args = parser.parse_args()
if args.type == None or (args.type == 'diff' and args.payment != None):
    print('Incorrect parameters')
elif args.type == 'diff':
    calculate_diff_payments(args.principal, args.periods, args.interest)
elif args.type == 'annuity':
    if args.principal is not None and args.periods is not None and args.interest is not None:
        calculate_annuity_payment(args.principal, args.periods, args.interest)
    elif args.payment is not None and args.periods is not None and args.interest is not None:
        calculate_principal(args.payment, args.periods, args.interest)
    elif args.principal is not None and args.payment is not None and args.interest is not None:
        calculate_periods(args.principal, args.payment, args.interest)
    else:
        print('Incorrect parameters')
