import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# load dataset
data = pd.read_csv("dataset.csv")

print("\nDataset Loaded Successfully")

# select input columns
X = data[["income","food","rent","travel","bills","others"]]

# target column for prediction
y_expense = data["total_expense"]

# split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_expense,
    test_size=0.2,
    random_state=42
)

# Linear Regression model
model_lr = LinearRegression()

model_lr.fit(X_train, y_train)

pred_expense = model_lr.predict(X_test)

# evaluation metrics
mae = mean_absolute_error(y_test, pred_expense)
mse = mean_squared_error(y_test, pred_expense)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, pred_expense)

print("\nLINEAR REGRESSION RESULTS")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Accuracy:", r2)

# classification label
data["category"] = data["savings"].apply(
    lambda x: "Saver" if x > 20000 else "Overspender"
)

y_class = data["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_class,
    test_size=0.2,
    random_state=42
)

# Logistic Regression model
model_log = LogisticRegression()

model_log.fit(X_train, y_train)

pred_class = model_log.predict(X_test)

print("\nCLASSIFICATION RESULTS")

print("Accuracy:", accuracy_score(y_test, pred_class))

print(classification_report(y_test, pred_class))

# Isolation Forest model
model_iso = IsolationForest(contamination=0.05)

model_iso.fit(X)

pred_anomaly = model_iso.predict(X)

anomaly_count = list(pred_anomaly).count(-1)

print("\nANOMALY DETECTION")

print("Total anomalies detected:", anomaly_count)

# Isolation Forest model
model_iso = IsolationForest(contamination=0.05)

model_iso.fit(X)

pred_anomaly = model_iso.predict(X)

anomaly_count = list(pred_anomaly).count(-1)

print("\nANOMALY DETECTION")

print("Total anomalies detected:", anomaly_count)


# convert to percentage
r2_percent = r2 * 100

accuracy_percent = accuracy_score(y_test, pred_class) * 100

total_records = len(X)

anomaly_percent = (anomaly_count / total_records) * 100


print("\nFINAL EVALUATION METRICS (OUT OF 100)\n")

print("Linear Regression Accuracy (R2 Score):", round(r2_percent,2), "%")

print("Linear Regression RMSE:", round(rmse,2))

print("Classification Accuracy:", round(accuracy_percent,2), "%")

print("Anomaly Detection Rate:", round(anomaly_percent,2), "%")

print("Total anomalies detected:", anomaly_count, "out of", total_records)