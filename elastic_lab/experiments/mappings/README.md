# Experiments: Mappings

Mapping is the process of defining how documents fields will be stored and indexed. They define:

- which string fields are to be treated as `full text` fields;
- which fields contain `numbers`, `dates` or even `geolocations`;
- format of date values;
- custom rules for `dynamically added fields`

Hence, roughly, it's used to define the data types and shapes that each field of document will use.

## Dynamic mappings

Fields and mapping types do not need to be defined before being created/used. `Dynamic typing` will detect and try
to guess new fields types as they are indexed!

Some dynamic rules can be customized.

## Explicit mappings

Usually we know more about the data type than Elasticsearch can guess. Hence, dynamic mapping is a great start point but
we can fine tune the define types **explicitly**.

### Explicit mappings can be created using INDEX CREATION api:

```text
PUT /new-index-000001
{
  "mappings": {
    "properties": {
      "age":    { "type": "integer" },
      "email":  { "type": "keyword"  },
      "name":   { "type": "text"  }
    }
  }
}
```

### Explicit mappings can be added to an existing API

In this case, the index already exists with some mapping (even if just the dynamic one). In the following example, the field name
`employee-id` is stored but not indexed/returned by searches:

```
PUT /my-index-000001/_mapping
{
  "properties": {
    "employee-id": {
      "type": "keyword",
      "index": false
    }
  }
}
```

However, this only adds new types, but it's not possible to **change a mapping type** of an existing field as this could break previously saved data.

In order to change the type of a field that already exists -> reindex data into a new index with appropriate type.

### Alias for document fields

Alias exist for both indexes and document fields. For document fields, the `mapping API` can be used to add an alias to an existing document field:

```text
PUT index
{
  "mappings": {
    "properties": {
      "distance": {
        "type": "long"
      },
      "route_length_miles": {
        "type": "alias",
        "path": "distance" ---> 'distance' field also points to the 'route_lenght_miles' field
      }
    }
  }
}
```

### Date formats

By default, Elasticsearch stores datetimes using `epoch_millis` which is milliseconds-since-the-epoch in **UTC**: yes, all dates are stored in UTC.

`PS`: The Unix epoch is `00:00:00 UTC` on `1 January 1970` (an arbitrary date)

Many built-in formats are supported:

- [built-in datetime formats](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats)
- [custom datetime formats](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html)

Specifying a datetime format:

```text
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "date": {
        "type":   "date",
        "format": "yyyy-MM-dd" --> date math is supported
      }
    }
  }
}
```
