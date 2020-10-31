"""
Settings to configure the application.
"""
import os

from elastic_lab.tools.infra.environment import getenv_or_exception
from elastic_lab.tools.infra.environment import getenvbool_or_exception

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Elasticsearch connection
ELASTICSEARCH = {
    "host": getenv_or_exception("ELASTICSEARCH_HOST"),
    "port": int(getenv_or_exception("ELASTICSEARCH_PORT")),
    "user": getenv_or_exception("ELASTICSEARCH_HTTP_AUTH_USERNAME"),
    "password": getenv_or_exception("ELASTICSEARCH_HTTP_AUTH_PASSWORD"),
    "use_ssl": getenvbool_or_exception("ELASTICSEARCH_USE_SSL"),
}

ELASTICSEARCH_SEEDS = {"pipe_products": "resources/seeds/pipe_products.json"}
