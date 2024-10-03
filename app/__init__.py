from .config.settings import Settings  # Importando as configurações do app
from .services.prometheus_metrics import PrometheusMiddleware, prometheus_metrics  # Importando Prometheus
from .services.dremio_connection import dremio_query  # Função de conexão com o Dremio
from app.config.logging_config import setup_logging