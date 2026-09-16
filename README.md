# Vakeel Contracts API

AI-powered contract analysis backend built with FastAPI, Google Gemini, MongoDB, and Docker.

This project allows users to upload PDF or TXT contracts, extract their text, analyze the contract using Google Gemini AI, and store the analysis results in MongoDB.

---

## Features

* Upload PDF and TXT contract files
* Validate uploaded file types
* Extract text from PDF and TXT files
* Store contract details in MongoDB
* Analyze contracts using Google Gemini AI
* Generate structured contract analysis
* Identify important contract clauses
* Identify potential risks
* Assign an overall risk level
* Generate recommendations
* Fetch all contracts
* Fetch a single contract
* Fetch contract analysis
* Delete contracts
* Swagger API documentation

---

## Tech Stack

* Python
* FastAPI
* Uvicorn
* MongoDB
* PyMongo
* Docker
* Docker Compose
* Google Gemini API
* `google-genai`
* PyPDF2
* Pydantic
* Pydantic Settings

---

## Project Architecture

```text
vakeel-contracts-api/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── contracts.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── contract_service.py
│   │   ├── contract_database.py
│   │   ├── document_parser.py
│   │   ├── gemini_service.py
│   │   └── contract_prompt.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── analysis.py
│   │
│   └── models/
│       └── __init__.py
│
├── uploads/
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Prerequisites

Before setting up the project, install the following software:

* Python 3.11 or higher
* Docker Desktop
* Git
* Google Gemini API key

Verify installations:

```bash
python --version
```

```bash
docker --version
```

```bash
docker compose version
```

```bash
git --version
```

---

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd vakeel-contracts-api
```

Example:

```bash
cd vakeel-contracts-api
```

---

## 2. Create a Python Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is successful, your terminal should show something similar to:

```text
(venv) PS C:\path\to\vakeel-contracts-api>
```

### macOS/Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Python Dependencies

Make sure the virtual environment is activated.

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install dependencies manually:

```bash
pip install fastapi uvicorn python-multipart PyPDF2 pymongo pydantic-settings google-genai
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
APP_NAME=Vakeel Contracts API
APP_VERSION=1.0.0
ENVIRONMENT=development

GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY

MONGODB_URL=mongodb://root:mypassword@localhost:27017
DATABASE_NAME=vakeel_contracts
```

### Environment Variable Description

| Variable         | Description            |
| ---------------- | ---------------------- |
| `APP_NAME`       | Application name       |
| `APP_VERSION`    | Application version    |
| `ENVIRONMENT`    | Current environment    |
| `GEMINI_API_KEY` | Google Gemini API key  |
| `MONGODB_URL`    | MongoDB connection URL |
| `DATABASE_NAME`  | MongoDB database name  |

### Getting Gemini API Key

Create an API key from Google AI Studio:

```text
https://aistudio.google.com/
```

Replace:

```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
```

with your actual key.

Never expose or commit your API key publicly.

---

## 5. Start MongoDB Using Docker Compose

This project uses MongoDB through Docker Compose.

Start MongoDB:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

You should see a MongoDB container running.

Check MongoDB logs:

```bash
docker logs vakeel-mongodb
```

Stop MongoDB:

```bash
docker compose down
```

Stop MongoDB and remove volumes:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` removes the MongoDB volume and may delete stored database data.

---

## 6. Run the FastAPI Application

Activate your virtual environment first.

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 7. API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## 8. Available API Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

### Health Check

```http
GET /
```

### Upload Contract

```http
POST /api/v1/contracts/upload
```

Supported file types:

* PDF
* TXT

### Test Gemini Connection

```http
GET /api/v1/contracts/test-ai
```

### Test Structured AI Analysis

```http
GET /api/v1/contracts/test-analysis
```

### Get All Contracts

```http
GET /api/v1/contracts/
```

### Get Single Contract

```http
GET /api/v1/contracts/{contract_id}
```

### Analyze Contract

```http
POST /api/v1/contracts/{contract_id}/analyze
```

### Get Contract Analysis

```http
GET /api/v1/contracts/{contract_id}/analysis
```

### Delete Contract

```http
DELETE /api/v1/contracts/{contract_id}
```

---

## 9. Typical API Workflow

The recommended workflow is:

```text
1. Upload Contract
       ↓
