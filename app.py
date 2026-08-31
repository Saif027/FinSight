import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify, session
from database.db import users, expenses
import bcrypt
import datetime

from ml_models.predictor import predict_expense
from ml_models.classifier import classify_spending
from ml_models.anomaly import detect_anomaly

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup_page")
def signup_page():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/signup", methods=["POST"])
def signup():

    data = request.json

    username=data["username"]
    password=data["password"]

    if users.find_one({"username":username}):
        return jsonify({"message":"User already exists"})

    hashed_pw=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    users.insert_one({
        "username":username,
        "password":hashed_pw
    })

    return jsonify({"message":"Signup successful"})

@app.route("/login", methods=["POST"])
def login():

    data=request.json

    user=users.find_one({"username":data["username"]})

    if not user:
        return jsonify({"message":"User not found"})

    if bcrypt.checkpw(data["password"].encode(),user["password"]):

        session["user"] = data["username"]

        return jsonify({"message":"success"})

    return jsonify({"message":"invalid"})

@app.route("/add_expense", methods=["POST"])
def add_expense():

    data = request.json

    expenses.insert_one({

        "user": session["user"],
        "category": data["category"],
        "amount": float(data["amount"]),
        "date": data["date"]

    })

    return jsonify({"message":"expense saved"})

@app.route("/get_expenses")
def get_expenses():

    data=list(expenses.find({"user":session["user"]},{"_id":0}))

    return jsonify(data)
@app.route("/monthly_expenses")
def monthly_expenses():

    data=list(expenses.find({"user":session["user"]},{"_id":0}))

    monthly={}

    for d in data:

        month=d["date"][:7]

        monthly[month]=monthly.get(month,0)+d["amount"]

    return jsonify(monthly)


@app.route("/predict")
def predict():

    data=list(expenses.find({"user":session["user"]}).sort("date",1))

    amounts=[x["amount"] for x in data if "amount" in x]

    prediction=predict_expense(amounts)

    return jsonify({"prediction":prediction})

@app.route("/classify", methods=["POST"])
def classify():

    data = request.json

    income = float(data["income"])
    expense = float(data["expense"])

    result = classify_spending(income,expense)

    return jsonify({"classification":result})


@app.route("/anomaly")
def anomaly():

    user = session["user"]

    # get all expenses sorted by date
    data = list(expenses.find({"user": user}).sort("date", -1))

    if not data:
        return jsonify({"anomaly": None})

    # latest month from newest expense
    latest_month = data[0]["date"][:7]

    # filter expenses only for that month
    month_data = [d for d in data if d["date"].startswith(latest_month)]

    amounts = [x["amount"] for x in month_data]

    if len(amounts) < 5:
        return jsonify({"anomaly": None})

    result = detect_anomaly(amounts)

    for i, r in enumerate(result):
        if r == -1:
            return jsonify({
                "category": month_data[i]["category"],
                "amount": month_data[i]["amount"],
                "month": latest_month
            })

    return jsonify({"anomaly": None})

@app.route("/logout")
def logout():

    session.clear()

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)