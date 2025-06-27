import os
import requests
from bs4 import BeautifulSoup

def scrape_and_create_folders(url, output_dir="examples"):
    """
    Scrapes the main example links from gobyexample.com,
    and creates a numbered sub-folder for each example to maintain order.

    Args:
        url (str): The URL of the Go by Example homepage.
        output_dir (str): The name of the main directory to store the sub-folders.
    """
    print(f"Starting scraper for: {url}")

    try:
        # 1. Fetch the HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the URL. {e}")
        return

    # 2. Create the main output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created main directory: '{output_dir}{os.sep}'")
    else:
        print(f"Main directory '{output_dir}{os.sep}' already exists.")

    # 3. Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. Find all the links within the main examples list
    example_list = soup.select_one('#intro > ul')
    
    if not example_list:
        print("Error: Could not find the example list on the page.")
        return

    links = example_list.find_all('a')
    
    if not links:
        print("No example links found in the list.")
        return

    print(f"\nFound {len(links)} example links. Creating sub-folders...")

    # 5. Loop through each link to create a folder with a numbered prefix
    for index, link in enumerate(links, 1): # Use enumerate to get a counter starting from 1
        href = link.get('href')
        
        # Check if the link is relative (doesn't start with http)
        if href and not href.startswith('http'):
            stub = href.strip('/')

            if not stub: # Skip if the stub is empty
                continue

            # Create a prefixed folder name, e.g., "01-hello-world"
            # The :02d formats the number to have a leading zero if it's less than 10
            folder_name = f"{index:02d}-{stub}"
            
            # Create a full path for the new folder
            folder_path = os.path.join(output_dir, folder_name)

            # Create the sub-folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"  - Created folder: {folder_path}")
            else:
                print(f"  - Folder already exists: {folder_path}")

    print("\nScript finished successfully!")


# --- Main execution block ---
if __name__ == "__main__":
    target_url = "https://gobyexample.com/"
    scrape_and_create_folders(target_url)