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
