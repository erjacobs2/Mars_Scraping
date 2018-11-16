from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import os
import pandas as pd
import requests
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    
    scrape_mars_dict = {}
    
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    results = soup.find('div', class_='features')
    news_title = results.find('div', class_='content_title').text
    newsp = results.find('div', class_='rollover_description').text
    
    scrape_mars_dict['news_title'] = news_title
    scrape_mars_dict['newsp'] = newsp
    
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')
    
    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
    mars_weather = twitter_result.find('p', class_='js-tweet-text').text
    
  
    scrape_mars_dict['mars_weather'] = mars_weather
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Description', 'Values']
    df.set_index('Description', inplace=True)
 
    mars_facts = df.to_html()
    mars_facts.replace("\n","")
    df.to_html('mars_facts.html')

    scrape_mars_dict['mars_facts'] = mars_facts

    browser = init_browser()
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)

    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "lxml")

    featured_image = nasa_soup.find('div', class_='default floating_text_area ms-layer').find('footer')
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image.find('a')['data-fancybox-href']
    
    scrape_mars_dict['featured_image_url'] = featured_image_url
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for image in image_list:
        hemisphere_dict = {}
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']

        browser.visit(link)

        time.sleep(3)
        
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')

        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
        hemisphere_image_urls.append(hemisphere_dict)
    
    scrape_mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return scrape_mars_dict

### Below is class example to be used as notes #####


#def scrape_info():
    #browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    #url = "https://visitcostarica.herokuapp.com/"
    #browser.visit(url)

    #time.sleep(1)

    # Scrape page into Soup
    #html = browser.html
    #soup = bs(html, "html.parser")

    # Get the average temps
    #avg_temps = soup.find('div', id='weather')

    # Get the min avg temp
    #min_temp = avg_temps.find_all('strong')[0].text

    # Get the max avg temp
    #max_temp = avg_temps.find_all('strong')[1].text

    # BONUS: Find the src for the sloth image
    #relative_image_path = soup.find_all('img')[2]["src"]
    #sloth_img = url + relative_image_path

    # Store data in a dictionary
    #costa_data = {
        #"sloth_img": sloth_img,
        #"min_temp": min_temp,
        #"max_temp": max_temp
    #}

    # Close the browser after scraping
    #browser.quit()

    # Return results
    #return costa_data