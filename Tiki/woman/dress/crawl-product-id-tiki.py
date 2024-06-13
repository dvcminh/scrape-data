import requests
import time
import random
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'version': 'home-persionalized',
    'trackity_id': '1ff19c9a-17ce-afec-4968-3defc4dde472',
    'category': '941',
    'page': '1',
    'src': 'c1883',
    'urlKey':  'dam-vay-lien',  
}

product_detailparams = {
    'platform': 'web',
    'spid': '1',
}

product_id = []
try:
    for i in range(1, 11):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
        if response.status_code == 200:
            print('request success!!!')
            for record in response.json().get('data'):
                quantity_sold = record.get('quantity_sold')
                quantity_sold_text = quantity_sold.get('text') if quantity_sold and quantity_sold.get('text') else '0'
                
                # product_detailparams['spid'] = record.get('id')
                product_description = requests.get('https://tiki.vn/api/v2/products/' + str(record.get('id')), headers=headers).json().get('description')          
                
                
                product = {
                    'title': record.get('name'),
                    'price': record.get('price'),   
                    'link_item': 'https://tiki.vn/' + record.get('url_path'),
                    'image_url': record.get('thumbnail_url'),
                    'discount_percent_list': record.get('discount_rate'),
                    'review_count': str(record.get('review_count')) + ' ' + quantity_sold_text,      
                    'description': product_description,  
                    'type': "tiki",                                                                 
                    'category': "abc",
                    'subcategory': "xyz",
                    'official': record.get('visible_impression_info').get('amplitude').get('is_authentic')
                }
                product_id.append(product)
        time.sleep(random.randrange(3, 10))
except Exception as e:
    print("End of pages or an error occurred: ", str(e))

df = pd.DataFrame(product_id)
df.to_csv('product_id_ncds.csv', index=False)