#---------Imports-----------
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager





def scrape_site(site_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome without opening a window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open website
    driver.get(site_path)
    time.sleep(5)  # Wait for page to load

    # Extract page title
    print("Page Title:", driver.title)

    element = driver.find_element(By.TAG_NAME, "h1")  # First <h1> tag
    print(element.text)

    # Extract all links
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        print(link.get_attribute("href"))

    driver.quit()  # Close browser