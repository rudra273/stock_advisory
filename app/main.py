import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from app.core.config import settings
from app.api.routes.ingest import router as ingest_router 
from app.db.db_init import init_db
from app.api.routes.stock_apis import router as stock_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agent-based LLM Stock Advisory System",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Example: if your frontend runs on port 3000
    "*" # WARNING: Using "*" allows all origins. Restrict this in production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True, # Allow cookies to be included in requests
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)
# letter will be replced by alembic
@app.on_event("startup")
def on_startup():
    init_db()  # create tables if not exist


# Register the ingestion router
app.include_router(ingest_router)
app.include_router(stock_router)


# Base API (root endpoint)
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Agent-based LLM Stock Advisory System!",
        "version": "0.1.0",
        "available_routes": ["/ingest/daily", "/ingest/current", "/ingest/stock-info", "/ingest/balance-sheet", "/ingest/income-statement", "/ingest/cash-flow"]
    }

# Print the DB URL on startup
print(f"Database URL: {settings.DATABASE_URL}")

# Optional: run with uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
