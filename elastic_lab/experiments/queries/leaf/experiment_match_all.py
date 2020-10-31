from uuid import uuid4

from elastic_lab.tools.infra.elasticsearch import elastic_client
from elastic_lab.tools.services.seed import seed_elasticsearch_with_pipe_products


def experiment_should_use_match_all_to_query_all_documents():
    """
    Objective: analyze the leaf query used to get all documents from an index.
    """
    # arrange
    index_name = f"pipes-index-1-{uuid4()}"
    seed_elasticsearch_with_pipe_products(index_name)

    # act
    query = {"query": {"match_all": {}}}
    es_response = elastic_client.search(index=index_name, body=query)

    # assert
    assert es_response["hits"]["total"]["value"] == 6
