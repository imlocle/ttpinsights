

```python
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
import re
import requests
import datetime as dt
import time
```


```python
"""
This function is to parse out content using a regular expression pattern from a string.
<param>regex_pattern</param>
<param>string</param>
"""

def parse_definition(regex_pattern, string):
    result = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    # Checking if the patten works for the string
    if not result.search(string):
        return "None"
    else:
        return result.search(string).group(1)
```


```python
# Example store
url = "https://www.yelp.com/biz/kempt-mens-hair-irvine-2?osq=kempt"
```


```python
my_dict = {"user": [],
            "body_review": [],
            "rating": [],
            "possible_rating": [],
            "location": [],
            "date_review": [],
            "useful": [],
            "id_review": [],
            "source": []}
```


```python
#Grabbing HTML content
response = requests.get(url)
soup = bs(response.text, 'html.parser')
reviews_per_page = 20
total_reviews = int(parse_definition('\\{\"reviewCount\": (\\d+),', response.text))
max_pages_to_scrape = int((total_reviews / reviews_per_page) + 1)
yelp_reviews = soup.find_all("div", attrs={'class': 'review review--with-sidebar'})
store_name = soup.find("h1", attrs={'class':'biz-page-title'}).text.strip()
review_pages = 1
```


```python
print(f"Total Reviews: {total_reviews}")
print(f"Expected Review Pages: {max_pages_to_scrape}")
```

    Total Reviews: 70
    Expected Review Pages: 4



```python
while review_pages <= max_pages_to_scrape:
    print(f"Review Page: {review_pages}")
    yelp_reviews = soup.find_all("div", attrs={'class': 'review review--with-sidebar'})
    #looping through each review to get the content
    for i in yelp_reviews:
        user = i.find('a', attrs={'id':'dropdown_user-name'}).text    
        body_review = i.find("p", attrs={'lang':'en'}).text  
        rating = parse_definition('i-stars i-stars--regular-[^\"]+\" title=\"([\d\\.]+)[^\"]+\"', str(i))    
        location = i.select(".user-location > b")[0].text    
        date_review = parse_definition("<span class=\"rating-qualifier\">\s*([\d\\/]+)[^<]+<", str(i))
        useful = parse_definition('Useful<\\/span>\\s*<span class=\"count\">(\\d+)<', str(i))    
        id_review = parse_definition('data-review-id=\"([^\"]+)\"', str(i))

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
        review_pages+=1
        next_page_url = soup.find("a", class_="u-decoration-none next pagination-links_anchor").attrs['href']
        # Sleep for 3 seconds to avoid blocks
        time.sleep(3)
        response = requests.get(next_page_url)
        soup = bs(response.text, 'html.parser')
    except:
        break
```

    Review Page: 1
    Review Page: 2
    Review Page: 3
    Review Page: 4



```python
# Checking how many users
# Length should match total_reviews
users = my_dict["user"]
if len(users) != total_reviews:
    print(f"Please check crawler. Length of users, {len(users)}, don't match total reviews, {total_reviews}.")
else:
    print(f"Scrape completed! Length of users, {len(users)}, matches with the total reviews, {total_reviews}.")
```

    Scrape completed! Length of users, 70, matches with the total reviews, 70.



```python
yelp_reviews_df = pd.DataFrame(my_dict)
yelp_reviews_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>body_review</th>
      <th>date_review</th>
      <th>id_review</th>
      <th>location</th>
      <th>possible_rating</th>
      <th>rating</th>
      <th>source</th>
      <th>useful</th>
      <th>user</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>I've been waiting for my 3rd cut to post this,...</td>
      <td>5/30/2018</td>
      <td>VQhZMCY6b7jKyr-HDbrRaQ</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Brian L.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>I have been to KEMPT twice and both experience...</td>
      <td>5/2/2018</td>
      <td>jaL8RSQ0SsxagLiNq0G1Pg</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Daniel E.</td>
    </tr>
    <tr>
      <th>2</th>
      <td>I went on yelp, messaged 3 different salons an...</td>
      <td>4/27/2018</td>
      <td>O2hNoxxyvwPONcWoWkBp0w</td>
      <td>Santa Ana, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>jesse n.</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Found this place for my boyfriend and let me t...</td>
      <td>6/14/2018</td>
      <td>7b-FVnYllrQGBbivJlP4UQ</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Olivia C.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Well i feel really satisfied with my new hair ...</td>
      <td>6/15/2018</td>
      <td>8xg0pEpGQU1L8sNH2s6LCg</td>
      <td>Westminster, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>José A.</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Saving into a csv file
yelp_reviews_df.to_csv(f"reviews/{store_name.replace(' ','_')}.csv", encoding='utf-8')
```
