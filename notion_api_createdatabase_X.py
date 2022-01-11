import requests
from selenium import webdriver
import gdown
import json
import re

NOTION_TOKENS = ''

NOTION_DATABASE_ID = ''


NOTION_HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKENS,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

SITE_PASSWORD = ''
SITE_LOGIN = ''

browser = webdriver.Chrome()

def create_page(DatabaseId, headers, posterName, posterTitle):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": DatabaseId },
        "properties": {
            "Authors": {
                "rich_text": [
                    {
                        "text": {
                            "content": posterName
                        }
                    }
                ]
            },
            "tytul": {
                "title": [
                    {
                        "text": {
                            "content": posterTitle
                        }
                    }
                ]
            }
            
        }
    }
    
    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)

def download_with_name(link, author):
    file_id = link
    filename = author + '.pdf'
    url = 'https://drive.google.com/uc?id=' + file_id
    gdown.download(url, filename, quiet=False)

def log_in_into_site(login, password, url):
    browser.get(url)
    userElem = browser.find_element_by_xpath("""//*[(@id = "login-user_1")]""")
    userElem.send_keys(login)
    passwordElem = browser.find_element_by_xpath("""//*[(@id = "login-pass_1")]""")
    passwordElem.send_keys(password)
    passwordElem.submit()

homepage_url = 'https://anfarch.ucsd.edu/login-page'
log_in_into_site(SITE_LOGIN, SITE_PASSWORD, homepage_url)

urls_to_parse = ['https://anfarch.ucsd.edu/Poster-Session-II', 'https://anfarch.ucsd.edu/Poster-Session-II', 'https://anfarch.ucsd.edu/Poster-Session-III']
for anfaURL in urls_to_parse:
    res = browser.get(anfaURL)
    all_titles = browser.find_elements_by_xpath("""//*[contains(concat( " ", @class, " " ), concat( " ", "poster-title", " " ))]""")
    all_titl_str = [str(postitle.text) for postitle in all_titles]

    all_authors = browser.find_elements_by_xpath("""//*[contains(concat( " ", @class, " " ), concat( " ", "poster-author", " " ))]""")
    all_auth_str = [str(author.text) for author in all_authors]

    all_links = browser.find_elements_by_link_text("View")
    all_href_links = [str(link.get_attribute("href")) for link in all_links]
    print(all_href_links)

    all_short_href_links = []
    for link in all_href_links:
        data = link
        regex = """^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)"""
        matches = re.findall(regex, data) 
        matchestuplelist = list(matches[0])
        shortlink = matchestuplelist[3].replace('/', '').replace('filed', '')
        all_short_href_links.append(shortlink)


    for author, link in zip(all_auth_str, all_short_href_links):
        shortauthor = author.replace(' ', '').replace(',', '').lower()
        download_with_name(link, shortauthor)

for author, postitle, link in zip(all_auth_str, all_titl_str):
    posterName = author
    posterTitle = postitle
    create_page(NOTION_DATABASE_ID, NOTION_HEADERS, posterName, posterTitle)


