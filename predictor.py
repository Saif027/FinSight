import numpy as np
from sklearn.linear_model import LinearRegression

def predict_expense(expenses):

    if len(expenses) < 2:
        return expenses[-1] if expenses else 0

    X = np.arange(len(expenses)).reshape(-1,1)
    y = np.array(expenses)

    model = LinearRegression()
    model.fit(X,y)

    next_month = [[len(expenses)]]

    prediction = model.predict(next_month)

    return round(float(prediction[0]),2)