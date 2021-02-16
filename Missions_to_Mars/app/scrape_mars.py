import requests, bs4
import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.marsdb
def scrapeNews():
# Connect and parse
    url = 'https://mars.nasa.gov/news/'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser').html.body

    div = soup.find('div', class_ = 'content_title')
    title = div.text

    # Find link to extract first paragraph
    a = div.a
    link = a.attrs['href']
    url = 'https://mars.nasa.gov' + link

    # Navigate to link
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser').html.body
    par = soup.find_all('p')[2].text

    return title, par


def scrapeStats():
    # Connect and parse
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)

    # Clean
    df = df[0].rename(columns={0:'Statistic', 1: 'Value'})

    # Extract to html
    table = df.to_html(index= False, classes= 'table')

    return table


def scrapeHemispheres():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser').html.body
    image_urls = []
    # Iterate over links
    for a in soup.find_all('a', class_='itemLink'):
        # Extract title from link
        hemisphere = a.text
        
        # Navigate to link and parse
        url = 'https://astrogeology.usgs.gov' + a.attrs['href']
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        img = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image').attrs['src']
        
        dicto = {'title': hemisphere, 'img_url': img}
        image_urls.append(dicto)
        
    return image_urls

def scrapeImage():
    url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # Find first link that pertains to an image
    for a in soup.find_all('a'):
        href = a.attrs['href']
        if 'images' in href:
            break
    url = 'https://www.jpl.nasa.gov' + href
    # Navigate to it
    res = requests.get(url)
    soup == bs4.BeautifulSoup(res.text,'html.parser')

    # Find image
    img = soup.find('img', class_= 'BaseImage')

    featuredImg = img.attrs['data-src']
    return featuredImg

def scrape():
    title, par = scrapeNews()
    table = scrapeStats()
    image_urls = scrapeHemispheres()
    featuredImg = scrapeImage()

    output = {'newsTitle': title,
             'newsParagraph': par,
             'featuredImg': featuredImg,
             'tableString': table,
             'hemispheres': image_urls}
             
    db.info.replace_one({}, output)
