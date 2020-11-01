from elastic_lab.tools.infra.elasticsearch import elastic_client
from elastic_lab.tools.services.seed import temporary_index


def experiment_should_tokenize_searched_text_with_default_analyzer():
    with temporary_index(elastic_client) as index_name:
        # arrange

        # fmt: off
        query = {
            "analyzer": "standard",
            "text": "Quick brown fox 2!"
        }
        # fmt: on

        # act
        es_response = elastic_client.indices.analyze(index=index_name, body=query)
        analyzed_text = [token_data["token"] for token_data in es_response["tokens"]]

        # assert
        first_token = es_response["tokens"][0]
        second_token = es_response["tokens"][1]
        third_token = es_response["tokens"][2]
        fourth_token = es_response["tokens"][3]

        assert analyzed_text == ["quick", "brown", "fox", "2"]  # tokenized (analyzed text)

        assert first_token["token"] == "quick"  # lowercase token filter
        assert first_token["type"] == "<ALPHANUM>"
        assert first_token["start_offset"] == 0

        assert second_token["token"] == "brown"
        assert second_token["type"] == "<ALPHANUM>"
        assert second_token["start_offset"] == 6

        assert third_token["token"] == "fox"  # most punctuation is removed in tokenization
        assert third_token["type"] == "<ALPHANUM>"
        assert third_token["start_offset"] == 12

        assert fourth_token["token"] == "2"  # numbers are kept in tokenization
        assert fourth_token["type"] == "<NUM>"
        assert fourth_token["start_offset"] == 16


def experiment_should_tokenize_searched_text_with_customized_analyzer():
    with temporary_index(elastic_client) as index_name:
        # arrange

        # fmt: off
        custom_analyzer_index_settings = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "my_new_analyzer": {"type": "standard", "stopwords": "_english_"}  # adds stopwords token filter
                    }
                }
            }
        }
        query_custom_analyzer = {
            "analyzer": "my_new_analyzer",
            "text": "The quick brown fox jumped a fence!"
        }
        query_default_analyzer = {
            "analyzer": "standard",
            "text": "The quick brown fox jumped a fence!"
        }
        # fmt: on

        elastic_client.indices.close(index_name)  # index must be closed in order to add the analyzer
        elastic_client.indices.put_settings(index=index_name, body=custom_analyzer_index_settings)
        elastic_client.indices.open(index_name)  # index is reopened for searches with the analyzer

        # act
        es_response = elastic_client.indices.analyze(index=index_name, body=query_custom_analyzer)
        es_response_default = elastic_client.indices.analyze(index=index_name, body=query_default_analyzer)

        analyzed_text_customized = [token_data["token"] for token_data in es_response["tokens"]]
        analyzed_text_default = [token_data["token"] for token_data in es_response_default["tokens"]]

        # assert
        assert analyzed_text_customized == ["quick", "brown", "fox", "jumped", "fence"]
        assert analyzed_text_default == ["the", "quick", "brown", "fox", "jumped", "a", "fence"]
