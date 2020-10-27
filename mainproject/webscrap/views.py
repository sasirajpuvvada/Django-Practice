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
    newsData = db['newsData']
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
            if 'pdf' in link:
                print('skipped')
                continue    
            scoreValue = score[index].get_text()
            time = age[index].get_text()
            value = str(title+" "+link+"   "+scoreValue+"  "+time)
            dict[i] = value
            print(value)
            try:
                resLink = requests.get(link)
                soupLink = bs4.BeautifulSoup(resLink.text,'lxml')
            except:
                print("************************************Exception**********************************************8")
                continue
            try:
                heading = soupLink.select('title')
            except:
                heading = soupLink.select('.title')
            
            description = soupLink.select('p')

            data = {"title":title, "url":link, "points":scoreValue, "time":time}
            newsID = news.insert_one(data)

            if len(heading) == 0:
                heading = ''
            else:
                heading = heading[0].get_text()
            
            descData = ''
            if len(description) != 0:
                for val in description:
                    desc = val.get_text()
                    descData = descData + desc

            newsDataValues = {"title":heading,"heading":newsID.inserted_id,"description":descData}
            newsData.insert_one(newsDataValues)
        
        
        moreLink = soup.select('.morelink')
        
        if len(moreLink) == 0:
            break
        page = page + 1

        if page == 4:
            break
        
        
    return JsonResponse(dict)

