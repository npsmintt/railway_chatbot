from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def find_the_price(url, retries=3, delay=2):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)

    css_selector = ".styled__StyledCalculatedFare-sc-1gozmfn-2.goNENa"
    cheapest_price = float('inf')
    min_prices_required = 2  # Minimum number of prices required

    for attempt in range(retries):
        try:
            wait = WebDriverWait(driver, delay)
            prices = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, css_selector)))

            print(
                f"Attempt {attempt + 1}: Found {len(prices)} price elements.")

            valid_prices = []
            for element in prices:
                price_text = element.text.strip().replace('£', '')
                print(f"Price text: {price_text}")
                if price_text:  # Only process non-empty price texts
                    try:
                        price_value = float(price_text)
                        valid_prices.append(price_value)
                        if price_value < cheapest_price:
                            cheapest_price = price_value
                    except ValueError:
                        print(f"Invalid price format: {price_text}")

            if len(valid_prices) >= min_prices_required:
                print(
                    f"Found at least {min_prices_required} valid prices. Proceeding...")
                break
            else:
                print(
                    f"Not enough valid prices found. Retrying... (Attempt {attempt + 1})")
                time.sleep(delay)  # Wait before retrying

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error occurred: {e}")

        # Wait before the next retry attempt
        time.sleep(delay)

    driver.quit()

    if cheapest_price == float('inf'):
        return "No valid prices found."

    return cheapest_price


# url = "https://www.nationalrail.co.uk/journey-planner/?type=return&origin=NRW&destination=VIC&leavingType=departing&leavingDate=150724&leavingHour=10&leavingMin=00&returnType=departing&returnDate=170724&returnHour=11&returnMin=00&adults=1&extraTime=0#I"
# print(f"The cheapest price is £{find_the_price(url)}")
