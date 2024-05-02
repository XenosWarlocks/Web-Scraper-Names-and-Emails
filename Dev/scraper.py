# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class Scraper:
    def __init__(self, url):
        self.url = url

    def visit_url(self, url=None):
        try:
            if url is None:
                url = self.url
            response = requests.get(url)
            if response.status_code == 200:
                # print("Successfully landed on", url)
                return response.content
            else:
                print("Failed to land on", url)
                return None
        except requests.RequestException as e:
            print("An error occurred while visiting the URL:", e)
            return None

    def extract_links(self, content):
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            lightsaber_links = soup.find_all('a', class_='lightsaber-link')
            return lightsaber_links
        else:
            return []

    def extract_name(self, link):
        return link.text.strip() if link else None

    def extract_email(self, content):
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            email_div = soup.find('div', class_='email-address__address label-above')
            if email_div:
                email_link = email_div.find('a')
                if email_link:
                    return email_link.text.strip()
        return None

    def scrape(self):
        content = self.visit_url()
        links = self.extract_links(content)
        names_emails = []
        for link in links:
            time.sleep(1)  # Add a delay to avoid overloading the server
            full_url = urljoin(self.url, link.get('href'))
            sub_content = self.visit_url(full_url)
            name = self.extract_name(link)
            email = self.extract_email(sub_content)
            names_emails.append((name, email))
            if not email:
                print(f"No email found for {name}")
        return names_emails
