"""
Settings to configure the application.
"""
from elastic_lab.infra.environment import getenv_or_exception
from elastic_lab.infra.environment import getenvbool_or_exception

# Elasticsearch connection
ELASTICSEARCH = {
    "host": getenv_or_exception("ELASTICSEARCH_HOST"),
    "port": int(getenv_or_exception("ELASTICSEARCH_PORT")),
    "user": getenv_or_exception("ELASTICSEARCH_HTTP_AUTH_USERNAME"),
    "password": getenv_or_exception("ELASTICSEARCH_HTTP_AUTH_PASSWORD"),
    "use_ssl": getenvbool_or_exception("ELASTICSEARCH_USE_SSL"),
}
