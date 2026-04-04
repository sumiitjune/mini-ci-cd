from flask import Flask, request, jsonify, send_file
import os
import datetime
import subprocess
import json

app = Flask(__name__)

LOG_FILE = "logs/deploy.log"
STATUS_FILE = "status.json"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# ---------------- LOG FUNCTION ----------------
def log(message):
    timestamp = datetime.datetime.now()
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {message}\n")

    # 🔥 Keep only last 100 lines
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    with open(LOG_FILE, "w") as f:
        f.writelines(lines[-100:])


# ---------------- STATUS FUNCTIONS ----------------
def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)


def load_status():
    if not os.path.exists(STATUS_FILE):
        default = {
            "status": "idle",
            "changes": "None",
            "time": ""
        }
        save_status(default)
        return default

    with open(STATUS_FILE, "r") as f:
        return json.load(f)


# ---------------- FILTER CHANGED FILES ----------------
def get_changed_files(data):
    files = []

    if data and "commits" in data:
        for commit in data["commits"]:
            files.extend(commit.get("added", []))
            files.extend(commit.get("modified", []))
            files.extend(commit.get("removed", []))

    # remove duplicates
    files = list(set(files))

    # 🔥 filter unwanted files
    filtered = []
    for f in files:
        if (
            not f.startswith("logs/") and
            "status.json" not in f and
            not f.endswith(".log")
        ):
            filtered.append(f)

    return "\n".join(filtered) if filtered else "No changes detected"


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
            return jsonify({"error": "No JSON"}), 400

        # 🔥 GET CHANGED FILES
        changed_files = get_changed_files(data)

        log(f"📝 Changed files:\n{changed_files}")

        # 🔥 UPDATE STATUS → RUNNING
        status_data = {
            "status": "running",
            "changes": changed_files,
            "time": str(datetime.datetime.now())
        }
        save_status(status_data)

        # 🔥 RUN DEPLOY IN BACKGROUND (IMPORTANT)
        subprocess.Popen(["sh", "/app/backend/scripts/deploy.sh"])

        log("🚀 Deployment started in background")

        # ✅ RETURN FAST → ngrok will show 200
        return jsonify({"status": "started"}), 200

    except Exception as e:
        log(f"💥 Error: {str(e)}")

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
    return load_status()


@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except:
        return "No logs yet"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)