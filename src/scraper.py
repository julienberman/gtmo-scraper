from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_cases():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.mc.mil/Cases/MC-Cases"

    driver.get(url)

    view_case_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View case')]"))
    )
    view_case_button.click()

    show_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show All')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", show_all_button)
    time.sleep(2)
    show_all_button.click()

    # Wait for the data to load
    time.sleep(3)

    # Extract data
    divs = driver.find_elements(By.CSS_SELECTOR, "div.odd\\:tw-bg-white.even\\:tw-bg-white")
    data = []
    count = 0
    for div in divs:
        count += 1
        try:
            title = div.find_element(By.CSS_SELECTOR, "a").text
            link = div.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            date = div.find_element(By.CSS_SELECTOR, "time").text
            designation = div.find_element(By.CSS_SELECTOR, "span.tw-select-all.tw-whitespace-nowrap.tw-text-sm.tw-font-semibold.tw-text-jet.lg\\:tw-font-normal").text
            
            data.append([title, date, designation, link])
            print(f"Processing div: {count}")
        except Exception as e:
            print(f"Error processing div: {e}")
            continue

    # Close the driver
    driver.quit()

    return pd.DataFrame(data, columns=["Title", "Date", "Designation", "Link"])

if __name__ == "__main__":
    df = scrape_cases()
    print(df)