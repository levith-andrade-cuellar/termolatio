import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
# Navigate to url
url = "https://es.wikipedia.org/wiki/Categor%C3%ADa:Charcuter%C3%ADa"

className = "CategoryTreeBullet"
itemName = "CategoryTreeItem"

driver.get(url)

# 1. OPEN ALL CATEGORIES
i = 0
links = [url]
# Find all divs with class "CategoryTreeSection"
for i in range(3):
    sections = driver.find_elements(By.CLASS_NAME, "CategoryTreeSection")

    # Iterate through each section
    for section in sections:
        print(section.text)
        # Check if the section contains a div with class "CategoryTreeChildren" and style "display:none"
        tree_item = section.find_element(By.CLASS_NAME, "CategoryTreeItem")
        ahref = tree_item.find_element(By.TAG_NAME, "a")

        span_element = tree_item.find_element(By.TAG_NAME, "span")
        class_attribute_value = span_element.get_attribute("class")

        if class_attribute_value == "CategoryTreeBullet":
            print("Cat Tree Bull found")
            print(span_element.get_attribute("class"))

            span_toggle = span_element.find_element(By.TAG_NAME, "span")
            # print(span_toggle.get_attribute("data-ct-state")
            state_value = span_toggle.get_attribute("data-ct-state")

            print(state_value)

            print(ahref.text)
            if ahref.text and state_value=="collapsed":
                span_element.click()
                i = i+1
                print("clicked: ", i)
                time.sleep(3)

print('SDFASFSA')

spans = driver.find_elements(By.CLASS_NAME, "CategoryTreeEmptyBullet")

for span in spans:
    parent = span.find_element(By.XPATH, "..")
    link_element = parent.find_element(By.TAG_NAME, "a")
    print(link_element.text)
    href_value = link_element.get_attribute("href")
    print(href_value)
    links.append(href_value)

print(links)

# 2. SCRAPE ALL LINKS TO CATEGORY PAGES

#3 SCRAPE LINKS TO ALL THE PAGES IN EACH CATEGORY PAGE

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

# SCRAPE THE ACTUAL WIKI PAGES

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
        folder_path = 'scraped/foreground'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save text content to a file in the 'scraped' folder
        file_path = os.path.join(folder_path, f"{title.text.replace(' ', '_')}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)



for link in links:
   scrapeLinkedPages(link, 100)
