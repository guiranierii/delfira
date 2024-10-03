from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from fastapi.responses import Response

#Config das métricas do prometheus
REQUEST_COUNT = Counter("delfira_request_count", "Contagem total de HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("delfira_request_latency_seconds", "Tempo de respsotas das requisições HTTP", ["endpoint"])
ACTIVE_USERS = Gauge("delfira_active_users", "Total de usuários ativos na API")

#Middlware do Prometheus: Ele quem vai fazer a coleta automática, interceptando tudo
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        method = request.method
        endpoint = request.url.path
        status_code = 500

        ACTIVE_USERS.inc()

        try:
            with REQUEST_LATENCY.labels(endpoint=endpoint).time():
                response = await call_next(request)
                status_code = response.status_code

            REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

            return response
        
        finally:
            ACTIVE_USERS.dec()

def prometheus_metrics():
    metrics_content = generate_latest().decode('utf-8')
    return Response(content = metrics_content, media_type=CONTENT_TYPE_LATEST)
