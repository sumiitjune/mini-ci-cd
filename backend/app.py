from flask import Flask, request, jsonify
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

@app.route('/webhook', methods=['POST'])
def webhook():
    log("📩 Webhook triggered")

    try:
        # Get changed files
        try:
            changes = subprocess.check_output(
                "git diff --name-only HEAD~1 HEAD", shell=True
            ).decode()
        except:
            changes = "No previous commit or git history not available"

        log(f"📝 Changed files:\n{changes}")

        # 🚀 Deploy
        os.system("sh /scripts/deploy.sh")

        log("✅ Deployment successful")

        return jsonify({
            "status": "success",
            "changed_files": changes
        })

    except Exception as e:
        log(f"❌ Deployment failed: {e}")
        return jsonify({"status": "failed", "error": str(e)})

@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except:
        return "No logs yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)