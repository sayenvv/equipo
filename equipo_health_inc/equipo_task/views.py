from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

# Create your views here.
def index(request):
    return render(request,'index/index.html')  

def download(request):
    # driver = webdriver.Chrome("/home/sayen/chromedriver ")
    products=[] #List to store name of the product
    prices=[] #List to store price of the product
    ratings=[] #List to store rating of the product
    url = "https://www.hcpcsdata.com/Codes"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    # print(soup.prettify())
    # print(soup.findall('tr'))
    # driver.get("https://www.hcpcsdata.com/Codes")
    # print(driver,"ddd")
    Product_Fields = []

    for i in soup.find_all('tr',class_='clickable-row'):
        # print(i,"this data")
        url2 = 'https://www.hcpcsdata.com'+i.get('data-href')
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.content,'html.parser')
        Product_Fields =[[[m.text for m in j.find_all('td')][0].replace("\n","").replace("\r\n","").replace("\r",""),[m.text for m in j.find_all('td')][1].replace("\n","").replace("\r\n","").replace("\r","")] for j in soup2.find_all('tr',class_='clickable-row')]
        # Product_Fields =[l,k for l,k in zip([j.find_all('td')][0].replace("\n","").replace("\r\n","").replace("\r","")],[j.find_all('td')][1].replace("\n","").replace("\r\n","").replace("\r","")])) for j in soup2.find_all('tr',class_='clickable-row')]
        response = HttpResponse(content_type='text/csv')
        filename = "ProductListBycategory.csv"
        response['Content-Disposition'] = "attachment; filename="+filename
        writer = csv.writer(response)
        writer.writerow(['Group','Category','Code', 'long description', 'short description'])
    count=0
    for pro in Product_Fields:
        count+=1
        writer.writerow([pro])
    return response
    
 
    