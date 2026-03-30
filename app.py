from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["Healthcare"]
collection = db["users"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        total_income = request.form.get("total_income")

        expenses = {}

        categories = {
            "utilities": "utilities_amount",
            "entertainment": "entertainment_amount",
            "school_fees": "school_fees_amount",
            "shopping": "shopping_amount",
            "healthcare": "healthcare_amount"
        }

        for category, amount_field in categories.items():
            if request.form.get(category):
                amount = request.form.get(amount_field)
                expenses[category] = float(amount) if amount else 0

        user_data = {
            "name": name,
            "age": int(age) if age else None,
            "gender": gender,
            "total_income": float(total_income) if total_income else 0,
            "expenses": expenses
        }

        collection.insert_one(user_data)

        return f"""
        <h3>Data saved successfully!</h3>
        <p><a href="/">Go back</a></p>
        """

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)