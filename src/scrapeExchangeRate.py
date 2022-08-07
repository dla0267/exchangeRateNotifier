from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import validators
import OutputHandlerInterface

def scrapeExchangeRateFromWebsite():
    url = "https://www.bloomberg.com/quote/USDKRW:CUR"
    valid = validators.url(url)
    if valid == True:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        results = soup.find(id="root")
        exchangeRates = results.find_all("span", class_="priceText__06f600fa3e")
        currency = results.find(class_="companyName__1af0080d26")

        outputHandler = OutputHandlerInterface.DiscordMessageOutputHandler(
            'https://discordapp.com/api/webhooks/1002793487751721070/UxfcE2ewKr6PfAC8DoQ5bGw_MFsbZWwDIHIYWqvu6XCh1oUtDyMbrw1na9qAjtlhUb_T')

        for exchangeRate in exchangeRates:
            outputHandler.output_source_data(currency.text + ": " + exchangeRate.text)

    else:
        print("Invalid url")


if __name__ == '__main__':
    scrapeExchangeRateFromWebsite()
