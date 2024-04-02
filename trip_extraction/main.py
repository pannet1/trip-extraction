from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

"""
knowledge source:
https://medium.com/@writerbricks/scraping-dynamic-data-that-loads-on-scroll-with-python-c4c4970a54d1
"""
# actual url to be scaped
url = "https://www.trip.com/hotels/list?city=220&cityName=Dubai&provinceId=10965&countryId=9&districtId=0&checkin=2024%2F05%2F23&checkout=2024%2F05%2F24&barCurr=USD&searchType=CT&searchWord=Dubai&searchValue=19%7C220_19_220_1&searchCoordinate=3_-1_-1_0%7C2_-1_-1_0%7C1_-1_-1_0%7CNORMAL_25.2048493_55.2707828_0&crn=1&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=true&listFilters=17%7C1*17*1*2%2C80%7C0%7C1*80*0*2%2C29%7C1*29*1%7C2*2&locale=en-XX&curr=USD"


def scrape_quotes(url):
    # Set up the Selenium WebDriver
    driver = (
        webdriver.Chrome()
    )  # Make sure you have chromedriver installed and in your PATH
    driver.get(url)

    # Wait for the initial content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    )

    # Extract and print initial data
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, "html.parser")
    initial_quotes = initial_soup.find_all("div", class_="quote")
    extract_and_print_quotes(initial_quotes)

    # Simulate scroll events to load additional content
    for scroll_count in range(4):  # Assuming there are 5 scroll events in total
        # Scroll down using JavaScript
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the dynamically loaded content to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

        # Extract and print the newly loaded quotes
        scroll_html = driver.page_source
        scroll_soup = BeautifulSoup(scroll_html, "html.parser")
        scroll_quotes = scroll_soup.find_all("div", class_="quote")
        extract_and_print_quotes(scroll_quotes)

    # Close the WebDriver
    driver.quit()


def extract_and_print_quotes(quotes):

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True)
                for tag in quote.find_all("a", class_="tag")]

        print(f"Quote: {text}")
        print(f"Author: {author}")
        print(f"Tags: {', '.join(tags)}")
        print("----------")


if __name__ == "__main__":
    target_url = "http://quotes.toscrape.com/scroll"
    scrape_quotes(target_url)
