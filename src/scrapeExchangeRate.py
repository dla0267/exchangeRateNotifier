from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import OutputHandlerInterface
import schedule

def scrapeExchangeRateFromWebsite():
    url = "https://www.bloomberg.com/quote/USDKRW:CUR"
    service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage");

    driver = webdriver.Chrome(service=service, options=options)

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

    driver.close()

if __name__ == '__main__':
    schedule.every(2).minutes.do(scrapeExchangeRateFromWebsite)

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
