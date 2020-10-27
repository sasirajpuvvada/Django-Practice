from pymongo import MongoClient
from . import constants
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 



def removeSpecialCharacthers(desc):
    desc = desc.lower()
    return re.sub('[^A-Za-z0-9]+',' ',desc)

def removeStopWords(desc):

    filtered_sentence_string = ''
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(desc) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence_string = ' '.join(map(str, filtered_sentence))
    # print(filtered_sentence)
    return filtered_sentence_string



def letsStart():

    democlient = MongoClient()
    client = MongoClient('localhost',27017)
    db = client[constants.db]
    newsData = db[constants.newsData]
    for newsVal in newsData.find({}):
        status = newsVal['status']
        if not status:
            desc = newsVal['description']
            # print(desc,len(desc))
            desc = removeSpecialCharacthers(desc)
            desc = removeStopWords(desc)
            # print(desc,len(desc))
            id = newsVal['_id']
            newsData.update_one({"_id": id}, {"$set": { "description": desc} })
            newsData.update_one({"_id": id}, {"$set": { "status": True} })

    
    
