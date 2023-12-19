import requests
from bs4 import BeautifulSoup
import random
import os
from time import sleep

def scrapeWikiArticle(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')

    a_tags = soup.find_all('a', href=True)
    allLinks = []
    for a in a_tags:
        href = a['href']
        if href.startswith("/wiki/"):
            allLinks.append(href)

    random.shuffle(allLinks)        

    for link in allLinks[:50]:
        sleep(5)
        linkToScrape = "https://fr.wikipedia.org" + link
        response = requests.get(url=linkToScrape)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id="firstHeading").text.replace(' ', '_')  
        if not os.path.exists("articles"):
            os.mkdir("articles")
            
        with open(f"articles/{title}.txt", "w", encoding="utf-8") as f:
            for paragraph in soup.find_all('p'):
                text = paragraph.text.strip().replace('\n', ' ')
                f.write(' '.join(text.split()).lower() + '\n')

scrapeWikiArticle("https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Liste_d%27articles_que_toutes_les_encyclop%C3%A9dies_devraient_avoir")