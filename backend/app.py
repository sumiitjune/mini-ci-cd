from flask import Flask, request, jsonify, send_file
import os
import datetime
import subprocess
import traceback

app = Flask(__name__)

LOG_FILE = "logs/deploy.log"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {message}\n")

# 🔥 GLOBAL STATE (THIS WAS YOUR MISSING PIECE)
LAST_STATUS = {
    "status": "idle",
    "changes": "None",
    "time": ""
}

@app.route('/')
def home():
    return "CI/CD Server Running 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    global LAST_STATUS

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

        # Remove duplicates
        files = list(set(files))

        changed_files = "\n".join(files) if files else "No changes detected"

        log(f"📝 Changed files:\n{changed_files}")

        # 🔥 UPDATE STATUS BEFORE DEPLOY
        LAST_STATUS["status"] = "running"
        LAST_STATUS["changes"] = changed_files
        LAST_STATUS["time"] = str(datetime.datetime.now())

        log("🚀 Starting deployment...")

        # 🔥 BETTER THAN os.system
        result = subprocess.run(
            ["sh", "/scripts/deploy.sh"],
            capture_output=True,
            text=True
        )

        log(f"📤 STDOUT:\n{result.stdout}")
        log(f"📛 STDERR:\n{result.stderr}")

        if result.returncode != 0:
            LAST_STATUS["status"] = "failed"
            log("❌ Deployment failed")

            return jsonify({
                "status": "error",
                "changes": files
            }), 500

        # ✅ SUCCESS
        LAST_STATUS["status"] = "success"
        log("✅ Deployment successful")

        return jsonify({
            "status": "success",
            "changes": files
        }), 200

    except Exception as e:
        LAST_STATUS["status"] = "error"

        error_msg = str(e)
        log(f"💥 Error: {error_msg}")
        log(traceback.format_exc())

        return jsonify({
            "status": "error",
            "message": error_msg
        }), 500


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