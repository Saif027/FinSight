import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Training dataset
data = {
    "income":[50000,40000,60000,45000,70000,30000,80000],
    "expense":[20000,35000,55000,30000,50000,28000,60000],
}

df = pd.DataFrame(data)

# Feature engineering
df["ratio"] = (df["income"] - df["expense"]) / df["income"]

# Labels
labels = []

for r in df["ratio"]:
    if r > 0.3:
        labels.append("Saver")
    elif r > 0.1:
        labels.append("Balanced")
    else:
        labels.append("Overspender")

# Train model
X = df[["income","expense","ratio"]]
y = labels

model = DecisionTreeClassifier()
model.fit(X,y)

# Prediction function
def classify_spending(income, expense):

    ratio = (income-expense)/income

    prediction = model.predict([[income,expense,ratio]])

    return prediction[0]