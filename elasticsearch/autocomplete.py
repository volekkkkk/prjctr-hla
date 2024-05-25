#!/usr/bin/env python3
import argparse
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://127.0.0.1:9200")

index_name = 'autocomplete'

if not es.indices.exists(index=index_name):
    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "autocomplete_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "autocomplete_filter"]
                    }
                },
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "word": {
                    "type": "completion",
                    "analyzer": "autocomplete_analyzer",
                    "search_analyzer": "standard"
                }
            }
        }
    }
    
    es.indices.create(index=index_name, body=index_settings)

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    
    actions = [
        {
            "_index": index_name,
            "_source": {"word": word}
        }
        for word in words
    ]
    
    helpers.bulk(es, actions)


def autocomplete(query, size=10):
    fuzziness = 'AUTO'
    if len(query) > 7:
        fuzziness = 2

    body = {
        "suggest": {
            "word_suggestion": {
                "prefix": query,
                "completion": {
                    "field": "word",
                    "size": size,
                    "fuzzy": {
                        "fuzziness": fuzziness
                    }
                }
            }
        }
    }
    response = es.search(index=index_name, body=body)

    suggestions = response['suggest']['word_suggestion'][0]['options']
    
    return [suggestion['_source']['word'] for suggestion in suggestions]

def main(args):
    if args.init_data:
        print("loading dictionary to database...")
        load_words(args.words_source)
        
    while True:
        query = input("search: ")
        suggestions = autocomplete(query)
        print(suggestions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("words_source")
    parser.add_argument("--init-data", action="store_true")

    main(parser.parse_args())


