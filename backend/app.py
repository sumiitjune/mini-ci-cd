from flask import Flask, request, jsonify
from flask import send_file
import os
import datetime
import subprocess

app = Flask(__name__)

LOG_FILE = "logs/deploy.log"

def log(message):
    os.makedirs("logs", exist_ok=True)  # ensure folder exists
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

@app.route('/')
def home():
    return "CI/CD Server Running 🚀"

LAST_STATUS = {
    "status": "idle",
    "changes": "None",
    "time": ""
}

@app.route('/webhook', methods=['POST'])
def webhook():
    global LAST_STATUS

    log("📩 Webhook triggered")

    try:
        try:
            changes = subprocess.check_output(
                "git diff --name-only HEAD~1 HEAD", shell=True
            ).decode()
        except:
            changes = "No previous commit or git history not available"

        log(f"📝 Changed files:\n{changes}")

        os.system("sh /scripts/deploy.sh")

        log("✅ Deployment successful")

        LAST_STATUS = {
            "status": "success",
            "changes": changes,
            "time": str(datetime.datetime.now())
        }

        return "OK", 200

    except Exception as e:
        log(f"❌ Deployment failed: {e}")

        LAST_STATUS = {
            "status": "failed",
            "changes": "",
            "time": str(datetime.datetime.now())
        }

        return "Fail", 500

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


    