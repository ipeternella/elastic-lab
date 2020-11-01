# Experiments: Elasticsearch DSL (Domain specific language)

Elasticsearch provides a full query DSL (Domain Specific Language) which is based on JSONs. Hence, Elasticsearch's DSL is like an AST (Abstract Syntax Tree) defined with JSONs.

Just like every AST, there can be leaf nodes (called `leaf queries` -- individual queries) and interior nodes (called `compound queries` -- a query that itself wraps other leaf or other compound queries). The compound queries wrap several smaller queries in a `boolean` or `dis_max` way.

## Leaf queries

These can be `match`, `term` or `range` queries. They are standalone queries that can be executed directly.

## Compound queries

This query envolves/wraps other leaf queries or other compound queries. Think of it as a **group of queries** that are executed and the results are combined in a boolean way, for example.

## Expensive queries

These are like leaf queries in a way that they can be executed directly, but they can affect stability of the cluster. Examples:

- `script queries`: perform linear scans
- `fuzzy, regexp, prefix, wildcard, etc. queries`: high up-front cost, except if performed on **wildcard type** fields
- `joining queries`: sql-like join queries that are very expensive as ES is a distributed data store
