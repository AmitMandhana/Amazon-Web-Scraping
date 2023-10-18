from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import csv
from time import sleep

options1 = Options()
options1.add_experimental_option("detach", True)

driver = webdriver.Chrome(
    service=ChromeService(executable_path="E:\\Selenium_tutorials\\chromedriver-win64\\chromedriver.exe"),
    options=options1
)

driver.get("https://www.amazon.in")

input_search = driver.find_element(By.ID, "twotabsearchtextbox")
search_button = driver.find_element(By.XPATH, '(//input[@type="submit"])[1]')

input_search.send_keys("Bags")
search_button.click()

product_name_path = "//span[@class='a-size-medium a-color-base a-text-normal']"
product_url_path = '//span[@class="a-size-medium a-color-base a-text-normal"]/ancestor::a'
product_price_path = '//div[@class="puisg-col-inner"]//a[@target = "_blank"]//span[@data-a-size = "xl"][1]//span[@class="a-price-whole"]'
product_rating_path = '//div[@class="puisg-col-inner"]//div[@class="a-row a-size-small"]/span[1]'
product_rating_count_path = '//div[@class="puisg-col-inner"]//span[@class="a-size-base s-underline-text"]'

ASIN_path = '//div[@id="detailBullets_feature_div"]//li[4]/span/span[2]'
manufacturer_path = '//div[@id="detailBullets_feature_div"]//li[3]/span/span[2]'
description_path = '//div[@id="productDescription"]//span'

product_names = []
product_urls = []
product_prices = []
product_ratings = []
product_rating_counts = []
ASINs = []
manufacturers = []
descriptions = []

for i in range(20):
    print(f"We are on PAGE {i+1}")

    names = driver.find_elements(By.XPATH, product_name_path)
    urls = driver.find_elements(By.XPATH, product_url_path)
    prices = driver.find_elements(By.XPATH, product_price_path)
    ratings = driver.find_elements(By.XPATH, product_rating_path)
    rating_counts = driver.find_elements(By.XPATH, product_rating_count_path)

    product_names.extend([name.text for name in names])
    product_urls.extend([url.get_attribute('href') for url in urls])
    product_prices.extend([price.text for price in prices])
    product_ratings.extend([rating.get_attribute('aria-label') for rating in ratings])
    product_rating_counts.extend([count.text for count in rating_counts])

    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
    except NoSuchElementException:
        print("Reached the last page. Exiting loop.")
        break

    sleep(4)

file_path = 'product_data.csv'

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Product URL', 'Product Price', 'Product Rating', 'Product Rating Count'])

    for name, url, price, rating, count in zip(product_names, product_urls, product_prices, product_ratings, product_rating_counts):
        writer.writerow([name, url, price, rating, count])

print(f'Data written to {file_path}')

# Extract additional information for each product
new_file_path = 'additional_product_data.csv'

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    print("The no of Rows are:",len(rows))
for i,row in enumerate(rows):

    url = row['Product URL']
    driver.get(url)
    print(f"We are on Row {i+1}")

    try:
        ASIN = driver.find_element(By.XPATH, ASIN_path).text
    except NoSuchElementException:
        ASIN = 'Not found'

    try:
        manufacturer = driver.find_element(By.XPATH, manufacturer_path).text
    except NoSuchElementException:
        manufacturer = 'Not found'

    try:
        description = driver.find_element(By.XPATH, description_path).text
    except NoSuchElementException:
        description = 'Not found'

    row['ASIN'] = ASIN
    row['Manufacturer'] = manufacturer
    row['Description'] = description

    sleep(2)  # Add a small delay to prevent overloading the server

with open(new_file_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Product Name', 'Product URL', 'Product Price', 'Product Rating', 'Product Rating Count', 'ASIN', 'Manufacturer', 'Description']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Data written to {new_file_path}')

driver.quit()
