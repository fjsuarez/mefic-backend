from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OpenIdConnect
import firebase_admin
from routes import stocks, financial, technical, risk, portfolio, user_portfolio
from models import ErrorResponse
import logging

logger = logging.getLogger(__name__)

if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

openid_connect_url = f"https://securetoken.google.com/{cred.project_id}/.well-known/openid-configuration"
security_scheme = OpenIdConnect(openIdConnectUrl=openid_connect_url)

# --- Basic App Setup ---
app = FastAPI(
    title="Mefic API",
    description="API for fetching stock data and analysis for the Mefic app.",
    version="0.1.0",
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)

# --- CORS Configuration ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://mefic-ie.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root Endpoint ---
@app.get("/")
async def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the Mefic API!"}

app.include_router(stocks.router)
app.include_router(financial.router)
app.include_router(technical.router)
app.include_router(risk.router)
app.include_router(portfolio.router)
app.include_router(user_portfolio.router)

@app.middleware("http")
async def log_requests(request, call_next):
    """Log request details for debugging"""
    logger.info(f"Request path: {request.url.path}")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {request.headers.get('authorization', 'None')[:15]}...")
    
    response = await call_next(request)
    
    logger.info(f"Response status: {response.status_code}")
    return response