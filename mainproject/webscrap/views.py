from django.shortcuts import render, HttpResponse
from  calculate import views
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import bs4
from pymongo import MongoClient
# Create your views here.

def index(request):
    i = 0
    page = 1
    dict = {0:'val'}
    dict.popitem()
    democlient = MongoClient()
    client = MongoClient('localhost',27017)
    db = client['temp']
    news = db['news']
    while True:
        url = 'https://news.ycombinator.com/news?p='
        pageStr = str(page)
        url = url + pageStr

        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text,'lxml')
        content = soup.select('.storylink')
        score = soup.find_all('span',class_='score')
        age = soup.find_all('span',class_='age')
        for index in range(len(score)):
            i = i + 1
            title = content[index].get_text()
            link = content[index]['href']
            scoreValue = score[index].get_text()
            time = age[index].get_text()
            value = str(title+" "+link+"   "+scoreValue+"  "+time)
            dict[i] = value
            data = {"title":title, "url":link, "points":scoreValue, "time":time}
            news.insert_one(data)
        
        
        moreLink = soup.select('.morelink')
        
        if len(moreLink) == 0:
            break
        page = page + 1
        if page == 2:
            break
    return JsonResponse(dict)

