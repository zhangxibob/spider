import requests
from bs4 import BeautifulSoup
# 书店网站
content = requests.get("http://books.toscrape.com/").text
soup = BeautifulSoup(content, "html.parser")

all_titles = soup.findAll("h3")
# print(all_titles)

titles = []
for title in all_titles:
    all_links = title.findAll("a")
    for link in all_links:
        titles.append(link.string)
print(titles)