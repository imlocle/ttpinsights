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
        #finding all reviews first
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews_per_page = 20
        total_reviews = ParseHelper.parse_definition('\\{\"reviewCount\": (\\d+),', response.text)
        max_pages_to_scrape = int((int(total_reviews) / reviews_per_page) + 1)
        yelp_reviews = soup.find_all("div", attrs={'class': 'review review--with-sidebar'})
        #looping through each review to get the content
        for i in yelp_reviews:
        #    append to all_reviews_list if you want
        #    review_id = (soup.find('div', attrs={'class': 'review review--with-sidebar'})['data-review-id'])
        #    review_rating = (soup.find(attrs={"class":"i-stars i-stars--large-5 rating-very-large"})["title"])
            #print (review_rating)
            #print (review_id)

            #only breaking to print out one for now
        #    break