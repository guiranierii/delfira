from fastapi import Request, APIRouter
from app.services.prometheus_metrics import prometheus_metrics
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/metrics")
@limiter.limit("10/minute")
async def metrics(request:Request):
    return prometheus_metrics()