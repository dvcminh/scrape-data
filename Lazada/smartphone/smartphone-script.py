import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
# Declare browser
driver = webdriver.Chrome()

# Open URL
driver.get("https://www.lazada.vn/dien-thoai-di-dong/?spm=a2o4n.searchlistcategory.cate_1.1.6d6025bcfmlbiE")
sleep(random.randint(5,10))
count = 1
all_data = pd.DataFrame()
while True:
        if count > 10:
            break
        sleep(random.randint(3,5))
        try:
            print("Crawl Page " + str(count))
            
            # ================================ GET link/title
            elems = driver.find_elements(By.CSS_SELECTOR , ".RfADt [href]")
            title = [elem.text for elem in elems]
            links = [elem.get_attribute('href') for elem in elems]
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
            img_elements = driver.find_elements(By.CSS_SELECTOR, "._95X4G .picture-wrapper.jBwCF img")
            img_links = [elem.get_attribute('src') for elem in img_elements]


            # ================================ GET price
            elems_price = driver.find_elements(By.CSS_SELECTOR , ".aBrP0")  
            price = [elem_price.text for elem_price in elems_price]
            df1 = pd.DataFrame(list(zip(title, price, links, img_links)), columns = ['title', 'price','link_item', 'image_url'])
            df1['index_']= np.arange(1, len(df1) + 1)



            # ================================GET discount

            elems_discount = driver.find_elements(By.CSS_SELECTOR , ".WNoq3")
            discount_all = [elem.text for elem in elems_discount]

            # elems_discount = driver.find_elements(By.CSS_SELECTOR , ".WNoq3 ._1m41m")
            # discount = [elem.text for elem in elems_discount]

            # elems_discountPercent = driver.find_elements(By.CSS_SELECTOR , ".WNoq3 .IcOsH")
            # discountPercent = [elem.text for elem in elems_discountPercent]

            discount_idx, discount_percent_list = [], []
            for i in range(1, len(title)+1):
                try:
                    # discount = driver.find_element("xpath", "/html/body/div[3]/div/div[3]/div[1]/div/div[1]/div[2]/div[{}]/div/div/div[2]/div[4]/span[1]/del".format(i))
                    # discount_list.append(discount.text)
                    # discount_percent = driver.find_elements(By.CSS_SELECTOR , ".WNoq3 .IcOsH")
                    # discount_percent_list.append(discount_percent.text)
                    print(i)
                    discount_idx.append(i)
                except NoSuchElementException:
                    print("No Such Element Exception " + str(i))

            df2 = pd.DataFrame(list(zip(discount_idx, discount_all)), columns = ['discount_idx', 'discount_percent_list'])

            df3 = df1.merge(df2, how='left', left_on='index_', right_on='discount_idx')


            # ================================ GET location/countReviews

            elems_countReviews = driver.find_elements(By.CSS_SELECTOR , "._6uN7R")
            countReviews = [elem.text for elem in elems_countReviews]
            subcategory = driver.find_element(By.CSS_SELECTOR, ".breadcrumb_item_anchor_last").text

            df3['countReviews'] = countReviews
            df3['type'] = 'lazada'
            df3['category'] = 'smartphone'
            df3['subcategory'] = subcategory
            # ================================ GET official status
            elems_official = driver.find_elements(By.CSS_SELECTOR , ".RfADt")
            official = ['1' if elem_official.find_elements(By.CSS_SELECTOR, 'i.ic-dynamic-badge-76432') else '0' for elem_official in elems_official]
            
            official_idx = []
            for i in range(1, len(title)+1):
                try:
                    official_idx.append(i)
                except NoSuchElementException:
                    print("No Such Element Exception " + str(i))
            df4 = pd.DataFrame(list(zip(official_idx, official)), columns = ['official_idx', 'official'])

            df5 = df3.merge(df4, how='left', left_on='index_', right_on='official_idx')

            # ================================ Next pagination
            
            next_pagination_cmt = driver.find_element(By.CSS_SELECTOR, ".ant-pagination-next .ant-pagination-item-link")
            next_pagination_cmt.click()

            print("Clicked on button next page!")
            sleep(random.randint(1,3))
            try:
                close_btn = driver.find_element("xpath", "/html/body/div[7]/div[2]/div") 
                close_btn.click()
                print("Clicked on button exit!")
                sleep(random.randint(1,3))
            except:
                pass
            count += 1
            all_data = pd.concat([all_data, df5], ignore_index=True)
        except Exception as e:
            print("End of pages or an error occurred: ", str(e))
            break

all_data.to_csv('lazada.csv', index=False)

# ================================ GET more infor of each item  
# list1 = []
# list1 = [1,2,3,4] + list1     

# driver.get(links[0])

# elems_name = driver.find_elements(By.CSS_SELECTOR , ".middle")
# name_comment = [elem.text for elem in elems_name]

# elems_content = driver.find_elements(By.CSS_SELECTOR , ".item-content .content")
# content_comment = [elem.text for elem in elems_content]

