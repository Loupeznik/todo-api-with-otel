import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()
logger = logging.getLogger()


@router.get("/healthz")
def health_check(db: Session = Depends(deps.get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(
            status_code=503, detail="Database connection failed")
