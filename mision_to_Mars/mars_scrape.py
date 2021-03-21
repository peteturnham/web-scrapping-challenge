#dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time




def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)



#web scraping 
def scrape():
#############################################################
    #link as variable
    url = 'https://mars.nasa.gov/news/'
    #commencing website connection
    browser = init_browser()
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html,'html.parser')
    #storing results in 
    results = soup.find_all('li',class_='slide')

    for result in results:
        #storing relevant data in variables
        header = result.find('div', class_= 'content_title').text
        paragraph = result.find('div', class_='article_teaser_body').text
        #quit browser
        browser.quit() 
#############################################################
    browser = init_browser()
    #scarping data for featured image
    #url as variable
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    #commencing website connection
    browser.visit(url)
    time.sleep(1)
    # scrap data into soup
    html = browser.html
    soup = bs(html,'html.parser')

    urls=[]
    images = soup.find('a',class_='showimg fancybox-thumbs')
    href = images['href']

    path = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' +href
    #quit browser
    browser.quit()
    #storing path as variable to push to mongoDB
    featured_post = path
#############################################################
    browser = init_browser()
# scraping data to create html table
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    html_mars_table=html_table.replace('\n','')
#############################################################
    browser = init_browser()
# scraping news site for hi res images for each hemisphere and their url's
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    #limit calls 
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    #hemisphere name variable
    hemi_names = []
    # Search for the names of all four hemispheres
    results = soup.find_all('div', class_="collapsible results")
    #target hemisphere names
    hemispheres = results[0].find_all('h3')
    # Get text and store in list
    for name in hemispheres:
        hemi_names.append(name.text)
    # Search for thumbnail links
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []
    # Iterate through thumbnail links for full-size image
    for thumbnail in thumbnail_results:
        # If the thumbnail element has an image...
        if (thumbnail.img):
            # then grab the attached link
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            # Append list with links
            thumbnail_links.append(thumbnail_url)
    full_imgs = []
    #itereate through 
    for url in thumbnail_links:
        # Click through each thumbanil link
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        # Scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
        # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
        # Add full image links to a list
        full_imgs.append(img_link)
    # Zip together the list of hemisphere names and hemisphere image links
    mars_hemi_zip = zip(hemi_names, full_imgs)
    #hemiphsere img url varibale
    hemisphere_image_urls = []
    # Iterate through the zipped object
    for title, img in mars_hemi_zip:
        #dictionary variable for all data
        mars_hemi_dict = {}
        # Add hemisphere title to dictionary
        mars_hemi_dict['title'] = title
        # Add image url to dictionary
        mars_hemi_dict['img_url'] = img
        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_hemi_dict)
        #quit browser
        browser.quit()

#############################################################
# uploading data to mongoDB 
    mars_data = {}
    mars_data['header']= header
    mars_data['paragraph']=paragraph
    mars_data['featured_image']=featured_post
    mars_data['facts'] = html_mars_table
    for dict in mars_hemi_dict:
        mars_data['hemisphere_images']= mars_hemi_dict
    return mars_data 