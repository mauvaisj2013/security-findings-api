# Security Findings REST API

A lightweight REST API and command-line client built with Python.

This project demonstrates how to create and consume a REST API using Flask and Requests, manage JSON data, validate incoming requests, and sort API results.

## 1. Project Overview

The application consists of two main components:

- **REST API (`api.py`):** Provides a single endpoint supporting GET and POST requests to retrieve and add security findings.
- **CLI Client (`main.py`):** Communicates with the API, retrieves security findings, sorts them by date in descending order, and submits a new finding.

Security findings are stored locally in `results.json`, allowing newly submitted entries to persist between application restarts.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| Flask | REST API framework |
| Requests | HTTP client for the CLI |
| JSON | Data storage and exchange |
| pathlib | File path management |

## 3. Project Structure

```text
security-findings-api/
├──templates/
|  └─── home.html
├── api.py
├── main.py
├── results.json
├── requirements.txt
└── README.md
```

## 4. Installation and Setup

### Prerequisites

- Python 3 installed
- pip available
- A terminal or command prompt

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd security-findings-api
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

The application requires Flask and Requests.

### Step 4: Start the API server

```bash
python api.py
```

The API will be accessible at:

```text
http://127.0.0.1:5000/api/v1/results
```

Keep this terminal running.

### Step 5: Run the CLI client

Open another terminal, activate the same virtual environment, and execute:

```bash
python main.py
```

The CLI retrieves the stored findings, sorts them by date (newest first), displays them, and submits the example finding configured in `main.py`.

## 5. API Documentation

### Endpoint

```text
/api/v1/results
```

Supported HTTP methods: `GET`, `POST`

### GET — Retrieve Security Findings

**Request:**

```http
GET /api/v1/results
```

**Successful response: `200 OK`**

```json
{
    "results": [
        {
            "name": "SQL Injection",
            "type": "Application",
            "description": "Improper Input Validation",
            "date": "2026-10-20"
        },
        {
            "name": "Elevation of Privilege",
            "type": "Platform",
            "description": "Security Feature Bypass",
            "date": "2022-01-01"
        }
    ]
}
```

The API returns the collection in its stored order. The CLI is responsible for sorting the results by date.

### POST — Add Security Findings

The POST endpoint accepts either a single JSON object or a list of JSON objects.

Each finding must contain these fields:

| Field | Description |
|---|---|
| `name` | Name of the security finding |
| `type` | Category of the finding |
| `description` | Description of the finding |
| `date` | Date represented as `YYYY-MM-DD` |

**Example: Submit one finding**

```bash
curl -X POST http://127.0.0.1:5000/api/v1/results \
  -H "Content-Type: application/json" \
  -d '{"name":"Missing MFA","type":"Identity","description":"MFA not enforced","date":"2026-10-21"}'
```

**Example: Submit multiple findings**

```json
[
    {
        "name": "Exposed Credentials",
        "type": "Application",
        "description": "Hardcoded API key",
        "date": "2026-10-19"
    },
    {
        "name": "Overly Permissive IAM Role",
        "type": "Infrastructure",
        "description": "Wildcard IAM permissions",
        "date": "2026-10-18"
    }
]
```

Send this JSON array as the POST request body with `Content-Type: application/json`.

**Successful response: `201 Created`**

```json
{
    "message": "Received successfully",
    "result": {
        "name": "Missing MFA",
        "type": "Identity",
        "description": "MFA not enforced",
        "date": "2026-10-21"
    }
}
```

### Error Responses

| Status | Meaning |
|---|---|
| `400 Bad Request` | Required fields are missing or the top-level JSON structure is unsupported |
| `409 Conflict` | An identical finding already exists in the stored collection or has been encountered earlier in the submitted batch |

Example:

```json
{
    "error": "Entry already exists."
}
```

Duplicate detection compares complete JSON objects, not individual fields such as `name`.

## 6. CLI Functionality

The CLI uses the Requests library to interact with the API.

Its workflow is:

1. Send a GET request to retrieve security findings.
2. Parse the JSON response into Python objects.
3. Sort the findings by `date` in descending order.
4. Print the sorted findings to the terminal.
5. Submit an example security finding using POST.
6. Display the POST response status and body.

Dates use the ISO-style `YYYY-MM-DD` representation, which supports chronological string sorting when values are valid and consistently formatted.

**Note:** The CLI performs GET before POST. A newly submitted finding therefore appears in the retrieved list on a subsequent execution. Repeating an identical POST request returns `409 Conflict`.

## 7. Data Persistence and Validation

The API stores findings in a local JSON file rather than using an external database.

For POST requests, the application:

- Loads the existing collection.
- Checks for exact duplicate entries.
- Checks that the required fields are present.
- Appends valid findings to the collection.
- Writes the updated collection to `results.json`.

For batch submissions, the application checks entries before writing the updated collection to disk. If a validation error occurs, the request returns an error without saving the partially processed batch.

## 8. Design Decisions

**Single API endpoint:** Both GET and POST are implemented through the same Flask route, matching the assessment requirements.

**File-based persistence:** JSON storage keeps the solution lightweight and avoids introducing database infrastructure beyond the assessment's scope.

**Procedural design:** Small functions and straightforward control flow were chosen over unnecessary class abstractions.

**Client-side sorting:** The CLI handles date sorting independently of the API, demonstrating the separation between data retrieval and presentation.

## 9. Limitations and Future Improvements

This project is intended as a small technical demonstration rather than a production-ready service.

Potential improvements include:

- Stricter validation of field types and date formats.
- Rejecting empty batch submissions and non-object entries within batches.
- Handling API connection failures and non-successful responses in the CLI.
- Automated unit and integration tests.
- Database-backed storage for concurrent requests.
- Authentication, authorization, and request logging for production deployment.

The Flask development server is intended for local testing only.

## 10. Assessment Requirements

| Requirement | Implementation |
|---|---|
| Single API route supporting GET and POST | `/api/v1/results` |
| JSON DTO with four required fields | `name`, `type`, `description`, `date` |
| GET returns findings in `{"results": [...]}` | Implemented |
| Initial collection contains at least 10 objects | Implemented |
| POST supports one or multiple objects | Implemented |
| CLI invokes GET and POST | Implemented |
| CLI sorts GET results by descending date | Implemented |

---

**Project purpose:** Demonstrate foundational REST API development, HTTP communication, JSON persistence, input validation, and Python command-line integration.
