import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

class WebScraper:
    def __init__(self, base_url, sitemap_url, save_folder):
        self.base_url = base_url
        self.sitemap_url = sitemap_url
        self.save_folder = save_folder
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_sitemap(self):
        try:
            response = requests.get(self.sitemap_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            return [loc.text for loc in soup.find_all('loc')]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sitemap: {e}")
            return []

    def extract_data(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            # Check if the response content type is HTML
            content_type = response.headers.get('Content-Type', '').split(';')[0]
            if content_type != 'text/html':
                print(f"Skipping {url} - Not HTML content")
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Select relevant elements: title and text content
            title = soup.title.text if soup.title else ''
            text = ' '.join([p.text for p in soup.find_all('p')])

            return {'title': title, 'content': text}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def save_to_json(self, data, url):
        parsed_url = urlparse(url)
        file_name = f"{parsed_url.netloc.replace('.', '_')}_{parsed_url.path.replace('/', '_')}.json"
        file_name = file_name.strip('_')  # Clean up leading/trailing underscores
        file_path = os.path.join(self.save_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        print(f"Data saved to {file_path}")

    def process_url(self, url):
        data = self.extract_data(url)
        if data:
            self.save_to_json(data, url)

    def process_site(self):
        urls = self.fetch_sitemap()
        for url in urls:
            self.process_url(url)



if __name__ == "__main__":
    base_url = 'https://kobu.agency'
    sitemap_url = 'https://kobu.agency/sitemap.xml'
    save_folder = 'assistant/knowledge/data_store_files/web_scraper_files'

    # Initialize and run the web scraper
    scraper = WebScraper(base_url, sitemap_url, save_folder)
    scraper.process_site()
