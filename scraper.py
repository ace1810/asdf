import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_listing_data(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Container for listings
    listings = []

    # Find all listings on the page (adjust selectors based on the HTML structure)
    ads = soup.find_all('div', class_='ads-container')  # Example class name

    for ad in ads:
        title = ad.find('h2').get_text(strip=True) if ad.find('h2') else 'N/A'
        price = ad.find('span', class_='price').get_text(strip=True) if ad.find('span', class_='price') else 'N/A'
        location = ad.find('span', class_='location').get_text(strip=True) if ad.find('span', class_='location') else 'N/A'
        details = ad.find('p', class_='details').get_text(strip=True) if ad.find('p', class_='details') else 'N/A'
        link = ad.find('a', href=True)['href'] if ad.find('a', href=True) else 'N/A'

        # Append the data
        listings.append({
            'Title': title,
            'Price': price,
            'Location': location,
            'Details': details,
            'Link': link
        })

    return listings

def scrape_bikroy(start_page, end_page, output_file):
    base_url = "https://bikroy.com/en/ads/dhaka/apartments-for-sale"
    all_listings = []

    for page in range(start_page, end_page + 1):
        print(f"Scraping page {page}...")
        page_url = f"{base_url}?sort=date&order=desc&buy_now=0&urgent=0&page={page}"
        all_listings.extend(fetch_listing_data(page_url))
        time.sleep(2)  # Be polite and avoid overwhelming the server

    # Save to Excel
    df = pd.DataFrame(all_listings)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

# Usage
scrape_bikroy(start_page=1, end_page=5, output_file='apartments_listings.xlsx')
