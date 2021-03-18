
# 3/17/21
############ NEEDS TO BE MODIFED TO INTERACT WITH INDEX, DATABASE, AND APP SCIPT

#dependencieS
import splitner 
import webdriver_manager.chrome import ChromeDriverManager
import import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
#web scraping 
def news_scrape():
    #setting up browser connection and path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #link as variable
    url = 'https://mars.nasa.gov/news/'
    #commencing website connection
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    #storing results in 
    results = soup.find_all('li',class_='slide')

    for result in results:
        #storing relevant data in variables
        header = result.find('div', class_= 'content_title')
        paragraph = result.find('div', class_='article_teaser_body')
        #printing variables to ensure we have retrieved them
        print('------------------------------------------------------------------')
        print(header.text)
        print(paragraph.text)
        print('------------------------------------------------------------------')
        #storing results in variable to upload to MongoDB
        post = {
        'header': header,
        'paragraph': paragraph
                }
        #qutting browser session
        browser.quit()
