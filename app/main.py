import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.ingest import router as ingest_router 
from app.db.db_init import init_db
from app.api.routes.stock import router as stock_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agent-based LLM Stock Advisory System",
    version="0.1.0"
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
