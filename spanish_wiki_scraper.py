import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrapeLinkedPages(wikipedia_link, max_articles):
    if max_articles == 0:
        return

    response = requests.get(wikipedia_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    list_items = soup.find_all('li')
    for li in list_items:
        # Check if the li tag is within a div with class mw-category-group
        parent_div = li.find_parent('div', class_='mw-category-group')
        if parent_div:
            a_tag = li.find('a')
            if a_tag:
                link = urljoin(wikipedia_link, a_tag['href'])
                scrapeWikiArticle(link, max_articles)

                # Reduce the count of articles to scrape
                max_articles -= 1
                if max_articles == 0:
                    break

def scrapeWikiArticle(url, max_articles):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    print(title.text)

    body_content = soup.find(id="bodyContent")
    if body_content:
        # Extract and save text content from <p> tags
        paragraphs = body_content.find_all("p")
        text_content = ''.join(paragraph.get_text() for paragraph in paragraphs)

        # Create a 'scraped' folder if it doesn't exist
        folder_path = 'scraped'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save text content to a file in the 'scraped' folder
        file_path = os.path.join(folder_path, f"{title.text.replace(' ', '_')}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)

# Example usage with a limit of 5 articles
scrapeLinkedPages("https://es.wikipedia.org/wiki/Categor%C3%ADa:Platos_con_chorizo", max_articles=13)
