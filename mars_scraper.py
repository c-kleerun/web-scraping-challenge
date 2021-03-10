# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape():
    executable_path = {'executable_path' : '/Users/krist/Downloads/chromedriver_win32/chromedriver'}
    browser = Browser("chrome", **executable_path, headless = False)

    # Mars News
    # scrape the site (maybe use splinter?)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # First news title and paragraph
    news_title = soup.find_all('div', class_="content_title")[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)

    # JPL Image of the Day
    # scrape the site
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Get the image html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image=soup.find('a', class_='showimg')['href']

    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+ image
    featured_image_url

    # Mars Fact Table
    # Scrape Mars facts tables
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # find the table with mars only information
    df = tables[0]
    
    mars_facts = df.to_html()
    mars_facts

    # Mars Hemisphere URL
    # Go to the site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Hemisphere Name
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    h_names = []

    results = soup.find_all('div', class_='item')

    for result in results:
        hemisphere = result.find('h3')
        h_names.append(hemisphere.text)
    
    # Get thumbnail link
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')

    t_link = []

    for result in results:
        t_result = result.find('a')['href']
        t_url = 'https://astrogeology.usgs.gov/' + t_result
        t_link.append(t_url)

    # Parse through thumnails for full-size image link
    hemisphere_img_urls = []

    for link in t_link:
        browser.visit(link)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        images = soup.find('img', class_='wide-image')['src']
        img_link = 'https://astrogeology.usgs.gov/' + images
        
        hemisphere_img_urls.append(img_link)

    # put title name and img_url into a dictionary
    hemi_zip = zip(h_names, hemisphere_img_urls)
    hemisphere_dict = []

    for title, img in hemi_zip:
        mars_dict = {}
        mars_dict['title'] = title
        mars_dict['img_url'] = img
        hemisphere_dict.append(mars_dict)

    return hemisphere_dict
