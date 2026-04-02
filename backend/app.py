from flask import Flask, request, jsonify, send_file
import os
import datetime
import subprocess
import traceback
import json

app = Flask(__name__)

# 🔥 FILE PATHS (IMPORTANT)
STATUS_FILE = "/app/status.json"
LOG_FILE = "/app/logs/deploy.log"

os.makedirs("/app/logs", exist_ok=True)

# -------- LOG FUNCTION --------
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {message}\n")

# -------- STATUS FUNCTIONS --------
def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def load_status():
    if not os.path.exists(STATUS_FILE):
        save_status({
            "status": "idle",
            "changes": "None",
            "time": ""
        })

    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"Error reading status: {e}")
        return {
            "status": "error",
            "changes": "Cannot read status",
            "time": ""
        }

# -------- ROUTES --------

@app.route('/')
def home():
    return "CI/CD Running 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        log("📩 Webhook triggered")

        data = request.get_json()

        files = []
        if data and "commits" in data:
            for commit in data["commits"]:
                files.extend(commit.get("added", []))
                files.extend(commit.get("modified", []))
                files.extend(commit.get("removed", []))

        files = list(set(files))
        changed_files = "\n".join(files) if files else "No changes detected"

        log(f"📝 Changed files:\n{changed_files}")

        # 🔥 SAVE STATUS BEFORE DEPLOY
        status_data = {
            "status": "running",
            "changes": changed_files,
            "time": str(datetime.datetime.now())
        }
        save_status(status_data)

        # RUN DEPLOY
        result = subprocess.run(
            ["sh", "/scripts/deploy.sh"],
            capture_output=True,
            text=True
        )

        log(result.stdout)
        log(result.stderr)

        if result.returncode != 0:
            status_data["status"] = "failed"
            save_status(status_data)
            log("❌ Deployment failed")
            return jsonify({"status": "failed"}), 500

        status_data["status"] = "success"
        save_status(status_data)

        log("✅ Deployment success")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        log(str(e))
        log(traceback.format_exc())

        save_status({
            "status": "error",
            "changes": "Error occurred",
            "time": str(datetime.datetime.now())
        })

        return jsonify({"status": "error"}), 500


@app.route('/dashboard')
def dashboard():
    return send_file("index.html")


@app.route('/status')
def status():
    return load_status()   # 🔥 THIS FIXES YOUR ISSUE


@app.route('/logs')
def logs():
    try:
        with open(LOG_FILE) as f:
            return f.read()
    except:
        return "No logs"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)