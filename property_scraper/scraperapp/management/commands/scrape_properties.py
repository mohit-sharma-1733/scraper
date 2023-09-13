import time
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from scraperapp.models import Property



# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

# Set up the Chrome WebDriver with the configured options
browser = webdriver.Chrome(options=chrome_options)

# Define a function to scrape property data
def scrape_properties_task(city, locality):
    base_url = f"https://www.99acres.com/search/property/buy/{city.lower()}-all?city=38&preference=S&area_unit=1&res_com=R"
    
    try:
        browser.get(base_url)
        time.sleep(5)  # Allow time for page to load

        # Scroll the page to load more results (adjust as needed)
        for _ in range(3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Extract property details and store them in MongoDB
        for property_elem in soup.find_all('div', class_='srpTuple__tupleDetails'):
            property_name_elem = property_elem.find('a', class_='srpTuple__propertyName')
            if property_name_elem:
                property_name = property_name_elem.h2.text.strip()
            else:
                property_name = "Property Name Not Found"

            property_price_elem = property_elem.find('td', id='srp_tuple_price')
            if property_price_elem:
                property_price = property_price_elem.text.strip()
            else:
                property_price = "Price Not Found"

            property_area_elem = property_elem.find('td', id='srp_tuple_primary_area')
            if property_area_elem:
                property_area = property_area_elem.text.strip()
            else:
                property_area = "Area Not Found"

            property_type_elem = property_elem.find('td', id='srp_tuple_bedroom')
            if property_type_elem:
                property_type = property_type_elem.text.strip()
            else:
                property_type = "Type Not Found"

            property_link_elem = property_name_elem['href']

            # Extract Property Locality and Property City
            property_locality = locality
            property_city = city

            # Create and save a Property document to MongoDB
            property_doc = Property(
                property_name=property_name,
                property_cost=property_price,
                property_type=property_type,
                property_area=property_area,
                property_locality=property_locality,
                property_city=property_city,
                individual_property_link=property_link_elem
            )
            property_doc.save()

    except Exception as e:
        print(f"An error occurred: {e}")

# List of cities and localities
cities_and_localities = [
    ("Pune", "Baner"),
    ("Delhi", "Dwarka"),
    ("Mumbai", "Andheri"),
    ("Lucknow", "Gomti Nagar"),
    ("Agra", "Tajganj"),
    ("Ahmedabad", "Bodakdev"),
    ("Kolkata", "Salt Lake City"),
    ("Jaipur", "Malviya Nagar"),
    ("Chennai", "Adyar"),
    ("Bengaluru", "Whitefield")
]

# Schedule the task to run twice a day
for city, locality in cities_and_localities:
    # Schedule the task to run at 8 AM and 8 PM (adjust time as needed)
   # scrape_properties_task(city,locality)
    schedule.every().day.at("08:00").do(scrape_properties_task, city, locality)
    schedule.every().day.at("20:00").do(scrape_properties_task, city, locality)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
