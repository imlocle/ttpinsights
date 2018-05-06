from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import ParseHelper


# this function is only for passing in an array of urls
def yelp_store_scraper(urls):
    for url in urls:      
        store_information = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        store_rating = (soup.find("div", attrs={'class': re.compile("i-stars i-stars--large-[\w]+")})["title"])

def yelp_store_review_scraper(url):
        # finding all reviews first
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews_per_page = 20
        total_reviews = ParseHelper.parse_definition('\\{\"reviewCount\": (\\d+),', response.text)
        max_pages_to_scrape = int((int(total_reviews) / reviews_per_page) + 1)
        yelp_reviews = soup.find_all("div", attrs={'class': 'review review--with-sidebar'})
        # looping through each review to get the content
        for i in yelp_reviews:
            #print (i)
            store_name = 'yelp'
            user = i.find('a', attrs={'id':'dropdown_user-name'}).text
            body_review = i.find("p", attrs={'lang':'en'}).text
            rating = ParseHelper.parse_definition('i-stars i-stars--regular-5 rating-large\" title=\"([\d\\.]+)[^\"]+\"', str(i))
            possible_rating = '5'
            location = i.select(".user-location > b")[0].text
            date_review = i.find('span', attrs={'class':'rating-qualifier'}).text.strip()
            helpful = ParseHelper.parse_definition('Useful<\\/span>\\s*<span class=\"count\">(\\d+)<', str(i))
            id_review = ParseHelper.parse_definition('data-review-id=\"([^\"]+)\"', str(i))
            