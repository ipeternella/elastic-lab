# Experiments: Leaf Queries

## Term vs Match queries

Unlike `match` queries, the `term` queries **do not analyze** the search term before actually performing the search. Hence, whatever is being searched will not undergo tokenization and token filtering and, as a result, may return poor or no results.

The `term` query should be used **exact matches** including whitespace and capitalization. This type of query can be useful for fields like `name.keyword` due to the fact that `keyword` fields are saved **without any text analysis** (stored as is).

Hence, for full text searching, the `match` queries are more well suited due to the tokenization and token filtering that are made to the searched field.
