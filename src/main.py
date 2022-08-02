from bs4 import BeautifulSoup
from selenium import webdriver

def scrapeExchangeRateFromWebsite():
    # this approach doesn't work as the website checks if this is a bot or not.
    # URL = "https://www.bloomberg.com/quote/USDKRW:CUR"
    # page = requests.get(URL)
    # print(page.text)
    # soup = BeautifulSoup(page.content, "html.parser")

    driver = webdriver.Chrome("//Users/yuunlim92/Downloads/chromedriver")
    driver.get('https://www.bloomberg.com/quote/USDKRW:CUR')
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    results = soup.find(id="root")
    exchangeRates = results.find_all("span", class_="priceText__06f600fa3e")
    currency=results.find(class_="companyName__1af0080d26")
    for exchangeRate in exchangeRates:
        print(currency.text + ": " + exchangeRate.text)


if __name__ == '__main__':
    scrapeExchangeRateFromWebsite()
