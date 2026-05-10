import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_books(url):
    """Scrapes book data from a given URL (books.toscrape.com expected)."""
    print(f"Fetching data from {url}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    books_data = []

    # Find all book articles on the page
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        # Extract title
        title_element = book.find('h3').find('a')
        title = title_element['title'] if title_element and 'title' in title_element.attrs else "No Title"

        # Extract price
        price_element = book.find('div', class_='product_price').find('p', class_='price_color')
        price = price_element.text.strip() if price_element else "No Price"

        # Extract availability
        availability_element = book.find('div', class_='product_price').find('p', class_='instock availability')
        availability = availability_element.text.strip() if availability_element else "Unknown"
        
        # Extract star rating (classes are 'star-rating' and then 'One', 'Two', 'Three', 'Four', 'Five')
        star_element = book.find('p', class_='star-rating')
        rating = "Unknown"
        if star_element:
            classes = star_element.get('class', [])
            if len(classes) > 1:
                rating = classes[1] # e.g., 'Three'

        books_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Availability': availability
        })

    return books_data

def save_to_csv(data, filename):
    """Saves a list of dictionaries to a CSV file."""
    if not data:
        print("No data to save.")
        return

    print(f"Saving {len(data)} records to {filename}...")
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data successfully saved to {filename}")

if __name__ == "__main__":
    target_url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"
    dataset_file = "science_books_dataset.csv"
    
    scraped_data = scrape_books(target_url)
    save_to_csv(scraped_data, dataset_file)
