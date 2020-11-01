from elasticsearch.helpers import bulk

from elastic_lab.tools.infra.elasticsearch import elastic_client
from elastic_lab.tools.services.seed import seed_elasticsearch_with_pipe_products
from elastic_lab.tools.services.seed import temporary_index


def experiment_should_get_all_documents_using_match_all_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)
        query = {"query": {"match_all": {}}}

        # act
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 6


def experiment_should_get_no_docs_using_term_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # fmt: off
        query = {
            "query": {
                "term": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on

        # act -> should not find as 'description' field is text and has been analyzed (tokenized)
        # so the qry shouldn't find any docs with term (which does not analyze the searched term)
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 0


def experiment_should_get_all_docs_using_match_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # fmt: off
        query = {
            "query": {
                "match": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on

        # act -> should find all docs as the tokenized terms like 'PVC', 'water', 'pipe' will mostly like match all docs
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 6


def experiment_should_get_two_docs_using_match_phrase_query():
    with temporary_index(elastic_client) as index_name:
        # arrange
        seed_elasticsearch_with_pipe_products(index_name)

        # fmt: off
        query = {
            "query": {
                "match_phrase": {
                    "description": "PVC water pipe elbow joint of 90 degrees"
                }
            }
        }
        # fmt: on

        # act -> should find just two docs, as the 'match_phrase' analyzes the search text (tokenizes it) and
        # creates a phrase query of the text (which must respect the token order)
        es_response = elastic_client.search(index=index_name, body=query)

        # assert
        assert es_response["hits"]["total"]["value"] == 2


def experiment_should_check_differences_between_match_phrase_and_match_phrase_prefix_queries():
    with temporary_index(elastic_client) as index_name:
        # arrange
        actions = [
            {"_index": index_name, "_source": {"title": "The Legend Of Zelda: Majora's Mask"}},
            {"_index": index_name, "_source": {"title": "The Legend Of Zelda: Ocarina Of Time"}},
            {"_index": index_name, "_source": {"title": "The Legend Of Zelda: Breath Of The Wild"}},
            {"_index": index_name, "_source": {"title": "The Legend Of Zelda: A Link To The Past"}},
            {"_index": index_name, "_source": {"title": "The Legend Of Z: Something Else"}},  # no prefix matches this!
        ]
        bulk(elastic_client, actions)
        elastic_client.indices.refresh(index_name)

        # fmt: off
        query_match_phrase_no_prefix = {
            "query": {
                "match_phrase": {
                    "title": "The Legend Of Z"  # search terms must match in the same order and as they are
                }
            }
        }

        query_match_phrase_prefix = {
            "query": {
                "match_phrase_prefix": {
                    "title": "The Legend Of Z"  # search terms must match in the same order but the last one is a PREFIX
                }
            }
        }
        # fmt: on

        # act
        es_response_no_prefix = elastic_client.search(index=index_name, body=query_match_phrase_no_prefix)
        es_response_prefix = elastic_client.search(index=index_name, body=query_match_phrase_prefix)

        # assert -> with match_phrase, the last term requires an EXACT match!
        assert es_response_no_prefix["hits"]["total"]["value"] == 1
        assert es_response_no_prefix["hits"]["hits"][0]["_source"]["title"] == "The Legend Of Z: Something Else"

        # assert -> with match_phrase_prefix, the last term is a PREFIX and does not require an exact match!
        assert es_response_prefix["hits"]["total"]["value"] == 5
