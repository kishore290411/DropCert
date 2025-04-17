from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace with the name of your Google Sheet
spreadsheet = client.open("UAE Feedback Heatmap")
sheet = spreadsheet.sheet1

# Route for rendering the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route for saving feedback data
@app.route("/save-feedback", methods=["POST"])
def save_feedback():
    data = request.get_json()

    # Optional: Add server-side fallback timestamp
    current_time = datetime.now().strftime("%I:%M %p")

    # Ensure required fields are available
    required_fields = ["delivery_id", "location", "emirate", "time", "issue_reported", "item_type", "overall_rating", "user_rating", "raw_feedback"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing fields in data"}), 400

    row = [
        data["delivery_id"],
        data["location"],
        data["emirate"],
        data.get("time", current_time),
        data["issue_reported"],
        data["item_type"],
        data["overall_rating"],
        data["user_rating"],
        data["raw_feedback"]
    ]

    sheet.append_row(row)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
