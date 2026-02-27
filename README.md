
# 🚀 HR-Pulse — Automated Job Offer Analysis Platform

> A full-stack AI-powered platform that automates the analysis of job offers, extracts key skills using NER, predicts salary ranges, and exposes everything through a modern API — fully containerized and observable.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Phases](#phases)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [CI/CD Pipeline](#cicd-pipeline)
- [Observability](#observability)
- [Contributing](#contributing)

---

## 📌 Overview

HR-Pulse is a startup looking to automate the analysis of its job listings. This project delivers:

- **Infrastructure as Code** via Terraform (Azure SQL + Azure AI Language)
- **AI-powered NER** to extract skills from job descriptions
- **ML salary predictor** to benchmark competitiveness
- **FastAPI backend** exposing data and predictions
- **Next.js frontend** for recruiters
- **Full Docker orchestration** with OpenTelemetry tracing via Jaeger



---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Azure Cloud                          │
│  ┌──────────────────┐        ┌──────────────────────────┐  │
│  │  Azure SQL DB    │        │  Azure AI Language (NER) │  │
│  │  (Serverless)    │        │  Named Entity Recognition│  │
│  └──────────────────┘        └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ▲                              ▲
         │                              │
┌────────┴──────────────────────────────┴────────┐
│                  FastAPI Backend                │
│         + ML Predictor (Salary Estimate)        │
│         + OpenTelemetry Instrumentation         │
└────────────────────────┬───────────────────────┘
                         │
            ┌────────────┴────────────┐
            │         Next.js         │
            │        Frontend         │
            └─────────────────────────┘
                         │
            ┌────────────┴────────────┐
            │    Jaeger (Tracing UI)  │
            │    :16686               │
            └─────────────────────────┘          
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Package Manager | `uv` |
| Infrastructure | Terraform + Azure |
| Database | Azure SQL (via pyodbc / SQLAlchemy) |
| AI / NER | Azure AI Language |
| ML | scikit-learn (Regression) |
| Backend | FastAPI |
| Frontend | Next.js |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Linting | Flake8 |
| Testing | Pytest |
| Observability | OpenTelemetry + Jaeger |

---

## ✅ Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- [Terraform](https://www.terraform.io/) >= 1.5
- An Azure account with access to your provisioned Resource Group
- ODBC Driver 18 for SQL Server installed locally (for dev)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/HR-pulse-ai-platform.git
cd HR-pulse-ai-platform
```

### 2. Install dependencies with `pip`

```bash
pip install
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Fill in your Azure credentials
```

### 4. Provision infrastructure with Terraform

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```


### 5. Launch all services

```bash
docker compose up --build
```

---

## 📁 Project Structure

```
hr-pulse/
├── .github/
│   └── workflows/
│       └── ci.yml               
├── terraform/
│   ├── main.tf                  
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf               
├── src/
│   ├── ingestion/
│   │   └── ingest.py            
│   ├── predictor/
│   │   └── model.py             
│   ├── api/
│   │   └── main.py              
│   └── frontend/
│       └── app.py
├── model/
│   └── hr_ai_platform.pkl 
├── ml/
│   └── notebook                
├── tests/
│   └── test_*.py                
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── pyproject.toml              
├── .env.example
└── README.md
```

---

## 📦 Phases

### Phase 1 — Infrastructure as Code (Terraform)

Terraform provisions:
- **Azure SQL Database** (Serverless mode) for job & skills persistence
- **Azure AI Language** resource for NER

State is stored remotely via `azurerm` backend on the centralized Storage Account.

```bash
cd terraform && terraform init && terraform apply
```

---

### Phase 2 — Data & AI Pipeline

The ingestion script (`ml/src/prediction.py`):
1. Cleans `jobs.csv` (removes nulls, normalizes fields)
2. Sends job descriptions to **Azure AI Language** for NER skill extraction
3. Injects results into Azure SQL with the schema:

| Column | Type | Description |
|---|---|---|
| `id` | INT | Unique job offer ID |
| `job_title` | VARCHAR | Cleaned job title |
| `skills_extracted` | JSON | Skills extracted by NER |

---

### Phase 3 — Salary Predictor

- Parses `Salary Estimate` (e.g. `"$137K-$171K"` → `154`)
- Trains a **regression model** (scikit-learn) to predict average salary
- Exposed via the FastAPI `/predict` endpoint

---

### Phase 4 — API & Frontend

**FastAPI** (`src/api/main.py`) exposes:
- `GET /search_jobs/search?skill=python` — filter by skill
- `POST /salary_predict` — predict salary from job features

**Frontend** (Next.js):
- Browse and search job offers
- Upload new CSV files
- View salary predictions

---

### Phase 5 — Docker

```bash
docker compose up --build
```

Services launched:
- `backend` — FastAPI app
- `frontend` — Next.js UI
- `jaeger` — distributed tracing UI at [http://localhost:16686](http://localhost:16686)

Terraform Docker Provider is used to inject `.env` variables dynamically into containers.

---

### Phase 6 — Tests (Pytest)

```bash
pytest tests/ -v
```

Tests cover: data cleaning, NER parsing, salary preprocessing, API endpoints.

---

### Phase 7 — CI/CD (GitHub Actions)

The pipeline (`.github/workflows/ci.yml`) runs on every push:

| Job | Tool | Description |
|---|---|---|
| `lint` | Ruff / Flake8 | Code quality check — fails on violations |
| `test` | Pytest | Unit test execution |
| `build` | Docker | Build backend & frontend images |

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Azure SQL
DATABASE_URL=mssql+pyodbc://<username>:<password>@<server>.database.windows.net/<database>?driver=ODBC+Driver+18+for+SQL+Server

# Azure AI Language
AZURE_LANGUAGE_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=<your-key>
```

---

## 🐳 Running with Docker

```bash
# Build and start all services
docker compose up --build

# Stop all services
docker compose down
```

**Services & Ports:**

| Service | Port |
|---|---|
| FastAPI Backend | `8000` |
| Frontend | `3000` |
| Jaeger UI | `16686` |
| Jaeger OTLP | `4317` |

---

## 📡 Observability

The API is instrumented with **OpenTelemetry**:
- Traces every request from frontend to Azure
- Measures **Azure AI Language** response time
- Measures **SQL query latency**
- Surfaces **HTTP 500 errors** in Jaeger

Access the Jaeger UI at: [http://localhost:16686](http://localhost:16686)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Ensure linting passes: `uv run ruff check .`
4. Ensure tests pass: `uv run pytest`
5. Open a Pull Request

---
