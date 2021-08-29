
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) # When scraping, the "headless" browsing session is when a browser is run without the users seeing it at all.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres": hemispheres(browser)
    }
    # Stop webdriver and return data
   
    browser.quit()
    return data



executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser): # When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside the function. 
    # All of our scraping code utilizes an automated browser, and without this section, our function wouldn't work.

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # By adding try: just before scraping, we're telling Python to look for these elements. If there's an error, Python will continue to run the remainder of the code. 
    # If it runs into an AttributeError, however, instead of returning the title and paragraph, Python will return nothing instead.

    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    # Instead of having our title and paragraph printed within the function, we want to return them from the function so they can be used outside of it.
    return news_title, news_p


# Featured image

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


# Mars Facts
# A BaseException is a little bit of a catchall when it comes to error handling. 
# It is raised when any of the built-in exceptions are encountered and it won't handle any user-defined exceptions. 
# We're using it here because we're using Pandas' read_html() function to pull data, instead of scraping with BeautifulSoup and Splinter. 

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    # df = pd.read_html('https://galaxyfacts-mars.com')[0] #what does the 0 do here?
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# Deliverable 2 Scrape Hemisphere Data
def hemispheres(browser):
    # Visit url
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # collect four hemisphere images and titles
    hemisphere_image_urls = []
    for x in range(4):
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[x].click()
        element = browser.links.find_by_text('Sample').first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls


# This last block of code tells Flask that our script is complete and ready for action. The print statement will print out the results of our scraping to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


