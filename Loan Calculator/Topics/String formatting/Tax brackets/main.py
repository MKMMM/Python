income = int(input())

if 0 <= income <= 15527:
    percent = 0.0
elif 15527 < income <= 42707:
    percent = 0.15
elif 42708 <= income <= 132406:
    percent = 0.25
else:
    percent = 0.28

calculated_tax = round(income * percent)

print("The tax for {income} is {percent}%. That is {calculated_tax} dollars!".format(
    income=income, percent=round(percent * 100), calculated_tax=calculated_tax))
