# Text Analysis

Text analysis is the process of converting unstructured text into a structured format that is **optmized for search.** The analysis is performed either during:

- indexing time;
- searching time

And is performed by built-in or customized text analyzers.

## Analyzers

Analyzers are composed of three main parts:

- Character filter
- Tokenizer
- Token filter

### Character filter

```text
"Quick\t\tbrown\t\tfox!" ---> | Char filter (removes \t) | ---> "Quickbrownfox!"
```

The filter receives the original **characters stream** and performs changes on this stream such as adding, striping or changing the
chars. This is like pre-processing the text.

The analyzer can have zero or more character filters, which are applied in order.

### Tokenizer

Much like what is done by lexical analyzer of programming languages, the tokenizer receives the **characters stream** and extracts **tokens** from this stream. Moreover, it saves the order/position of every token of the text.

For example, the `whitespace` character breaks text into every whitespace:

```text
"Quickbrownfox!" --> | Tokenizer (whitespace) | ---> ["Quick", "brown", "fox!"]
```

The analyze must have at least **one tokenizer**.

### Token filter

```text
["Quick", "brown", "fox!"] --> | Token filters (lowercase, synonym) | ---> ["quick", "fast", "brown", "fox!"]
```

The token filter is similar to the character filter, but receives the generated tokens instead. The filter can add or remove common tokens. For example:

- `lowercase token filter`: changes all tokens by lowercasing them;
- `stop token filter`: removes common words such as "the";
- `synonym token filter`: adds synonyms to the token stream;

The analyzer can have zero or more token filters, which are applied in order.

## Default Analyzer

Elasticsearch comes with a default text analyzer which roughly uses:

- `standard tokenizer`: grammar based tokenization which works well in most languages (removes most punctuation);
- `lower case token filter`: lowercases every extracted token;
- `stop token filter`: **disabled** by default, but removes "common words" in english but there are extensions for many other languages

## Custom Analyzers

Customs analyzers can be created for each desired index by make a PUT to the index settings. Morever, the customized analyzer can be tested using the `_analyze` route:

```text
# customizes the analyzer
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_english_analyzer": {
          "type": "standard",
          "max_token_length": 5,
          "stopwords": "_english_"
        }
      }
    }
  }
}

# tests the analyzer
POST my-index-000001/_analyze
{
  "analyzer": "my_english_analyzer",
  "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
}
```
