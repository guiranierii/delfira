from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.services.prometheus_metrics import PrometheusMiddleware
from app.routers import purchases, health, metrics
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
from app.config.logging_config import setup_logging

setup_logging()

# Inicializando o FastAPI
app = FastAPI()

# Config do SlowAPI
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Cê tá ficando maluco? Me deixa em paz mano, para com essa porra de trocendas mil requisições"}
    )

app.add_middleware(SlowAPIASGIMiddleware)  
app.add_middleware(PrometheusMiddleware)

app.include_router(purchases.router)
app.include_router(health.router)
app.include_router(metrics.router)