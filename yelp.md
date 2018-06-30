

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
print(total_reviews)
print(max_pages_to_scrape)
```

    70
    4



```python
while review_pages <= max_pages_to_scrape:
    print(review_pages)
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

    1
    2
    3
    4



```python
# Checking how many users
# Length should match total_reviews
len(my_dict["user"])
```




    70




```python
yelp_reviews_df = pd.DataFrame(my_dict)
yelp_reviews_df
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
    <tr>
      <th>5</th>
      <td>Great place to get a haircut! Definitely recom...</td>
      <td>6/9/2018</td>
      <td>lEB_NFVF0PxUc8lpcBLATg</td>
      <td>Phoenix, AZ</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Anurag G.</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Booked this place for my hubby to get a haircu...</td>
      <td>6/4/2018</td>
      <td>cAhaEQC1yX-hIenL1-t0Ew</td>
      <td>Newport Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Mehak B.</td>
    </tr>
    <tr>
      <th>7</th>
      <td>KEMPT is legit and worth every penny. I've bee...</td>
      <td>6/9/2018</td>
      <td>pm3UDlmwD9q-NpoVZ6pU3w</td>
      <td>Huntington Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Tyler K.</td>
    </tr>
    <tr>
      <th>8</th>
      <td>I've had 3 cuts from Carley, and she's done an...</td>
      <td>6/20/2018</td>
      <td>a1FOU8tMjfxYqtZj402nnQ</td>
      <td>Wheaton, IL</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Robert B.</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Very friendly atmosphere. Went here after my l...</td>
      <td>5/8/2018</td>
      <td>6OGJYgu_sf7SrJAzFObpag</td>
      <td>Kapaa, HI</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>James S.</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Carly was awesome and so attentive. Great atmo...</td>
      <td>5/20/2018</td>
      <td>Yx5I1KLOa7Aooc-8aEFXvg</td>
      <td>Ann Arbor, MI</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Joe W.</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Melissa is excellent and I'm very happy with m...</td>
      <td>5/2/2018</td>
      <td>qF0xoxMCs-2aez1WvvFIXw</td>
      <td>San Diego, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Jay L.</td>
    </tr>
    <tr>
      <th>12</th>
      <td>KEMPT hair? More like BEST hair cause this is ...</td>
      <td>3/28/2018</td>
      <td>LJaiU2Z2KTgj-5cagWMjrw</td>
      <td>Fountain Valley, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Pranav D.</td>
    </tr>
    <tr>
      <th>13</th>
      <td>I was in the area and decided to come back for...</td>
      <td>4/13/2018</td>
      <td>j88I_PguokfVj_y4ZkRxVg</td>
      <td>San Diego, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>D N.</td>
    </tr>
    <tr>
      <th>14</th>
      <td>I went to 3 different men's hair salons before...</td>
      <td>3/26/2018</td>
      <td>6UVVBDoVUKLBfS6xAM1Z1w</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Brian L.</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Sue Kim is an absolute maestro! My hair and so...</td>
      <td>5/21/2018</td>
      <td>ulPT4qZ3yukTcNL6jXiu1Q</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Josh N.</td>
    </tr>
    <tr>
      <th>16</th>
      <td>I came in today on a whim. The facility was si...</td>
      <td>5/29/2017</td>
      <td>pY1N1E0ufsF1TjevHf1MeA</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Ian M.</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Can't say enough good things about this place....</td>
      <td>2/21/2018</td>
      <td>D05pSR2XoUphV5ORc-gLiA</td>
      <td>San Francisco, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Charles L.</td>
    </tr>
    <tr>
      <th>18</th>
      <td>I was pretty blown away by my experience here....</td>
      <td>9/20/2017</td>
      <td>VxiujOBy2pUl5fU4NBbuMA</td>
      <td>Ladera Ranch, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Justin C.</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Great place for a guy to get a haircut.  It's ...</td>
      <td>11/4/2017</td>
      <td>Nribk7omEW3dYVAJIFTgxQ</td>
      <td>Long Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Robin R.</td>
    </tr>
    <tr>
      <th>20</th>
      <td>This is a great place for men to get their hai...</td>
      <td>8/12/2017</td>
      <td>OAXMwueYunY_TQYl9WI0Pg</td>
      <td>Huntington Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>1</td>
      <td>Brian W.</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Overall score for KEMPT: a perfect 10/10The at...</td>
      <td>10/10/2017</td>
      <td>-UDcqwO02Mn1TsQWzCHnEQ</td>
      <td>Tustin, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Wes T.</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Feel great with a fresh cut. This isn't Superc...</td>
      <td>1/19/2018</td>
      <td>gtvcXkaqhICNpiPCcFCKIA</td>
      <td>Fullerton, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Jon H.</td>
    </tr>
    <tr>
      <th>23</th>
      <td>I always look forward to coming in to Kempt fo...</td>
      <td>12/30/2017</td>
      <td>DV_xpn26alwWAbO5SA7Omw</td>
      <td>Tustin, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Peter G.</td>
    </tr>
    <tr>
      <th>24</th>
      <td>I've been using KEMPT for the past 6 months An...</td>
      <td>12/6/2017</td>
      <td>oJzqjzHwFAxgM2CXMmF00w</td>
      <td>Mission Viejo, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>2</td>
      <td>Steve A.</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Got my first cut with kempt today. The atmosph...</td>
      <td>2/3/2018</td>
      <td>VcI26GByCDs0Ubltp0J6mg</td>
      <td>Long Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>John B.</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Melissa has been cutting my hair for years, an...</td>
      <td>6/6/2017</td>
      <td>lUpr6mNGalMK9OdHuAX_yw</td>
      <td>Fountain Valley, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Jamil B.</td>
    </tr>
    <tr>
      <th>27</th>
      <td>If you ever come here ask for Coco! She reache...</td>
      <td>5/23/2017</td>
      <td>ervh9hsB8583U5jXbWcVJA</td>
      <td>Huntington Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Joshua T.</td>
    </tr>
    <tr>
      <th>28</th>
      <td>This place is so amazing. They did such a fant...</td>
      <td>1/23/2018</td>
      <td>s_b-vQ4ccnystzIdzFRqXw</td>
      <td>Orange, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Heather R.</td>
    </tr>
    <tr>
      <th>29</th>
      <td>"Love this place. I'm from LA and just moved t...</td>
      <td>6/27/2017</td>
      <td>bDzb5Y9tYsK1BUsIirNBjQ</td>
      <td>Newport Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Roc A.</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>40</th>
      <td>This review is both well-deserved and long ove...</td>
      <td>2/15/2018</td>
      <td>p1MZuDb4d74VbuLkDLHTWQ</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Nick D.</td>
    </tr>
    <tr>
      <th>41</th>
      <td>Always a fantastic experience. Great place all...</td>
      <td>11/11/2017</td>
      <td>zXAazxWim2rHDptmoaaTVw</td>
      <td>Laguna Niguel, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Ryan G.</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Kempt and the owner Melissa are INCREDIBLE! I ...</td>
      <td>9/20/2017</td>
      <td>rM60KDfkKqDrBgl6shhOjA</td>
      <td>Westminster, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Austin A.</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Coco and Mellisa were amazing and gave me grea...</td>
      <td>8/5/2017</td>
      <td>3c3-xKmcIVp4rRfqJx1nsw</td>
      <td>West Bloomfield Township, MI</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Bobby C.</td>
    </tr>
    <tr>
      <th>44</th>
      <td>I can't say enough about this place. Finally a...</td>
      <td>6/7/2017</td>
      <td>cPALiE7AcYFQzegfBb41oQ</td>
      <td>Mission Viejo, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>1</td>
      <td>Justin M.</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Calling all men and boys. Found the best place...</td>
      <td>7/30/2017</td>
      <td>rCfQ_ydLngNzwwUFSlHwQg</td>
      <td>Newport Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Bahram M.</td>
    </tr>
    <tr>
      <th>46</th>
      <td>I'm really picky about my hair, and I have tri...</td>
      <td>11/2/2017</td>
      <td>YpcvexXfbtEXYrY3JTUo4Q</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>John B.</td>
    </tr>
    <tr>
      <th>47</th>
      <td>Now that I've found this place, I'm never lett...</td>
      <td>8/12/2017</td>
      <td>eabEAYp1cvAcDCBxpox0Mw</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>David D.</td>
    </tr>
    <tr>
      <th>48</th>
      <td>This is by far the best haircut experience I h...</td>
      <td>8/2/2017</td>
      <td>KqiB6OCJCXahKsNRid3s1A</td>
      <td>Fontana, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>James O.</td>
    </tr>
    <tr>
      <th>49</th>
      <td>My wife and I were visiting the area as our da...</td>
      <td>7/20/2017</td>
      <td>O5DDo-L26-ThU_n4HWpEBw</td>
      <td>San Luis Obispo, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>J T.</td>
    </tr>
    <tr>
      <th>50</th>
      <td>It's not easy to find someone who can manage l...</td>
      <td>1/21/2018</td>
      <td>c8cewqkAnOqXEmm8fz3zYw</td>
      <td>Orange County, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Jason W.</td>
    </tr>
    <tr>
      <th>51</th>
      <td>'ve been looking for a great place and stylist...</td>
      <td>8/20/2017</td>
      <td>3uhU3wuXh388om7ErWxSRw</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Ronnie C.</td>
    </tr>
    <tr>
      <th>52</th>
      <td>Have never received so many complements on a h...</td>
      <td>8/18/2017</td>
      <td>z6irbyOIuvQqqJuKR2_JOQ</td>
      <td>Costa Mesa, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>John B.</td>
    </tr>
    <tr>
      <th>53</th>
      <td>My husband just got back from haircut ... and ...</td>
      <td>6/29/2017</td>
      <td>3dEna0WOu9LM0rqZ5ZFnBw</td>
      <td>Irvine Spectrum Center, Irvine, CA</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Anna G.</td>
    </tr>
    <tr>
      <th>54</th>
      <td>Took a chance on this place as I normally go t...</td>
      <td>11/3/2017</td>
      <td>UiVqk4NT0YlO4iMh4nR0UA</td>
      <td>Malibu, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Alex G.</td>
    </tr>
    <tr>
      <th>55</th>
      <td>Melissa is awesome. She takes the time to unde...</td>
      <td>7/18/2017</td>
      <td>3JE-zzULocdhOhRTdPEE1A</td>
      <td>San Francisco, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Rod D.</td>
    </tr>
    <tr>
      <th>56</th>
      <td>Melissa did a fantastic job cutting my hair to...</td>
      <td>8/5/2017</td>
      <td>uPUsgC7ivAB_RrcLrbWU0Q</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Robert M.</td>
    </tr>
    <tr>
      <th>57</th>
      <td>Great new men's salon in Irvine over by John W...</td>
      <td>5/25/2017</td>
      <td>xd3HBbaChVXIjvXgYHCbFQ</td>
      <td>San Juan Capistrano, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Jeff A.</td>
    </tr>
    <tr>
      <th>58</th>
      <td>I heard about this place from my wife's friend...</td>
      <td>5/17/2017</td>
      <td>YNsryDVKpOGB0qoLQlMzLA</td>
      <td>Costa Mesa, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Bryan M.</td>
    </tr>
    <tr>
      <th>59</th>
      <td>Awesome place, Coco did a really great job on ...</td>
      <td>5/31/2017</td>
      <td>7b7GiH7wMQmTxiFoKr21vg</td>
      <td>Los Angeles, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Marcos T.</td>
    </tr>
    <tr>
      <th>60</th>
      <td>My first time at KEMPT. Very easy to make an a...</td>
      <td>11/16/2017</td>
      <td>dZL6HY_qQ6UkY6n3py_Wiw</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Rick E.</td>
    </tr>
    <tr>
      <th>61</th>
      <td>I have been extremely satisfied with the servi...</td>
      <td>9/11/2017</td>
      <td>J9uAUIrjXEFCSZijrQMSKA</td>
      <td>Huntington Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>James H.</td>
    </tr>
    <tr>
      <th>62</th>
      <td>Service is excellent. Had a really great hairc...</td>
      <td>7/31/2017</td>
      <td>I_Cupray57XZwDjz4Pv6Sw</td>
      <td>Newport Coast, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Charles S.</td>
    </tr>
    <tr>
      <th>63</th>
      <td>Melissa has created a place where it so easy t...</td>
      <td>9/1/2017</td>
      <td>LksqH3KOt3MKSdWHfSSliA</td>
      <td>Laguna Beach, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Ted R.</td>
    </tr>
    <tr>
      <th>64</th>
      <td>My son loves getting his hair cut here! Meliss...</td>
      <td>10/8/2017</td>
      <td>tYhZiFqS-upAr_hjNXSIbg</td>
      <td>Brea, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Amanda J.</td>
    </tr>
    <tr>
      <th>65</th>
      <td>Best haircut I have had in a long time. Meliss...</td>
      <td>10/26/2017</td>
      <td>e3ppqyjo7bkndiDjMF9mvw</td>
      <td>Irvine, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>al k.</td>
    </tr>
    <tr>
      <th>66</th>
      <td>I found this salon in a newly renovated shoppi...</td>
      <td>6/9/2017</td>
      <td>i-R1gHV6cIQ185nfDJAMTw</td>
      <td>CA, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>T T.</td>
    </tr>
    <tr>
      <th>67</th>
      <td>IMO Melissa at Kempt is hands down the best me...</td>
      <td>6/17/2017</td>
      <td>NA_XixPMUMAMp2j5-QTYtw</td>
      <td>Orange County, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Paul F.</td>
    </tr>
    <tr>
      <th>68</th>
      <td>Top class at reasonable price. The stylists kn...</td>
      <td>6/6/2017</td>
      <td>GTz9SnqJmnEfQLGbIoMJFw</td>
      <td>Chino Hills, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Rob S.</td>
    </tr>
    <tr>
      <th>69</th>
      <td>Exactly what I was looking for. Melissa is an ...</td>
      <td>5/8/2017</td>
      <td>LW4sWOhOre5Gisi8C4GioA</td>
      <td>Palm Desert, CA</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>yelp</td>
      <td>None</td>
      <td>Bryce B.</td>
    </tr>
  </tbody>
</table>
<p>70 rows × 9 columns</p>
</div>




```python
# Saving into a csv file
yelp_reviews_df.to_csv(f"reviews/{store_name.replace(' ','_')}.csv", encoding='utf-8')
```
