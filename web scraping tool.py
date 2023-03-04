#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask , render_template , request , jsonify           #web scraping tool
from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen as urReq
import requests
import pandas as pd
flipcart_url = "https://www.flipkart.com/search?q="+"iphone7"

response_website = urReq(flipcart_url)

data_flipcart = response_website.read()
#data_flipkart.encoding='utf-8'
beautifyed_html =bs(data_flipcart,"html.parser")
bigbox = beautifyed_html.find_all("div" , {"class":"_1AtVbE col-12-12" })
product3 = "https://www.flipkart.com" + bigbox[3].div.div.div.a['href'].replace('/p','/product-reviews',1)
product33=requests.get(product3)
product33.encoding= 'utf-8'
product3_page = bs(product33.text,"html.parser")
total_reviews=product3_page.find_all('div',{'class':'row _2afbiS'})[1].div.text.split(' ')[0].replace(',','')
for i in range(1,int(total_reviews)//(int(total_reviews)//10)+1):
    prodrev=requests.get(product3+'&page='+str(i))
    prodrev.encoding= 'utf-8'
    product3_page = bs(prodrev.text,"html.parser")
    all_review = product3_page.find_all('div', {"class":"_16PBlm"})

    comment_header=[]
    ratings=[]
    customer_name=[]
    long=[]
    customer_location=[]
    d={}
    try:
        for i in range(len(all_review)):
            comment_header.append(all_review[i].div.div.div.p.text)
            ratings.append(all_review[i].div.div.div.div.text)
            customer_name.append(all_review[i].find_all('p',{'class':"_2sc7ZR _2V5EHH"})[0].text)
            long.append(all_review[i].div.find_all('div' , {'class' : ""})[0].div.text)
            customer_location.append(all_review[i].find_all('p',{'class':"_2mcZGG"})[0].text)
    #d={"customer_name":customer_name,"comment_header":comment_header,"long":long,"ratings":ratings,"location":customer_location}
    #df=pd.DataFrame(d)
    #df.to_excel(r'C:\Users\TIWARI 210113\Downloads\Data science\data fsds\Flipkart.xlsx')
    except (NameError,AttributeError) as e:
        d['comment_header']=comment_header
        d['ratings']=ratings
        d['customer_name']=customer_name
        d['long']=long
        d['location']=customer_location
        df=pd.DataFrame(d)
        print(df)
        df.to_excel(r'C:\Users\TIWARI 210113\Downloads\Data science\data fsds\Flipkart1.xlsx')
    

