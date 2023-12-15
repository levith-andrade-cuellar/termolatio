# Wikipedia Category Page Scraper
# Takes Wikipedia Category Pages (where subcategories are loaded with Javascript after opening a toggle) and scrapes articles from all subcategories

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# INPUT FIELDS - modify these
url = "https://es.wikipedia.org/wiki/Categor%C3%ADa:Tecnolog%C3%ADa" #Category page (has toggles that do not reveal until clicked)
scrape_layers = 5 # Number of Tree Layers to Scrape. Minimum 1 for if bullets and not toggles
folder_path = "tech/background" # Folder to save scraped files. Program will generate it if it doesn't exist
# After filling these in, just run python3 scraper.py or python scraper.py


#START
print("Scraping: ", url)
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
driver.get(url)
# Create a list of one-layer list pages
links = [url]

counter = 0

# Parse multi-layer list pages (with category tree toggles)
def CategoryTreeParser(layers):
    global counter
    global categories

    # 1. OPEN ALL CATEGORY TOGGLES
    for n in range(layers):
        sections = driver.find_elements(By.CLASS_NAME, "CategoryTreeSection")

        # Iterate through each section
        for section in sections:
            # print(section.text)
            # Check if the section contains a div with class "CategoryTreeChildren" and style "display:none"
            tree_item = section.find_element(By.CLASS_NAME, "CategoryTreeItem")
            ahref = tree_item.find_element(By.TAG_NAME, "a")

            span_element = tree_item.find_element(By.TAG_NAME, "span")
            class_attribute_value = span_element.get_attribute("class")

            if class_attribute_value == "CategoryTreeBullet":

                span_toggle = span_element.find_element(By.TAG_NAME, "span")
                state_value = span_toggle.get_attribute("data-ct-state")

                if ahref.text and state_value=="collapsed":
                    counter +=1
                    print(counter)
                    span_element.click()
                    # time.sleep(1)
                    if counter > 100:
                        print("Break")
                        break

        spans = driver.find_elements(By.CLASS_NAME, "CategoryTreeEmptyBullet")

    # 2. SCRAPE ALL LINKS TO SINGLE LAYER LIST PAGES
    for span in spans:
        parent = span.find_element(By.XPATH, "..")
        link_element = parent.find_element(By.TAG_NAME, "a")
        # print(link_element.text)
        href_value = link_element.get_attribute("href")
        # print(href_value)
        links.append(href_value)

    print("List Page Links: ", len(links))
    # print("Category Page Links: ")
    # print(links)

#3 SCRAPE LINKS TO ALL THE ARTICLES IN EACH CATEGORY PAGE
def scrapeLinkedPages(wikipedia_link, user_folder_path):
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
                scrapeWikiArticle(link, user_folder_path)

#4 SCRAPE THE ACTUAL WIKI ARTICLE PAGES

#4 SCRAPE THE ACTUAL WIKI ARTICLE PAGES
articles_counter = 0
def scrapeWikiArticle(url, user_folder_path):
    global articles_counter 
    articles_counter = articles_counter + 1
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")

    # Skip articles with a dot in the title
    if '/' in title.text :
        print(f"Skipping article: {title.text}")
        return

    # print(title.text)
    body_content = soup.find(id="bodyContent")
    if body_content:
        # Extract and save text content from <p> tags
        paragraphs = body_content.find_all("p")
        text_content = ''.join(paragraph.get_text() for paragraph in paragraphs)

        # Create a 'scraped' folder if it doesn't exist
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        # Save text content to a file in the 'scraped' folder
        file_path = os.path.join(user_folder_path, f"{title.text.replace(' ', '_')}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)



# run the whole thing
def main (scrape_layers, user_folder_path):
    CategoryTreeParser(scrape_layers)
    for link in links:
        scrapeLinkedPages(link, user_folder_path)
    
    print("Scraped Pages: ", articles_counter)
    print("Done")

main(scrape_layers, folder_path)