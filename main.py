from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import csv

def resultOfInvestment(contrib, rate, period=0.25, taxes=0):
    profit = contrib*rate*period/100
    return contrib + profit*(1-taxes/100)

def calculate(startDate, taxes=19):
    bonds = []
    with open('data/bonds.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            date = dt.strptime(row['Date'], "%m/%d/%Y").date()
            bonds.append((date, float(row['Open'])))
    bonds.reverse()
    startDateIdx = next((i for i, (k, _) in enumerate(bonds) if k >= startDate), None)
    cumulative_return = 100
    while startDateIdx is not None:
        cumulative_return = resultOfInvestment(cumulative_return, bonds[startDateIdx][1], taxes=taxes)
        new_invest_date = bonds[startDateIdx][0] + relativedelta(months=3)
        startDateIdx = next((i for i, (k, _) in enumerate(bonds) if k >= new_invest_date), None)
    return cumulative_return - 100


start_date = dt.fromisoformat(input("Input start date in YYYY-MM-DD format\n")).date()
print("Result is {}%".format(round(calculate(start_date),2)))