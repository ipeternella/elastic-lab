# Experiments: Leaf Queries

## Term vs Match queries

Unlike `match` queries, the `term` queries **do not analyze** the search term before actually performing the search. Hence, whatever is being searched will not undergo tokenization and token filtering and, as a result, may return poor or no results.

The `term` query should be used **exact matches** including whitespace and capitalization. This type of query can be useful for fields like `name.keyword` due to the fact that `keyword` fields are saved **without any text analysis** (stored as is).

Hence, for full text searching, the `match` queries are more well suited due to the tokenization and token filtering that are made to the searched field.

## match_phrase VS match_phrase_prefix

These two `match` queries will analyze (tokenize) the searched terms. However, `match_phrase` will require the search tokens in the same
order and EXACTLY as they appear whereas the `match_phrase_prefix` the LAST TOKEN will be used as PREFIX and not an exact match:

```text
{
    "query": {
        "match_phrase": {
            "title": "The Legend Of Z" --> ["the", "legend", "of", "z"]  (analyzer: last token is an EXACT match)
        }
    }
}

{
    "query": {
        "match_phrase_prefix": {
            "title": "The Legend Of Z" --> ["the", "legend", "of", "z.*"]  (analyzer: last token is a prefix!)
        }
    }
}
```
