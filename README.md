# SpamShield-Dashboard
An automated email monitoring system with live inbox analysis, background classification, and a real-time dashboard for spam detection.
## Overview

This project is a server-rendered email analysis dashboard designed to demonstrate backend automation, ML integration, and real-time updates **without using WebSockets**, relying instead on background threads and controlled polling.

[View Demo](https://drive.google.com/file/d/1X0B6fGd41uokSjRg6fxGu5q-WqqRUNyW/view?usp=sharing)

## Key Features

- Automated inbox monitoring using IMAP
- Live email analysis with background processing
- Server-Side Rendering (SSR) with Flask and Jinja
- Real-time UI updates via polling (no WebSockets)
- Top 20 recent emails with classification badges
- Detailed analysis view for selected emails
- Graceful start/stop of live monitoring


## Architecture
```bash
Frontend (HTML + CSS + minimal JS)
|
| Polling
v
Flask Application
├── /             #Server-rendered dashboard
├── /live         #Starts background email monitoring
├── /live-status  #Returns latest analyzed email
└── /stop-live    #Stops live monitoring
|
v
Background Thread
├── Fetch emails via IMAP
├── Text preprocessing (spaCy)
├── Vectorization (TF-IDF)
└── ML prediction (Spam / Ham)
```
## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/BhumikaYeole/SpamShield-Dashboard.git
cd SpamShield-Dashboard
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 3. Add your email and app password in reader.py

```bash
HOST = "imap.gmail.com"
USERNAME = "your_email_address"
PASSWORD = "your_app_password"
```
Use an app password generated from your email provider (e.g., Gmail App Password).

### 4. Run the application
```bash
python app.py
```
Open browser at
```bash
http://127.0.0.1:5000
```

---


