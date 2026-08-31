import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomaly(data):

    X = np.array(data).reshape(-1,1)

    model = IsolationForest(contamination=0.15, random_state=42)

    model.fit(X)

    prediction = model.predict(X)

    return prediction