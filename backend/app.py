from flask import Flask, request, jsonify, send_file
import os
import datetime
import subprocess
import traceback
import json

app = Flask(__name__)

LOG_FILE = "logs/deploy.log"
STATUS_FILE = "status.json"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# ---------------- LOG FUNCTION ----------------
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {message}\n")

# ---------------- STATUS FUNCTIONS ----------------
def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def load_status():
    if not os.path.exists(STATUS_FILE):
        return {
            "status": "idle",
            "changes": "None",
            "time": ""
        }
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return "CI/CD Server Running 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        log("📩 Webhook triggered")

        data = request.get_json()

        if not data:
            log("❌ No JSON received")
            return jsonify({"error": "No JSON received"}), 400

        files = []

        # Extract changed files
        if "commits" in data:
            for commit in data["commits"]:
                files.extend(commit.get("added", []))
                files.extend(commit.get("modified", []))
                files.extend(commit.get("removed", []))

        files = list(set(files))  # remove duplicates

        changed_files = "\n".join(files) if files else "No changes detected"

        log(f"📝 Changed files:\n{changed_files}")

        # 🔥 SAVE STATUS BEFORE DEPLOY
        status_data = {
            "status": "running",
            "changes": changed_files,
            "time": str(datetime.datetime.now())
        }
        save_status(status_data)

        log("🚀 Starting deployment...")

        result = subprocess.run(
            ["sh", "/scripts/deploy.sh"],
            capture_output=True,
            text=True
        )

        log(f"📤 STDOUT:\n{result.stdout}")
        log(f"📛 STDERR:\n{result.stderr}")

        if result.returncode != 0:
            status_data["status"] = "failed"
            save_status(status_data)

            log("❌ Deployment failed")
            return jsonify({"status": "error"}), 500

        # ✅ SUCCESS
        status_data["status"] = "success"
        save_status(status_data)

        log("✅ Deployment successful")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        error_msg = str(e)

        log(f"💥 Error: {error_msg}")
        log(traceback.format_exc())

        # save error state
        save_status({
            "status": "error",
            "changes": "Error occurred",
            "time": str(datetime.datetime.now())
        })

        return jsonify({"status": "error", "message": error_msg}), 500


@app.route('/dashboard')
def dashboard():
    return send_file("index.html")


@app.route('/status')
def status():
    return load_status()   # 🔥 IMPORTANT FIX


@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except:
        return "No logs yet"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)