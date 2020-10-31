"""
Elasticsearch client.
"""
from elasticsearch import Elasticsearch

from elastic_lab.settings import ELASTICSEARCH

elastic_client = Elasticsearch(
    hosts=[
        {
            "host": ELASTICSEARCH["host"],
            "port": ELASTICSEARCH["port"],
            "use_ssl": ELASTICSEARCH["use_ssl"],
            "http_auth": (ELASTICSEARCH["user"], ELASTICSEARCH["password"]),  # HTTP basic authentication
        }
    ]
)
