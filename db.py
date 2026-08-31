# from pymongo import MongoClient

# client = MongoClient("mongodb+srv://expense_ai:Saif84321@cluster0.kjep3w5.mongodb.net/expense_ai?retryWrites=true&w=majority")

# db = client["expense_ai"]

# users = db["users"]
# expenses = db["expenses"]

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

except Exception as e:
    print("MongoDB connection failed:")
    print(e)

db = client["expense_ai"]

users = db["users"]

expenses = db["expenses"]