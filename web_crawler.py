import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_title_and_links(url):
    """
    Returns the title of the webpage and a list of links from the given webpage URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.find('title').get_text() if soup.title else 'No title'

        # Extract links
        links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href')]
        return title, links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return 'Error', []

def crawl_for_titles(start_url, max_depth=3, max_titles=100):
    """
    Crawls web pages starting from a start URL and extracts titles.

    Args:
    - start_url (str): The starting URL
    - max_depth (int): Maximum depth to crawl
    - max_titles (int): Maximum number of titles to collect

    Returns:
    - titles (list): List of page titles
    """
    visited = set()
    titles = []
    to_visit = [(start_url, 0)]

    while to_visit and len(titles) < max_titles:
        url, depth = to_visit.pop(0)
        if depth > max_depth:
            continue

        if url not in visited:
            print(f"Crawling: {url}")
            visited.add(url)

            title, links = get_title_and_links(url)
            titles.append((url, title))

            for link in links:
                if link not in visited and len(titles) < max_titles:
                    to_visit.append((link, depth + 1))

    return titles

# Start crawling from a specific URL and get titles
scraped_data = crawl_for_titles("https://www.example.com", max_depth=2, max_titles=100)

# Create a DataFrame from the scraped data
df = pd.DataFrame(scraped_data, columns=['URL', 'Title'])
print(df)
