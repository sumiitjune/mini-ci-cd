# Mini CI/CD System (Flask + Docker)

## Overview

This project is a **mini CI/CD pipeline** built using:

* Flask (Webhook server)
* Docker (Containerization)
* Shell scripting (Deployment automation)
* HTML Dashboard (Monitoring)

It automatically deploys code when changes are pushed to GitHub.

---

##How It Works (Flow)

```text
GitHub Push
   ↓
Webhook Trigger
   ↓
Flask Server (/webhook)
   ↓
Extract Changed Files
   ↓
Run deploy.sh
   ↓
Docker Rebuild & Restart
   ↓
Update status.json
   ↓
Dashboard Updates
```

---

## Project Structure

```text
mini-cicd/
│
├── backend/
│   ├── app.py
│   ├── index.html
│   ├── Dockerfile
│   ├── status.json
│   └── scripts/
│       └── deploy.sh
│
├── docker-compose.yml
├── logs/
│   └── deploy.log
└── README.md
```

---

## Docker Setup

### Build & Run

```bash
docker-compose up --build
```

### Stop

```bash
docker-compose down
```

---

## Webhook Setup (GitHub)

1. Go to your repository → Settings → Webhooks
2. Add webhook:

   * Payload URL: `http://<your-ip>:5001/webhook`
   * Content type: `application/json`
3. Save

---

## Dashboard

Access:

```text
http://localhost:5001/dashboard
```

### Shows:

* Deployment status (success/failed/running)
* Last run time
* Changed files
* Logs

---

## Key Files Explained

### app.py

* Handles webhook
* Runs deployment script
* Updates status.json
* Serves dashboard & logs

### deploy.sh

* Pulls latest code
* Rebuilds Docker container

### status.json

* Stores latest deployment state

### logs/deploy.log

* Stores all logs

---

## Key Concepts Learned

* Docker containers vs host
* Volume mapping
* Webhooks (GitHub → Flask)
* CI/CD basics
* Debugging real deployment issues

---

##Limitations

* No authentication on webhook
* No rollback system
* Single project only

---

## Future Improvements

* Add webhook secret validation
* Add build history
* Add rollback system
* Deploy on cloud (AWS)

---

##💻 Author

Built by Sumit Kumar Baghel

---

##  Note

This is a learning project to understand CI/CD fundamentals using real debugging and problem-solving.
