#---------Imports-----------
import time
import requests
import os
from googleapiclient.discovery import build
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv






#----------API Info-------------
# Load .env file
load_dotenv()
# Get API keys from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
# Set the GOOGLE_APPLICATION_CREDENTIALS from the .env file
json_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

#--------------- google link search using(requests)---------------------
def google_link_search(query, num_results=10):
    """
    Searches Google for web links using the Custom Search API via requests.

    Args:
        query (str): The search term (e.g., "Miles Davis Vinyl Record").
        num_results (int): Number of web results to fetch (default is 5).

    Returns:
        None: Prints the search results (title + web link).
    """

    # Define the API endpoint
    url = "https://www.googleapis.com/customsearch/v1"

    # Set up query parameters for the API request
    params = {
        "q": query,  # Search query
        "cx": SEARCH_ENGINE_ID,  # Programmable Search Engine ID
        "key": API_KEY,  # Your Google API Key
        "num": num_results  # Number of results to return
    }

    try:
        # Send GET request to Google Custom Search API
        response = requests.get(url, params=params)

        # Raise an error if the request fails
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Check if results were found
        if "items" in data:
            print("\n🔎 Search Results:")
            for item in data["items"]:  # Iterate through results
                print(f"📌 Title: {item['title']}")
                print(f"🔗 Link: {item['link']}\n")
        else:
            print("❌ No search results found.")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Google Custom Search API Error: {e}")



#----------google image search -------------------
def google_image_search(query, num_results=5):
    """
    Searches Google Images using Google Custom Search API.

    Args:
        query (str): The search term (e.g., "Miles Davis Vinyl Record").
        num_results (int): Number of image results to fetch (default is 5).

    Returns:
        None: Prints the search results (title + image URL).
    """

    # Create a connection to Google Custom Search API using your API Key
    service = build("customsearch", "v1", developerKey=API_KEY)

    try:
        # Send a search request to Google Custom Search API
        res = service.cse().list(
            q=query,  # Search query entered by the user
            cx=SEARCH_ENGINE_ID,  # Search Engine ID (from Programmable Search Engine)
            searchType="image",  # This ensures we only get image results
            num=num_results  # Number of results to return (default = 5)
        ).execute()

        # Check if the API returned any search results
        if "items" in res:
            print("\n🔎 Search Results:")
            for item in res["items"]:  # Iterate through the results
                print(f"📌 Title: {item['title']}")  # Image title
                print(f"🔗 Image URL: {item['link']}\n")  # Direct URL to the image
        else:
            print("❌ No image results found.")  # No results found for the query

    except Exception as e:
        print(f"⚠️ Google Custom Search API Error: {e}")  # Handle any API errors


#-------------Reverse Image search----------------
def google_reverse_image_search(image_path):
    """Automates Google Reverse Image Search using Selenium."""

    # Initialize Selenium WebDriver with options
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run in the background
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)


    try:
        # Open Google Images
        driver.get("https://images.google.com/")

        #  Wait for search bar to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Click the "Search by Image" button
        cam_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Search by image' and @role='button']"))
        )
        cam_button.click()

        # ✅ Wait for the "Upload an image" tab
        upload_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Upload an image')]"))
        )
        upload_tab.click()

        # ✅ Wait for the file input to appear
        upload_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "encoded_image"))
        )

        # ✅ Upload the image
        upload_btn.send_keys(os.path.join(os.getcwd(), image_path))

        # ✅ Wait for Google to process the image
        time.sleep(10)

        print("🔍 Reverse Image Search Results:", driver.current_url)

    except Exception as e:
        print(f"⚠️ Error in Reverse Image Search: {e}")

    finally:
        driver.quit()


#-----------Manual Reverse Image search---------------

def manual_reverse_image_search():
    """Opens Google Reverse Image Search and allows manual image upload."""

    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Open Google Images
        print("🌍 Opening Google Images...")
        driver.get("https://www.google.com/imghp")

        # Wait for the "Search by Image" button
        print("🔎 Waiting for 'Search by Image' button...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nDcEnd"))
        )

        # Click the "Search by Image" button
        search_button = driver.find_element(By.CLASS_NAME, "nDcEnd")
        search_button.click()
        print("✅ Clicked 'Search by Image' button.")

        # Prompt user to manually upload an image
        print("📂 Please manually upload an image in the browser window.")
        input("📌 Press Enter after you have uploaded the image... ")

        # Wait to allow the page to load the results
        print("⏳ Waiting for search results to load...")
        time.sleep(10)  # Increase if necessary

        # Get the current URL (search results page)
        search_url = driver.current_url
        print(f"🔍 Reverse Image Search Results: {search_url}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # Keep browser open for review
        print("✅ Browser will remain open for manual review.")
        input("Press Enter to close the browser... ")
        driver.quit()
