from . import constants
from pymongo import MongoClient
import requests
import bs4
from .configurations import client

links = []
def display():
    db = client[constants.db]
    news = db[constants.news]
    titles = []
    for val in news.find({}):
        titles.append(val['url'])
    return titles

def addNews():
    db = client[constants.db]
    news = db[constants.news]
    newsData = db[constants.newsData]
    page = 14
    
    while True:
        url = constants.URL
        pageStr = str(page)
        url = url + pageStr

        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text,'lxml')
        content = soup.select('.storylink')
        score = soup.find_all('span',class_='score')
        age = soup.find_all('span',class_='age')
        for index in range(len(score)):
            title = content[index].get_text()
            link = content[index]['href']
            if 'pdf' in link:
                print('skipped')
                continue    
            scoreValue = score[index].get_text()
            time = age[index].get_text()

            if urlExists(news,link):
                continue
            
            
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
    
    return "news added"



def urlExists(news,currentLink):
    if len(links) == 0:
        for val in news.find({}):
            links.append(val['url'])
    if currentLink in links:
        return True
    else:
        return False