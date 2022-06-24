from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
# from BeautifulSoup import BeautifulSoup
from .forms import *
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template
import datetime

# Create your views here.
def index(request):
    return render(request,'index/index.html')  

def download(request):
    
    responsecsv = HttpResponse(content_type='text/csv')
    filename = "equipo.csv"
    responsecsv['Content-Disposition'] = "attachment; filename="+filename
    writer = csv.writer(responsecsv)
    writer.writerow(['Group','Category','Code', 'long description','short_description'])
    url = "https://www.hcpcsdata.com/Codes"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    td1 = soup.find_all('tr')
    
    
    lists = []
    for i in range(1,len(td1)):
        x = td1[i].text
        y = x.split('\n')
        for k in y:
            lists.append(k.strip())
            if k.strip() != '':
                lists.append(k)
    list2 = []
    for i in lists:
        if i != '':
            list2.append(i)
    list_of_lists = [list2[i:i + 3] for i in range(0, len(list2), 3)]
    for index in range(len(list_of_lists)):
        print(list_of_lists[index])
        url2 = 'https://www.hcpcsdata.com/Codes/'+str(list_of_lists[index][0].replace("'",'').split(' ')[0])
    
        response2 = requests.get(url2)
        content2 = response2.content
        soup2 = BeautifulSoup(content2,'html.parser')
        td2 = soup2.find_all('tr')
        list2_inner = []
        for i in range(1,len(td2)):
            text2 = td2[i].text
            y = text2.split('\n')
            for k in y:
                list2_inner.append(k.strip())
        list2_inner2 = []
        for i in list2_inner:
            if i != '':
                list2_inner2.append(i)
        list_of_lists2 = [list2_inner2[i:i + 2] for i in range(0, len(list2_inner2), 2)]
        for index2 in range(len(list_of_lists2)):
            url3 = url2+'/'+str(list_of_lists2[index2][0])
            response3 = requests.get(url3)
            content3 = response3.content
            soup3 = BeautifulSoup(content3,'html.parser')
            td3 = soup3.find_all('tr')
            list3_inner = []
            for i in range(len(td3)):
                text3 = td3[0].text
                y3 = text3.split('\n')
                for k3 in y3:
                    list3_inner.append(k3.strip())
            list3inner = []
            for i in list3_inner:
                if i != '':
                    list3inner.append(i)
            list_of_lists3 = [list3inner[i:i + 2] for i in range(0, len(list3inner), 2)]
            for index3 in range(len(list_of_lists3)):
                try:
                    writer.writerow([list_of_lists[index][0],list_of_lists[index][2],list_of_lists2[index2][0],list_of_lists2[index2][1],list_of_lists3[index3][1]])
                  
                except Exception as e:
                    pass
            return responsecsv
    return render(request,'index/index.html')

def render_to_pdf(template_src, context_dict={}):
    print(context_dict)
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    text2 = html.encode('latin-1', 'replace').decode('latin-1')
    pdf = pisa.pisaDocument(BytesIO(text2.encode("latin-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# def pdf(**kwargs):
#     data = {}
#     for key, value in kwargs.items():
#         data[key] = value
#     pdf = render_to_pdf('template_pdf.html', data)
#     response = HttpResponse(pdf, content_type='application/pdf')
    
#     filename = "hsasah.pdf"
#     content = "attachment; filename=dsadsad.pdf" 
#     response['Content-Disposition'] = content
#     print(response)
#     return response      
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip   
 
def online_cusultationReport(request):
    if(request.method == "POST"):
        form = consultation_Form(request.POST)
        if form.is_valid():
            clinic_name = form.cleaned_data['clinic_name']
            clinic_logo = form.cleaned_data['clinic_logo']
            physician_name = form.cleaned_data['physician_name']
            physician_contact = form.cleaned_data['physician_contact']
            patient_firstname = form.cleaned_data['patient_firstname']
            patient_lastname = form.cleaned_data['patient_lastname']
            patient_dob = form.cleaned_data['patient_dob']
            patient_contact = form.cleaned_data['patient_contact']
            cheif_complaint = form.cleaned_data['cheif_complaint']
            consultation_note = form.cleaned_data['consultation_note']
            data = {
                'clinic_name' : clinic_name,
                'clinic_logo' : clinic_logo,
                'physician_name' : physician_name,
                'physician_contact' : physician_contact,
                'patient_firstname' : patient_firstname,
                'patient_lastname' : patient_lastname,
                'patient_dob' : patient_dob,
                'patient_contact' : patient_contact,
                'cheif_complaint' : cheif_complaint,
                'consultation_note' : consultation_note,
                'time' : datetime.datetime.now(),
                'ipaddress' : get_client_ip(request)
            }
            pdf = render_to_pdf('template_pdf.html', data)
            response = HttpResponse(pdf, content_type='application/pdf')
            
            filename = "CR_{}_{}_{}.pdf".format(patient_firstname,patient_lastname,patient_dob)
            content = "attachment; filename={}".format(filename) 
            response['Content-Disposition'] = content
            return response 
           
    context = {
        'form' : consultation_Form()
    }
    return render(request,"cunsultation/cunsultation_report.html",context)

