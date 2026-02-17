from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

print(f"Connected to Elasticsearch {es.info()['version']['number']}")

book_doc = {
    'title': 'The Hitchhiker\'s Guide to the Galaxy',
    'author': 'Douglas Adams',
    'publication_year': 1979,
    'genre': 'Science Fiction'
}

# try:
#     response = es.index(
#         index='books',
#         id=1,
#         document=book_doc
#     )
#     print(response)
# except Exception as e:
#     print(f"Error indexing document: {e}")

print("getting a document by ID")

try:
    response = es.get(index='books', id=1)
    print(response['_source'])

except Exception as e:
    print(f"Error getting document: {e}")
    