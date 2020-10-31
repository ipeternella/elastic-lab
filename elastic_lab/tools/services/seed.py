"""
Service for seeding data on Elasticsearch to be used for the tests.
"""
from contextlib import contextmanager
from typing import Optional
from uuid import uuid4

from elasticsearch import Elasticsearch
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


@contextmanager
def temporary_index(client: Elasticsearch, temp_index_name: Optional[str] = None):
    """
    Temporarily creates a test index name which is deleted at the end of the context manager.
    """
    temp_index_name = temp_index_name if temp_index_name is not None else f"test-index-{uuid4()}"

    # creates and yields the test index name
    client.indices.create(temp_index_name)
    yield temp_index_name

    # deletes the temp index after the test
    client.indices.delete(temp_index_name)
