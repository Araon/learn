# How to use Elastics Search
- Setup a basic getter and setter using python and Elastic search
- used docker to run elastic search locally
- wrote a search query to search for a specific documents
- used score/relevency score to search accross multiple fields in a document


docker command for elastic search
```bash
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" elasticsearch:8.11.0
```