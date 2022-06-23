from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
# from BeautifulSoup import BeautifulSoup
from .forms import *
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

# Create your views here.
def index(request):
    return render(request,'index/index.html')  

def download(request):

    url = "https://www.hcpcsdata.com/Codes"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    data = {}
    td1 = soup.find_all('tr')[:10]
    for key1,key2,key3 in zip(range(0,len(td1)-1,3),range(0,len(td1)-1,2),range(2,len(td1))):
        print(td1)
        url2 = 'https://www.hcpcsdata.com'+td1[key1].find('a').get('href')
        response2 = requests.get(url2)
        
        soup2 = BeautifulSoup(response2.content,'html.parser')
        td2 = soup2.find_all('td')[:10]
        for x,y in zip(range(0,len(td2)-1,2),range(0,len(td2)-1,3)):
         
            # print(td2)

            response = HttpResponse(content_type='text/csv')
            filename = "equipo.csv"
            response['Content-Disposition'] = "attachment; filename="+filename
            writer = csv.writer(response)
            writer.writerow(['Group','Category','Code', 'long description','count'])
            writer.writerow([td1[key1].text.strip(),td1[key2].text.strip(),td2[x].text.strip(),td2[y].text.strip()])
    return response
 
def online_cusultationReport(request):
    form = consultation_Form()
    return render(request,"cunsultation/cunsultation_report.html",locals())