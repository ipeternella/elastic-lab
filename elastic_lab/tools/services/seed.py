"""
Service for seeding data on Elasticsearch to be used for the tests.
"""
from elasticsearch.helpers import bulk

from elastic_lab.settings import ELASTICSEARCH_SEEDS
from elastic_lab.tools.infra.elasticsearch import elastic_client
from elastic_lab.tools.infra.json_reader import read_seed_json


def seed_elasticsearch_with_json(index_name: str, json_seed_path: str):
    """
    Bulk inserts seed data based on a JSON file into Elasticsearch in a given index.
    """
    elastic_data = read_seed_json(json_seed_path)["data"]
    actions = [{"_index": index_name, "_source": doc} for doc in elastic_data]

    bulk(elastic_client, actions)
    elastic_client.indices.refresh(index_name)


def seed_elasticsearch_with_pipe_products(index_name: str):
    """
    Seeds Elasticsearch with pipe products.
    """
    pipe_products_json_path = ELASTICSEARCH_SEEDS["pipe_products"]

    seed_elasticsearch_with_json(index_name, pipe_products_json_path)
