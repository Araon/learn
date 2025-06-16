"""
Elasticsearch Country Search Example

This module demonstrates how to use Elasticsearch for indexing and searching country data.
It fetches country information from the REST Countries API and provides various search operations.
"""

import time
from typing import Dict, List, Optional, Any, Tuple
import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ELASTICSEARCH_HOST = "http://localhost:9200"
INDEX_NAME = "countries"
API_BASE_URL = "https://restcountries.com/v3.1"


class CountrySearchService:
    """Service class for managing country data in Elasticsearch."""
    
    def __init__(self, es_client: Elasticsearch, index_name: str = INDEX_NAME):
        """
        Initialize the CountrySearchService.
        
        Args:
            es_client: Elasticsearch client instance
            index_name: Name of the index to use
        """
        self.es_client = es_client
        self.index_name = index_name
        
    def create_index_with_mapping(self) -> None:
        """Create the countries index with proper field mappings."""
        country_mapping = {
            "properties": {
                "name_common": {"type": "text"},
                "name_official": {"type": "text"},
                "region": {"type": "keyword"},
                "subregion": {"type": "keyword"},
                "capital": {"type": "text"},
                "population": {"type": "integer"},
                "area": {"type": "float"}
            }
        }
        
        if self.es_client.indices.exists(index=self.index_name):
            logger.info(f"Deleting existing index: {self.index_name}")
            self.es_client.indices.delete(index=self.index_name)
        
        logger.info(f"Creating new index: {self.index_name} with mappings")
        self.es_client.indices.create(index=self.index_name, mappings=country_mapping)

    def fetch_countries_data(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch country data from the REST Countries API.
        
        Returns:
            List of country dictionaries or None if fetch fails
        """
        try:
            fields = "name,region,subregion,capital,population,area"
            url = f"{API_BASE_URL}/all?fields={fields}"
            response = requests.get(url)
            response.raise_for_status()
            
            logger.info("Successfully fetched data from REST Countries API")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch country data: {e}")
            return None

    def process_and_index_data(self, country_data: List[Dict[str, Any]]) -> bool:
        """
        Process and bulk index country data into Elasticsearch.
        
        Args:
            country_data: List of country dictionaries from the API
            
        Returns:
            True if indexing was successful, False otherwise
        """
        actions = []
        
        for i, country in enumerate(country_data):
            doc = {
                "name_common": country.get('name', {}).get('common', ''),
                "name_official": country.get('name', {}).get('official', ''),
                "region": country.get('region', 'N/A'),
                "subregion": country.get('subregion', 'N/A'),
                "capital": ", ".join(country.get('capital', [])),  # Capital is a list
                "population": country.get('population', 0),
                "area": country.get('area', 0.0)
            }
            
            action = {
                "_index": self.index_name,
                "_id": i,
                "_source": doc
            }
            actions.append(action)
        
        logger.info(f"Preparing to index {len(actions)} documents...")
        
        try:
            success, failed = bulk(self.es_client, actions)
            if failed:
                logger.warning(f"Failed to index {len(failed)} documents")
                return False
            
            logger.info(f"Successfully indexed {len(actions)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error during bulk indexing: {e}")
            return False

    def search_countries_by_name(self, query_text: str) -> None:
        """
        Search for countries by name using wildcard query.
        
        Args:
            query_text: Text to search for in country names
        """
        logger.info(f"Searching for countries with '{query_text}' in their name...")
        
        query = {
            "wildcard": {
                "name_common": f"*{query_text}*"
            }
        }
        
        try:
            response = self.es_client.search(index=self.index_name, query=query)
            hits_count = response['hits']['total']['value']
            
            logger.info(f"Found {hits_count} matching countries:")
            for hit in response['hits']['hits']:
                print(f"  - {hit['_source']['name_common']}")
                
        except Exception as e:
            logger.error(f"Error during search: {e}")

    def search_by_region_and_population(self, region: str, min_population: int) -> None:
        """
        Search for countries by region with minimum population filter.
        
        Args:
            region: Region to filter by
            min_population: Minimum population threshold
        """
        logger.info(f"Searching for countries in '{region}' with population > {min_population:,}...")
        
        query = {
            "bool": {
                "must": {
                    "range": {
                        "population": {"gt": min_population}
                    }
                },
                "filter": {
                    "term": {
                        "region": region
                    }
                }
            }
        }
        
        try:
            response = self.es_client.search(index=self.index_name, query=query)
            hits_count = response['hits']['total']['value']
            
            logger.info(f"Found {hits_count} matching countries:")
            for hit in response['hits']['hits']:
                name = hit['_source']['name_common']
                population = hit['_source']['population']
                print(f"  - {name} (Population: {population:,})")
                
        except Exception as e:
            logger.error(f"Error during search: {e}")

    def aggregate_countries_by_subregion(self) -> None:
        """Aggregate and display country counts by subregion."""
        logger.info("Aggregating country counts by subregion...")
        
        query_body = {
            "size": 0,  # We don't need actual documents, just aggregation results
            "aggs": {
                "subregion_count": {
                    "terms": {
                        "field": "subregion"
                    }
                }
            }
        }
        
        try:
            response = self.es_client.search(index=self.index_name, body=query_body)
            buckets = response['aggregations']['subregion_count']['buckets']
            
            print("\nCountry count per subregion:")
            for bucket in buckets:
                subregion = bucket['key']
                count = bucket['doc_count']
                print(f"  - {subregion}: {count} countries")
                
        except Exception as e:
            logger.error(f"Error during aggregation: {e}")

    def interactive_search(self) -> None:
        """
        Interactive search loop that allows users to search for countries, regions, or continents.
        Users can enter 'quit' or 'exit' to stop the loop.
        """
        print("\n" + "="*60)
        print("Interactive Country Search")
        print("="*60)
        print("Search for countries, regions, subregions, or continents!")
        print("Type 'quit' or 'exit' to stop.")
        print("-" * 60)
        
        while True:
            try:
                # Get user input
                query = input("\nEnter your search query: ").strip()
                
                # Check for exit commands
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\nThanks for using Country Search! Goodbye!")
                    break
                
                if not query:
                    print("Please enter a search term.")
                    continue
                
                # Perform the search
                self._perform_comprehensive_search(query)
                
            except KeyboardInterrupt:
                print("\n\nThanks for using Country Search! Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error during interactive search: {e}")
                print(f"An error occurred: {e}")

    def _perform_comprehensive_search(self, query: str) -> None:
        """
        Perform a comprehensive search across multiple fields.
        
        Args:
            query: The search query from the user
        """
        print(f"\nSearching for: '{query}'...")
        
        # Multi-field search query
        search_query = {
            "bool": {
                "should": [
                    # Exact matches (higher boost)
                    {"match": {"name_common": {"query": query, "boost": 3.0}}},
                    {"match": {"name_official": {"query": query, "boost": 2.5}}},
                    {"term": {"region": {"value": query, "boost": 2.0}}},
                    {"term": {"subregion": {"value": query, "boost": 2.0}}},
                    {"match": {"capital": {"query": query, "boost": 1.8}}},
                    
                    # Partial matches (lower boost)
                    {"wildcard": {"name_common": {"value": f"*{query.lower()}*", "boost": 1.5}}},
                    {"wildcard": {"name_official": {"value": f"*{query.lower()}*", "boost": 1.2}}},
                    {"wildcard": {"capital": {"value": f"*{query.lower()}*", "boost": 1.0}}}
                ],
                "minimum_should_match": 1
            }
        }
        
        try:
            response = self.es_client.search(
                index=self.index_name, 
                query=search_query, 
                size=20,  # Limit results
                sort=[{"_score": {"order": "desc"}}]  # Sort by relevance
            )
            
            hits = response['hits']['hits']
            total_hits = response['hits']['total']['value']
            
            if total_hits == 0:
                print("No results found. Try a different search term.")
                self._show_search_suggestions()
                return
            
            print(f"Found {total_hits} result(s):")
            print("-" * 50)
            
            for i, hit in enumerate(hits, 1):
                source = hit['_source']
                score = hit['_score']
                
                print(f"\nResult {i} (Relevance: {score:.2f})")
                print(f"Country: {source['name_common']}")
                
                if source['name_official'] != source['name_common']:
                    print(f"Official Name: {source['name_official']}")
                
                print(f"Region: {source['region']}")
                print(f"Subregion: {source['subregion']}")
                
                if source['capital']:
                    print(f"Capital: {source['capital']}")
                
                if source['population'] > 0:
                    print(f"Population: {source['population']:,}")
                
                if source['area'] > 0:
                    print(f"Area: {source['area']:,} km²")
                
                if i < len(hits):  # Don't print separator after last result
                    print("-" * 30)
                    
        except Exception as e:
            logger.error(f"Error during comprehensive search: {e}")
            print(f"Search failed: {e}")

    def _show_search_suggestions(self) -> None:
        """Show some search suggestions to help users."""
        print("\nSearch suggestions:")
        print("  • Try country names: 'Finland', 'Brazil', 'Japan'")
        print("  • Try regions: 'Europe', 'Africa', 'Asia'")
        print("  • Try subregions: 'Northern Europe', 'Caribbean', 'Western Africa'")
        print("  • Try capitals: 'Paris', 'Tokyo', 'London'")
        print("  • Use partial names: 'land' (finds Finland, Thailand, etc.)")

    def run_interactive_search(self) -> None:
        """Run the interactive search loop."""
        self.interactive_search()


def main() -> None:
    """Main function to demonstrate Elasticsearch operations."""
    # Initialize Elasticsearch client
    try:
        es_client = Elasticsearch(hosts=[ELASTICSEARCH_HOST])
        
        # Test connection
        if not es_client.ping():
            logger.error("Failed to connect to Elasticsearch")
            return
            
        logger.info("Successfully connected to Elasticsearch")
        
    except Exception as e:
        logger.error(f"Failed to initialize Elasticsearch client: {e}")
        return
    
    # Initialize service
    service = CountrySearchService(es_client, INDEX_NAME)
    
    # Create index and mapping
    service.create_index_with_mapping()
    
    # Fetch and index country data
    country_data = service.fetch_countries_data()
    if not country_data:
        logger.error("Failed to fetch country data, exiting...")
        return
    
    if not service.process_and_index_data(country_data):
        logger.error("Failed to index country data, exiting...")
        return
    
    # Wait for indexing to complete
    time.sleep(1)
    
    logger.info("\n" + "="*50)
    logger.info("Running search scenarios...")
    logger.info("="*50)
    
    # Example searches (uncomment to run)
    # service.search_countries_by_name("land")
    # service.search_by_region_and_population("Africa", 50_000_000)
    # service.aggregate_countries_by_subregion()

    # Run interactive search
    service.run_interactive_search()


if __name__ == "__main__":
    main()
