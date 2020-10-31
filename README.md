# 🧪 Elastic Lab ⚗️

A repo for experimenting techniques, features and setups regarding the Elastic stack. In fact, this repo is mainly based on **tests** (called here as `experiments`) that are used to analyze/study some given features from the Elastic stack such as the different queries that Elasticsearch allows.

The experiments are written using `pytest` testing framework and are run against a `7.9.1` Elasticsearch cluster.

## Experiments

So far, the covered experiments (tests) with very useful `README.md` that can be used to study/learn the topic are the ones as follows:

- `text analysis`: what are analyzers, how to customize and use, etc.
- `leaf queries`: what are leaf queries, differences between `match` vs `term`, etc.
- `compound queries`: what are compound queries, examples, etc.

Many more topics will come soon!

## Executing the experiments

In order to execute the experiments, either run them with `pytest` locally or run them with `docker-compose`:

### Running locally

```bash
docker-compose up es  # boots elasticsearch for the experiments
pytest -vv  # runs the experiments (tests)
```

### Running with docker containers

```bash
docker-compose up tests
```
