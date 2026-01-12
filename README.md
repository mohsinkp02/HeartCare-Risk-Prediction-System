# Heart Disease Risk Prediction - Production Solution

This is a production-ready implementation of the Heart Disease Risk Prediction system, transformed from a research prototype into an enterprise-grade solution.

## Key Features

- **Microservices Architecture**: Separate Backend (FastAPI) and Frontend (Nginx) services.
- **Production-Grade API**: Built with FastAPI, including auto-generated Swagger documentation.
- **Robust Validation**: Pydantic schemas for strict input validation.
- **Frontend Optimization**: Static asset serving via Nginx with optimized paths.
- **Observability**: Prometheus metrics instrumentation for monitoring.
- **Containerization**: Full Docker and Docker Compose support.
- **CI/CD**: GitHub Actions workflow for automated testing and building.
- **Testing**: Comprehensive unit and integration tests.

## Project Structure

```
production_solution/
├── app/                    # Backend Application Code
│   ├── api/                # API Routes
│   ├── core/               # Configuration & Logging
│   ├── services/           # Business Logic (Preprocessing, Prediction)
│   ├── schemas/            # Pydantic Models
│   ├── tests/              # Unit & Integration Tests
│   └── main.py             # Application Entrypoint
├── frontend/               # Static Frontend Assets
├── nginx/                  # Nginx Configuration
├── model/                  # ML Model Files
├── .github/                # CI/CD Workflows
├── docker-compose.yml      # Orchestration
├── Dockerfile              # Backend Container Definition
├── requirements.txt        # Python Dependencies
└── prometheus.yml          # Monitoring Config
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9+ (for local dev)

### Running with Docker (Recommended)

1. **Build and Run**:
   ```bash
   cd production_solution
   docker-compose up --build
   ```

2. **Access the Application**:
   - **Frontend**: [http://localhost](http://localhost)
   - **API Docs (Swagger)**: [http://localhost/docs](http://localhost/docs)
   - **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)

### Running Locally (Dev Mode)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Backend**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will run at `http://localhost:8000`.

3. **Run Frontend**:
   You can serve the `frontend` directory using any static file server (e.g., Live Server in VS Code) or access `frontend/index.html` directly in your browser (note: some API calls might need CORS configuration if ports differ).

## API Endpoints

- `POST /api/v1/predict`: Predict heart disease risk.
  - Body: JSON with patient data.
- `GET /health`: Health check endpoint.
- `GET /metrics`: Prometheus metrics.

## Testing

Run the test suite with pytest:

```bash
python -m pytest app/tests/test_api.py
```