2. Receive contract_id
       ↓
3. Analyze Contract Using contract_id
       ↓
4. Gemini Generates Structured Analysis
       ↓
5. Analysis Saved in MongoDB
       ↓
6. Fetch Contract Analysis
```

Example:

```text
POST /api/v1/contracts/upload
```

Response:

```json
{
  "contract_id": "68abc123456789abcdef123456"
}
```

Then analyze:

```text
POST /api/v1/contracts/68abc123456789abcdef123456/analyze
```

Then fetch analysis:

```text
GET /api/v1/contracts/68abc123456789abcdef123456/analysis
```

---

## 10. MongoDB Information

MongoDB runs inside Docker using the following configuration:

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: vakeel-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: mypassword
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

MongoDB connection:

```text
mongodb://root:mypassword@localhost:27017
```

Database name:

```text
vakeel_contracts
```

Collection name:

```text
contracts
```

---

## 11. MongoDB Shell Access

Open MongoDB shell inside the container:

```bash
docker exec -it vakeel-mongodb mongosh
```

Switch to the admin database:

```javascript
use admin
```

Authenticate:

```javascript
db.auth("root", "mypassword")
```

Switch to the application database:

```javascript
use vakeel_contracts
```

View contracts:

```javascript
db.contracts.find().pretty()
```

---

## 12. Upload Directory

Uploaded files are stored inside:

```text
uploads/
```

Example:

```text
uploads/
├── employment.pdf
├── vendor-agreement.txt
└── nda.pdf
```

The `uploads/` directory should exist locally but should generally not be committed to Git if it contains user-uploaded files.

---

## 13. Git Ignore Configuration

Create a `.gitignore` file with:

```gitignore
# Virtual environment
venv/
.venv/

# Environment variables
.env

# Python cache
__pycache__/
*.py[cod]

# Uploaded files
uploads/

# IDE files
.vscode/
.idea/

# Operating system files
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## 14. Troubleshooting

### MongoDB Connection Error

Make sure Docker MongoDB is running:

```bash
docker ps
```

If it is not running:

```bash
docker compose up -d
```

---

### Gemini API Error

Check that:

* `GEMINI_API_KEY` exists in `.env`
* The API key is valid
* The `.env` file is in the project root
* The FastAPI server was restarted after changing `.env`

---

### ModuleNotFoundError

Make sure the virtual environment is activated:

```powershell
.\venv\Scripts\Activate.ps1
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

### Port Already in Use

If port `8000` is already being used:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will then run at:

```text
http://127.0.0.1:8001
```

---

### Docker Container Already Exists

If Docker reports that the container already exists:

```bash
docker start vakeel-mongodb
```

Or remove and recreate it:

```bash
docker compose down
docker compose up -d
```

---

## 15. Stop the Application

Stop FastAPI using:

```text
CTRL + C
```

Stop MongoDB:

```bash
docker compose down
```

---

## 16. Future Improvements

Planned improvements may include:

* JWT authentication
* User management
* Role-based access control
* Contract pagination
* Background AI processing
* Celery or task queues
* Contract chunking for large documents
* Streaming AI responses
* Better PDF extraction
* OCR for scanned PDFs
* File storage using AWS S3
* Production Dockerfile
* Docker Compose for the complete application
* Automated tests
* CI/CD pipeline
* Rate limiting
* Request logging
* API monitoring
* Frontend dashboard

---

## License

This project is for learning and development purposes.

---

## Author

Vakeel Contracts API