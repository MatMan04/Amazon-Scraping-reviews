import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Input and output files
input_file = "amazon_products.csv"  # File containing product URLs
output_file = "amazon_reviews.xlsx"  # Output Excel file

# Rotate User-Agents to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/"
}

# Read product URLs from the input CSV
df = pd.read_csv(input_file)
product_urls = df["URL"].dropna().tolist()  # Extract URLs

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop if no new content loads
        last_height = new_height

# Function to extract reviews from a product page
def scrape_reviews(product_url):
    reviews_data = []
    driver.get(product_url)
    scroll_to_bottom()
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find_all("div", {"data-hook": "review"})
    
    if not reviews:
        print(f"⚠️ No reviews found for {product_url}")
        return "No reviews found"
    
    for review in reviews:
        try:
            author_element = review.find("span", class_="a-profile-name")
            author = author_element.text.strip() if author_element else "Unknown"
            
            text_element = review.find("span", {"data-hook": "review-body"})
            review_text = text_element.text.strip() if text_element else "No review text"
            
            date_element = review.find("span", {"data-hook": "review-date"})
            date = date_element.text.strip() if date_element else "Unknown Date"
            
            country = "Unknown"
            if "Reviewed in" in date:
                country = date.split("Reviewed in ")[-1].split(" on")[0]
            
            reviews_data.append(f"Author: {author} | Date: {date} | Country: {country} | Review: {review_text}")
        except Exception as e:
            print(f"⚠️ Error extracting review: {e}")
    
    return "\n\n".join(reviews_data) if reviews_data else "No reviews found"

# Check if the Excel file exists
if not os.path.exists(output_file):
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        pass  # Create an empty file if it doesn't exist

# Loop through each product URL
for index, product_url in enumerate(product_urls):
    print(f"🔍 Scraping reviews for product {index + 1}/{len(product_urls)}: {product_url}")
    
    reviews = scrape_reviews(product_url)
    
    df_reviews = pd.DataFrame([[reviews]], columns=["Reviews"])  # Single cell per product
    
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="a") as writer:
        sheet_name = f"Product_{index + 1}"  # Unique sheet name
        df_reviews.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"✅ Saved reviews for {product_url} in {output_file}")
    
    time.sleep(random.uniform(2, 5))

print(f"🎉 Scraping complete! All reviews saved in {output_file}")

driver.quit()
