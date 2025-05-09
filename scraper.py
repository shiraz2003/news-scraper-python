import requests
from bs4 import BeautifulSoup
import csv

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def parse_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []

    for item in soup.select('article'):
        title_tag = item.find('h3')
        link_tag = item.find('a', href=True)

        title = title_tag.text.strip() if title_tag else 'No Title'
        link = link_tag['href'] if link_tag else 'No Link'

        articles.append([title, link])
    return articles

def save_to_csv(articles, filename='articles.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Link'])
            writer.writerows(articles)
        print(f"✅ Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def main():
    url = 'https://www.aljazeera.com/news/'
    html = fetch_page(url)
    if html:
        articles = parse_articles(html)
        save_to_csv(articles)

if __name__ == '__main__':
    main()

