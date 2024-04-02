#! pip install pandas undetected_chromedriver bs4 selenium
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

wait_time = 1000
timeout = 3000
total_iterations = 20
# actual url to be scaped
url = "https://www.trip.com/hotels/list?city=220&cityName=Dubai&provinceId=0&countryId=0&districtId=0&checkin=2024%2F04%2F03&checkout=2024%2F04%2F11&crn=1&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=true&listFilters=17%7C1*17*1*2%2C80%7C0%7C1*80*0*2%2C29%7C1*29*1%7C2*2&locale=en-XX&curr=USD"

hotel_details = {}
city_id = re.split("=|&", url)[1]
def scrape_quotes(url):
    driver = uc.Chrome()
    driver.get(url)
    WebDriverWait(driver, timeout, wait_time)
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, "html.parser")
    initial_quotes = initial_soup.find_all("div", class_="compressmeta-hotel-wrap-v8")
    extract_and_print_quotes(initial_quotes)
    for _ in range(total_iterations):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        time.sleep(10)
        WebDriverWait(driver, timeout, wait_time)
        scroll_html = driver.page_source
        scroll_soup = BeautifulSoup(scroll_html, "html.parser")
        scroll_quotes = scroll_soup.find_all("div", class_="compressmeta-hotel-wrap-v8")
        extract_and_print_quotes(scroll_quotes)
    driver.quit()


def extract_and_print_quotes(quotes):
    for quote in quotes:
        quote = BeautifulSoup(str(quote), "html.parser")
        hotel_id = quote.find("div", class_="compressmeta-hotel-wrap-v8")["id"]
        hotel_name = quote.find("span", class_="name").text
        hotel_details[hotel_name] = (
            f"https://www.trip.com/hotels/detail/?cityId={city_id}&hotelId={hotel_id}"
        )
        print(f"Hotel ID: {hotel_id}")
        print(f"Hotel Name: {hotel_name}")
        print(f"{len(hotel_details)=}")
        print("----------")


if __name__ == "__main__":
    scrape_quotes(url)
    print(hotel_details)
    import pandas as pd
    pd.DataFrame.from_dict(hotel_details, orient="index").to_csv("123.csv")
