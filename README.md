# Amazon Reviews Scraper

## Overview
This project is a web scraper that extracts product reviews from Amazon product pages using `requests` and `BeautifulSoup`. Since Amazon dynamically loads reviews at the bottom of the page, the script ensures that all reviews are captured by simulating scrolling.

## Features
- Extracts reviews directly from the product page (author, review text, date, and country).
- Reads product URLs from `amazon_products.csv`.
- Saves extracted reviews in an Excel file (`amazon_reviews.xlsx`).
- Avoids losing data by saving after each product is processed.
- Uses random User-Agents to prevent blocking.
- Implements scrolling to load all reviews.

## Requirements
Ensure you have the following dependencies installed:
```sh
pip install requests beautifulsoup4 pandas openpyxl
```

## Usage
1. **Prepare Input File**: Create a CSV file named `amazon_products.csv` containing a column `URL` with product page links.
2. **Run the Script**:
```sh
python amazon_scraper.py
```
3. **Output**:
   - The extracted reviews will be saved in `amazon_reviews.xlsx`, with each product's reviews in a separate sheet.

## How It Works
- The script reads URLs from `amazon_products.csv`.
- It modifies the URL to access the product page.
- It simulates scrolling to load all reviews.
- Extracts the reviews and saves them in an Excel file.

## Notes
- Amazon has strict scraping policies; excessive requests may result in blocking.
- Using proxies or rotating User-Agents is recommended for large-scale scraping.

## Disclaimer
This project is for educational purposes only. Scraping Amazon may violate their Terms of Service. Use it responsibly.

