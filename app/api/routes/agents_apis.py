from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.agents.technical_analysis_agent import TechnicalAnalysisAgent
from app.db.config import get_db



router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

@router.get("/technical_agent/{symbol}")
def run_technical_agent(
    symbol: str,
    db: Session = Depends(get_db)
):
    agent = TechnicalAnalysisAgent(db)
    try:
        result = agent.execute(symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

