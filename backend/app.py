from flask import Flask, request, jsonify
from flask import send_file
import os
import datetime
import subprocess

app = Flask(__name__)

LOG_FILE = "logs/deploy.log"

#def log(message):
#    os.makedirs("logs", exist_ok=True)  # ensure folder exists
#   with open(LOG_FILE, "a") as f:
#       f.write(f"{datetime.datetime.now()} - {message}\n")

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {message}\n")

@app.route('/')
def home():
    return "CI/CD Server Running"

LAST_STATUS = {
    "status": "idle",
    "changes": "None",
    "time": ""
}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        files = []

        # Extract changed files safely
        if "commits" in data:
            for commit in data["commits"]:
                files.extend(commit.get("added", []))
                files.extend(commit.get("modified", []))
                files.extend(commit.get("removed", []))

        changed_files = "\n".join(files) if files else "No changes detected"

        log(f"📝 Changed files:\n{changed_files}")

        # Run deployment script
        result = os.system("sh /scripts/deploy.sh")

        if result != 0:
            log("❌ Deployment script failed")
            return jsonify({"status": "error", "message": "Deployment failed"}), 500

        log("✅ Deployment successful")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        log(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return send_file("index.html")

@app.route('/status')
def status():
    return LAST_STATUS

@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except:
        return "No logs yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


    