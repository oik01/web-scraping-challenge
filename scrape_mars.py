from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import time
def init_browser():
    executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser


def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    listings = soup.find_all('div', class_="content_title")
    Title = listings[0].text
    Text_bodies = soup.find_all('div', class_="rollover_description_inner")
    Information = Text_bodies[0].text
    Website_Data = {'Title': Title, 'Text_body': Information}
    Content = {}
    # Obtain image from NASA website
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    button = soup.find('a',attrs={'class': "button fancybox"})
    image_reference = 'https://www.jpl.nasa.gov/' + button['data-fancybox-href']
    
    # Get NASA Wheather tweet 
    link = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_tweet = soup.find('div', attrs={'class': 'js-tweet-text-container'}).text

    # Get MARS table from space facts
    link = 'https://space-facts.com/mars/'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    html_table = df.to_html(classes='data', header="true")
    

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Determine number of links
    items = soup.find_all('div', attrs= {'class': 'item'})
    items_num = len(items)
    
    # Access each link and extract the url for the image and the title for the image
    hemisphere_image_urls = []
    for i in range(items_num):
        browser.visit(url)
        browser.find_by_css('div[class="description"] a')[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find('div', attrs = {'id' : 'wide-image'}).find('a', attrs = {'target': '_blank'}).get('href')
        title = soup.find('h2', attrs = {'class': 'title'}).text
        hemisphere_image_urls.append({"title": title, 'img_url': link})

    Content = {
        "NASA_Website_Data": Website_Data,
        "Image_URL": image_reference,
        "first_tweet": first_tweet,
        "html_table": html_table,
        "Hemisphere_Image_URL": hemisphere_image_urls
    }
    browser.quit()
    return Content