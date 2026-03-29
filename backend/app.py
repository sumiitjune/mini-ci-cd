from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Mini CI/CD Server Running 🚀"
# test webhook trigger
@app.route('/webhook', methods=['POST'])
def webhook():
    return "Webhook received!", 200
    return "Deployment triggered!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
