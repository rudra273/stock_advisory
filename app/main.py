import uvicorn
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agent-based LLM Stock Advisory System",
    version="0.1.0"
)


app.include_router(api_router, prefix="/api")


print(f"Database URL: {settings.DATABASE_URL}")






# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)