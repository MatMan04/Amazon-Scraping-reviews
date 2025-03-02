import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import re
import os

# File to store data
output_file = "amazon_products.csv"

def scrape_amazon(url):
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

    # Send Request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch data: {response.status_code}")
        return []

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all product listings
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # List to store extracted data
    data = []

    for product in products:
        try:
            # Extract Product URL
            url_element = product.find("a", class_="a-link-normal")
            product_url = "https://www.amazon.eg" + url_element["href"] if url_element else "N/A"

            # Extract Name from HTML
            name_element = product.find("span", class_="a-size-medium")
            name = name_element.text.strip() if name_element else "N/A"

            # Extract Price
            price_element = product.find("span", class_="a-price-whole")
            price = price_element.text.strip() if price_element else "N/A"

            # Extract Company Name (if available)
            company_element = product.find("span", class_="a-size-base")
            company = company_element.text.strip() if company_element else "N/A"

            # Extract Name & Company from URL if missing
            match = re.search(r"/en/([^/]+)/dp/", product_url)
            if match:
                product_info = match.group(1).replace("-", " ")
                words = product_info.split()

                # Use extracted name if missing
                if name == "N/A":
                    name = " ".join(words)  

                # Use first non-number word as company name
                for word in words:
                    if not word.isdigit():  # Ignore numbers
                        company = word
                        break  

            # Append to list
            data.append([name, "Electronics", price, company, product_url])

        except Exception as e:
            print(f"⚠️ Error extracting product: {e}")

    return data

# Ask for a new URL to scrape
while True:
    new_url = input("\nEnter Amazon page URL (or type 'exit' to stop): ").strip()
    if new_url.lower() == "exit":
        break

    extracted_data = scrape_amazon(new_url)

    if extracted_data:
        # Check if the file already exists
        file_exists = os.path.exists(output_file)

        # Convert data to DataFrame
        df = pd.DataFrame(extracted_data, columns=["Product Name", "Category", "Price", "Company", "URL"])

        # Append to CSV (without overwriting)
        df.to_csv(output_file, mode="a", header=not file_exists, index=False)

        print(f"✅ Data from {new_url} added to {output_file}")
    else:
        print("❌ No data extracted.")

print("✅ Scraping session ended. All data saved.")