# elems_skuInfo= driver.find_elements(By.CSS_SELECTOR , ".item-content .skuInfo")
# skuInfo_comment = [elem.text for elem in elems_skuInfo]

# elems_likeCount = driver.find_elements(By.CSS_SELECTOR , ".item-content .bottom .left .left-content")
# like_count = [elem.text for elem in elems_likeCount]

# df4 = pd.DataFrame(list(zip(name_comment , content_comment, skuInfo_comment, like_count)), 
#                    columns = ['name_comment', 'content_comment','skuInfo_comment', 'like_count'])
# # df4['link_item'] = links[0]
# df4.insert(0, "link_item", links[0])

# # ================================ next pagination
# # next_pagination_cmt = driver.find_element("xpath", "/html/body/div[4]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]")
# # next_pagination_cmt.click()
# # sleep(random.randint(1,3))
# # close_btn = driver.find_element("xpath", "/html/body/div[7]/div[2]/div")
# # close_btn.click()


# # ================================
# count = 1
# name_comment, content_comment, skuInfo_comment, like_count = [], [], [], []
# while count < 10:
#     try:
#         print("Crawl Page " + str(count))
#         elems_name = driver.find_elements(By.CSS_SELECTOR , ".middle")
#         name_comment = [elem.text for elem in elems_name] + name_comment
        
#         elems_content = driver.find_elements(By.CSS_SELECTOR , ".item-content .content")
#         content_comment = [elem.text for elem in elems_content] + content_comment
        
#         elems_skuInfo= driver.find_elements(By.CSS_SELECTOR , ".item-content .skuInfo")
#         skuInfo_comment = [elem.text for elem in elems_skuInfo] + skuInfo_comment
        
#         elems_likeCount = driver.find_elements(By.CSS_SELECTOR , ".item-content .bottom .left .left-content")
#         like_count = [elem.text for elem in elems_likeCount] + like_count

#         next_pagination_cmt = driver.find_element("xpath", "/html/body/div[4]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]")
#         next_pagination_cmt.click()
#         print("Clicked on button next page!")
#         sleep(random.randint(1,3))
#         # try:
#         #     close_btn = driver.find_element("xpath", "/html/body/div[7]/div[2]/div") 
#         #     close_btn.click()
#         #     print("Clicked on button exit!")
#         #     sleep(random.randint(1,3))
#         # # except ElementNotInteractableException:
#         # #     continue
#         # except NoSuchElementException:
#         #     print("No Such Element Exception!")
#         #     continue
#         sleep(random.randint(1,3))
#         count += 1
#     except ElementNotInteractableException:
#         print("Element Not Interactable Exception!")
#         break
#     except:
#         print("Error!")
#         break
    
# df4 = pd.DataFrame(list(zip(name_comment , content_comment, skuInfo_comment, like_count)), 
#                    columns = ['name_comment', 'content_comment','skuInfo_comment', 'like_count'])
# # df4['link_item'] = links[0]
# df4.insert(0, "link_item", links[0])    
    
# =============================================================================


# ============================GET INFOMATION OF ALL ITEMS
# def getDetailItems(link):
#     driver.get(link)
#     count = 1
#     name_comment, content_comment, skuInfo_comment, like_count = [], [], [], []
#     while True:
#         try:
#             print("Crawl Page " + str(count))
#             elems_name = driver.find_elements(By.CSS_SELECTOR , ".middle")
#             name_comment = [elem.text for elem in elems_name] + name_comment
            
#             elems_content = driver.find_elements(By.CSS_SELECTOR , ".item-content .content")
#             content_comment = [elem.text for elem in elems_content] + content_comment
            
#             elems_skuInfo= driver.find_elements(By.CSS_SELECTOR , ".item-content .skuInfo")
#             skuInfo_comment = [elem.text for elem in elems_skuInfo] + skuInfo_comment
            
#             elems_likeCount = driver.find_elements(By.CSS_SELECTOR , ".item-content .bottom .left .left-content")
#             like_count = [elem.text for elem in elems_likeCount] + like_count
#             next_pagination_cmt = driver.find_element("xpath", "/html/body/div[4]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]")
#             next_pagination_cmt.click()
#             print("Clicked on button next page!")
#             sleep(random.randint(1,3))
#             try:
#                 close_btn = driver.find_element("xpath", "/html/body/div[7]/div[2]/div") 
#                 close_btn.click()
#                 print("Clicked on button exit!")
#                 sleep(random.randint(1,3))
#             except:
#                 pass
#             count += 1
#         except Exception as e:
#             print("End of pages or an error occurred: ", str(e))
#             break
        
#     df4 = pd.DataFrame(list(zip(name_comment , content_comment, skuInfo_comment, like_count)), 
#                        columns = ['name_comment', 'content_comment','skuInfo_comment', 'like_count'])
#     # df4['link_item'] = links[0]
#     df4.insert(0, "link_item", link)
#     return df4

# df_list = []
# for link in links:
#     df = getDetailItems(link)
#     df_list.append(df)

# df_all = pd.concat(df_list, ignore_index=True)

# df_all.to_csv('lazada_comment.csv', index=False)


# Close browser
driver.close()    