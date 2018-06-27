from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import time
import ParseHelper, ReviewScraper

# this function is only for passing in an array of urls
def yelp_store_scraper(urls):
    for url in urls:      
        store_information = []
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        store_rating = (soup.find("div", attrs={'class': re.compile("i-stars i-stars--large-[\w]+")})["title"])

def yelp_store_review_scraper(url):
    my_dict = {"user": [],
            "body_review": [],
            "rating": [],
            "possible_rating": [],
            "location": [],
            "date_review": [],
            "useful": [],
            "id_review": [],
            "source": []}
    
    review_pages = 0
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    reviews_per_page = 20
    total_reviews = int(ParseHelper.parse_definition('\\{\"reviewCount\": (\\d+),', response.text))
    max_pages_to_scrape = (total_reviews / reviews_per_page) + 1)

    while review_pages <= max_pages_to_scrape:
        yelp_reviews = soup.find_all("div", attrs={'class': 'review review--with-sidebar'})
        #looping through each review to get the content
        for i in yelp_reviews:
            user = i.find('a', attrs={'id':'dropdown_user-name'}).text    
            body_review = i.find("p", attrs={'lang':'en'}).text  
            rating = ParseHelper.parse_definition('i-stars i-stars--regular-[^\"]+\" title=\"([\d\\.]+)[^\"]+\"', str(i))    
            location = i.select(".user-location > b")[0].text    
            date_review = ParseHelper.parse_definition("<span class=\"rating-qualifier\">\s*([\d\\/]+)[^<]+<", str(i))
            useful = ParseHelper.parse_definition('Useful<\\/span>\\s*<span class=\"count\">(\\d+)<', str(i))    
            id_review = ParseHelper.parse_definition('data-review-id=\"([^\"]+)\"', str(i))

            if id_review in my_dict["id_review"]:
                pass

            my_dict["user"].append(user)
            my_dict["body_review"].append(body_review)
            my_dict["rating"].append(float(rating))
            my_dict["possible_rating"].append(5.0)
            my_dict["location"].append(location)
            my_dict["date_review"].append(date_review)
            my_dict["useful"].append(useful)
            my_dict["id_review"].append(id_review)
            my_dict["source"].append("yelp")
        try:
            next_page_url = soup.find("a", class_="u-decoration-none next pagination-links_anchor").attrs['href']
            time.sleep(3)
            response = requests.get(next_page_url)
            soup = bs(response.text, 'html.parser')
            review_pages+=1
            print(review_pages)
        except:
            break

    yelp_reviews_df = pd.DataFrame(my_dict)
    store_name = soup.find("h1", attrs={'class':'biz-page-title'}).text.strip()
    # Saving reviews to CSV
    yelp_reviews_df.to_csv(f"reviews/{store_name.replace(' ','_')}.csv", encoding='utf-8')
