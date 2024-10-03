from fastapi import HTTPException, HTTPException, APIRouter
from app.services.dremio_connection import DremioConnection
import logging

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        query = "SELECT 1"
        df = DremioConnection(query)
        return{"status": "ok", "message": "Tá tudo certin"}
    except Exception:
        raise HTTPException(status_code=500, detail="Fudeo!")