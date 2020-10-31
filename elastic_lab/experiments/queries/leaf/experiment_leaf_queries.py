from elastic_lab.tools.infra.elasticsearch import elastic_client
from elastic_lab.tools.services.seed import seed_elasticsearch_with_pipe_products
from elastic_lab.tools.services.seed import temporary_index


def experiment_should_get_all_documents_using_match_all_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # act
        query = {"query": {"match_all": {}}}
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 6


def experiment_should_get_no_docs_using_term_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # act: should not find as 'description' field is text and has been analyzed (tokenized)
        # so the qry shouldn't find any docs with term (which does not analyze the searched term)
        # fmt: off
        query = {
            "query": {
                "term": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 0


def experiment_should_get_all_docs_using_match_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # act: should find all docs as the tokenized terms like 'PVC', 'water', 'pipe' will mostly
        # like match all docs
        # fmt: off
        query = {
            "query": {
                "match": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 6


def experiment_should_get_two_docs_using_match_phrase_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # act: should find just two docs, as the 'match_phrase' analyzes the search text (tokenizes it) and
        # creates a phrase query of the text (which must respect the token order)
        # fmt: off
        query = {
            "query": {
                "match_phrase": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 2
