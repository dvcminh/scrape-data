import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://21522348:5uJVhT1HGNK003jB@cluster0.czgkfdu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # Replace with your MongoDB URI
db = client['mika'] 
collection = db['product'] 

# Declare browser
driver = webdriver.Chrome()

# Open URL
driver.get("https://muathongminh.vn/laptop-c.1__101942?sort=rating_count__desc")
# sleep(random.randint(5,10))
count = 1
all_data = pd.DataFrame()
while True:
        if count > 3:
            break
        sleep(random.randint(5,7))
        try:
            print("Crawl Page " + str(count))
            sleep(random.randint(3,5))

            
            # ================================ GET link/title
            elems = driver.find_elements(By.CSS_SELECTOR , ".suggestion-item")
            title = [elem.get_attribute('title') for elem in elems]
            print('da lay duoc title')
            link = [elem.get_attribute('href') for elem in elems]
            print('da lay duoc link')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.1);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.2);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.4);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
            sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.87);")
            sleep(random.randint(3, 5))
            img_elements = driver.find_elements(By.CSS_SELECTOR, ".w-full.relative.overflow-hidden.product-img-wrap.flex-shrink-0 img")
            img_links = [elem.get_attribute('src') for elem in img_elements]
            print('da lay duoc img_links')

            # for link in links2:
            #     driver.get(link)
            #     sleep(5,7)
            #     link = driver.find_element(By.CSS_SELECTOR, ".primary.medium").get_attribute('href')



            # ================================ GET price
            elems_price = driver.find_elements(By.CSS_SELECTOR , ".text-red-500")  
            price = [elem_price.text for elem_price in elems_price]
            print('da lay duoc price')

            df1 = pd.DataFrame(list(zip(title, price, links, img_links)), columns = ['title', 'price','link_item', 'image_url'])
            df1['index_']= np.arange(1, len(df1) + 1)


            # ================================ GET location/countReviews

            elems_countReviews = driver.find_elements(By.CSS_SELECTOR , ".font-normal")
            print('da lay duoc elems_countReviews')
            countReviews = [elem.text if elem.text else "" for elem in elems_countReviews]
            print('da lay duoc countReviews')

            df1['countReviews'] = countReviews
            df1['type'] = 'shopee'
            df1['category'] = 'computerandlaptop'
            df1['subcategory'] = 'computer'

            elems_official = driver.find_elements(By.CSS_SELECTOR , ".is-desktop")
            official = [1 if elem_official.find_elements(By.CSS_SELECTOR, '._2fakLZ') else 0 for elem_official in elems_official]
            print('da lay duoc official')
            
            official_idx = []
            for i in range(1, len(title)+1):
                try:
                    official_idx.append(i)
                except NoSuchElementException:
                    print("No Such Element Exception " + str(i))
            df2 = pd.DataFrame(list(zip(official_idx, official)), columns = ['official_idx', 'official'])

            df3 = df1.merge(df2, how='left', left_on='index_', right_on='official_idx')

            data_dict = df3.to_dict("records")
            collection.insert_many(data_dict)
            print(f"Inserted {len(data_dict)} records into MongoDB")

            # ================================ Next pagination
            
            next_pagination_cmt = driver.find_element(By.CSS_SELECTOR, ".pagination-item-arrow-right")
            driver.get(next_pagination_cmt.get_attribute('href'))

            print("Clicked on button next page!")
            count += 1
            # all_data = pd.concat([all_data, df5], ignore_index=True)

        
        except Exception as e:
            print("End of pages or an error occurred: ", str(e))
            break
df1.to_csv('shopee_computer1.csv', index=False)
# df2.to_csv('shopee_computer2.csv', index=False)
df3.to_csv('shopee_computer3.csv', index=False)
driver.close()    