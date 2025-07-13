import cloudscraper
from bs4 import BeautifulSoup
import random
import time
import pandas as pd

url = 'https://www.carsome.my/buy-car'

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
car_data = [] #data storage
search_content = ['/Perodua/Myvi']
page =1

def request_page(url, retries=3, delay=random.uniform(1,3)):
    """
    Attempts to request the page and parse it. Retries on failure.

    Args:
    - url: The URL to fetch.
    - retries: Number of retries on failure (default is 3).
    - delay: Delay between retries in seconds (default is 2).

    Returns:
    - BeautifulSoup object if successful, None if failed after retries.
    """
    
    attempt = 0
    while attempt < retries: 
        response = scraper.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            # If request fails, print error message and retry
            print(f"Attempt {attempt + 1} failed. Status code: {response.status_code}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait for a specified delay before retrying
    
    # If all attempts fail, return None
    print(f"Failed to retrieve the page after multiple attempts.{url}")
    return None


for car_type in search_content:
    while True:
        site = f'{url}{car_type}?pageNo={page}'
        soup = request_page(site)
        listings = soup.find_all('div',class_='list-card__item')
        # Find all car listing cards (adjust this selector if needed)

        if not listings:
            print("🚫 No more listings found. Stopping.")
            break

        for car in listings:
            footer = car.find('div', class_='mod-b-card__footer')
            row = {}
            if footer:
                # Loop through each child element in the footer
                for child in footer.find_all(recursive=False):
                    if child.name and child.has_attr('class'):
                        class_name = child['class'][0]  # take the first class (if multiple)
                        row[class_name] = child.get_text(strip=True)
            
            car_data.append(row)
            # print(car_data)
        page += 1 # move to next page

# ✅ Convert to DataFrame
df = pd.DataFrame(car_data)

# 🔍 Extract Mileage and Transmission using regex
df[['Mileage', 'Transmission']] = df['mod-b-card__car-other'].str.extract(r'^(.*?km)([A-Za-z].*)$')
df['Price'] = df['mod-card__price'].str.extract(r'Car Price:RM\s*([\d,]+)')
df['mod-b-card__title'] = df['mod-b-card__title'].str.replace('\n', ' ', regex=True).str.strip()
df=df.drop_duplicates()
df = df.rename(columns={
    'mod-b-card__title': 'Car Name',
    'Mileage': 'Car Mileage',
    'Transmission': 'Car Transmission',
    'mod-b-card__car-location': 'Car Location',
    'Price': 'Car Price',
    'mod-tooltipMonthPay': 'Car Instalment Monthly Amount'
})

# Define the columns you want to keep
required_columns = ['Car Name', 'Car Mileage', 'Car Transmission','Car Location', 'Car Price','Car Instalment Monthly Amount']

# Create a new DataFrame with only those columns
df_final = df[required_columns]
# Preview 
print(df_final.head())

# Save to CSV if needed
# df_final.to_csv('carsome_footer_data.csv', index=False, encoding='utf-8-sig')
df_final.to_csv('docker_output/carsome_data.csv', index=False, encoding='utf-8-sig')
print("✅ Data saved to carsome_data.csv")