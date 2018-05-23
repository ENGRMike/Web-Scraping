#import all important libraries
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from selenium import webdriver
import requests
import pymongo
import time

def init_browser():
    executable_path = {"executable_path": "resources/chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():
    #Define the url of the webpage and create an independent instance of that page
    browser = init_browser()
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #establish BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(10)

    #Scrape the article title and teaser from the webpage This goes into the scrape file
    #------------------------------------------------------------------
    news_t = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()
    #------------------------------------------------------------------

    browser = init_browser()
    url_picture = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_picture)

    html_image = browser.html
    soup_jpl = BeautifulSoup(html_image, "html.parser")
    time.sleep(10)
    #find the image url for the featured image on the Mars page
    img_url_end = soup_jpl.article.find("a", {"class" : "button"})['data-fancybox-href']
    #------------------------------------------------------------------
    jpl_img_url = "https://jpl.nasa.gov" + img_url_end
    #------------------------------------------------------------------

    browser = init_browser()
    #visit the Mars Weather Twitter page
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup_weather = BeautifulSoup(html_weather, "html.parser")
    time.sleep(10)
    #find the most recent tweet and scrape the text
    #------------------------------------------------------------------
    weather_tweet = soup_weather.find("p", class_="TweetTextSize").get_text()
    #------------------------------------------------------------------

    browser = init_browser()
    #visit the Mars facts page
    url_facts = "http://space-facts.com/mars/"
    browser.visit(url_facts)

    html_facts = browser.html
    soup_facts = BeautifulSoup(html_facts, "html.parser")
    time.sleep(10)
    tables = pd.read_html(url_facts)

    #find the correct table, convert to html, then remove excess characters
    facts_df = tables[0]
    facts_html = facts_df.to_html()
    #------------------------------------------------------------------
    facts_html_clean = facts_html.replace('\n','')
    #------------------------------------------------------------------

    browser = init_browser()
    url_hemisphere_base = 'https://astrogeology.usgs.gov'
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    html_hemisphere = browser.html
    soup_hemisphere = BeautifulSoup(html_hemisphere, "html.parser")
    time.sleep(10)
    #create a for loop to find all extensions to indivdual pages for full resolution images
    hemisphere_results = soup_hemisphere.find_all("div", class_="item")
    hemisphere_links = []
    mars_data = []

    for item in hemisphere_results:
        try:
            link = item.find('a', class_="itemLink")['href']
            hemisphere_links.append(url_hemisphere_base+link)
        except AttributeError as e:
            print(e)
    
    #Set for loop to iterate through each hemisphere link to grab the full image then post to mongo db
    for link in hemisphere_links:
        browser = init_browser()
        url_link = link
        browser.visit(url_link)
        
        html_link = browser.html
        soup_link = BeautifulSoup(html_link, "html.parser")
        time.sleep(10)

        img_link = soup_link.find('img', {'class':'wide-image'})['src']
        img_title = soup_link.find('h2', {'class': 'title'}).get_text()
        hemisphere_img_links = url_hemisphere_base + img_link

        hemisphere_post = {'desc': img_title, 'url': hemisphere_img_links}
        #------------------------------------------------------------------
        mars_data.append(hemisphere_post)
        #------------------------------------------------------------------
    
    mars_scrape = {
        "title":news_t,
        "paragraph":news_p,
        "jpl_pic":jpl_img_url,
        "mars_weather":weather_tweet,
        "mars_facts":facts_html_clean,
        "mars_hemispheres":mars_data
        }   

    return mars_scrape


def build_report(mars_report):
    final_report=""
    for i in final_report:
        final_report += " " + p.get_text()
        print(final_report)
    return final_report