from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routes import router as api_router
from app.core.config import get_settings
from app.services.model_service import ModelService
from contextlib import asynccontextmanager
import os

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    ModelService.load_model()
    yield
    # Clean up resources if needed

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get absolute path to app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount Static Files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
if os.path.exists(TEMPLATES_DIR):
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
else:
    print(f"Warning: Templates directory not found at {TEMPLATES_DIR}")
    # Fallback to avoid crash on import, but routes will fail
    templates = Jinja2Templates(directory=".")

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calculate", response_class=HTMLResponse)
async def read_calculate(request: Request):
    return templates.TemplateResponse("calculate.html", {"request": request})

@app.get("/recommendation/{risk_level}", response_class=HTMLResponse)
async def read_recommendation(request: Request, risk_level: int):
    return templates.TemplateResponse("recommendation.html", {"request": request, "risk_level": risk_level})

# API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Prometheus Metrics
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
