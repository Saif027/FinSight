import pandas as pd
import random

data = []

for i in range(120):

    income = random.randint(30000, 100000)

    food = random.randint(3000, 15000)
    rent = random.randint(8000, 30000)
    travel = random.randint(1000, 8000)
    bills = random.randint(2000, 10000)
    others = random.randint(1000, 7000)

    total_expense = food + rent + travel + bills + others

    savings = income - total_expense

    data.append([
        income,
        food,
        rent,
        travel,
        bills,
        others,
        total_expense,
        savings
    ])

columns = [
"income",
"food",
"rent",
"travel",
"bills",
"others",
"total_expense",
"savings"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("dataset.csv", index=False)

print("dataset.csv created successfully")