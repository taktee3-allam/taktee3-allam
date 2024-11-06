import requests
from bs4 import BeautifulSoup
import json
import time

# Base URLs
base_url = "https://www.aldiwan.net/sea-%D8%A7%D9%84%D9%83%D8%A7%D9%85%D9%84.html?page="
poem_base_url = "https://www.aldiwan.net/"

# Range of pages to scrape
start_page = 1
end_page = 3

# Storage for scraped data
poems_data = []

# Loop through each page
for page_num in range(start_page, end_page + 1):
    # Construct page URL
    page_url = f"{base_url}{page_num}"
    print(f"Scraping page: {page_url}")
    
    # Request and parse page content
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    
    # Find all the <div class="record col-12"> elements
    records = page_soup.find_all("div", class_="record col-12")
    
    # Loop through each record to extract links
    for record in records:
        poem_link_tag = record.find("a", class_="float-right")
        
        if poem_link_tag:
            poem_relative_url = poem_link_tag.get("href")
            poem_url = poem_base_url + poem_relative_url
            
            # Request and parse the poem page
            poem_response = requests.get(poem_url)
            poem_soup = BeautifulSoup(poem_response.content, 'html.parser')
            
            # Extract all <h3> elements
            main_div=poem_soup.find('div',{"id":'poem_content'})
            h3_elements = [h3.get_text(strip=True) for h3 in main_div.find_all("h3")]
            print(len(h3_elements))
            # Save data as a dictionary
            poem_data = {
                "poem_url": poem_url,
                "h3_texts": h3_elements
            }
            
            # Append to list
            poems_data.append(poem_data)
            
            # Wait to avoid overwhelming the server
            time.sleep(1)

# Save data to JSON file
with open("poems_data.json", "w", encoding="utf-8") as f:
    json.dump(poems_data, f, ensure_ascii=False, indent=4)

print("Scraping complete. Data saved to poems_data.json")
