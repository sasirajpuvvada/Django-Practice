
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from collections import Counter
from bson.objectid import ObjectId
from math import log

from nltk.stem import SnowballStemmer

from . import constants
from .constants import WORD_COUNT_DICT as WCD
from .constants import TF_IDF
from .constants import INVERSE_DOCUMENT_FREQUENCY as IDF
from .configurations import client


p_stemmer = SnowballStemmer("english")

def remove_special_characthers(desc):
    desc = desc.lower()
    return re.sub('[^A-Za-z0-9]+',' ',desc)

def remove_stop_words(desc):

    filtered_sentence_string = ''
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(desc) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence_string = ' '.join(map(str, filtered_sentence))
    # print(filtered_sentence)
    return filtered_sentence_string


def filterateData():

    '''
        removes stop words and special characthers
    '''
    
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


def wordCountDict():

    db = client[constants.db]
    news = db[constants.news]
    newsData = db[constants.newsData]

    for doc_news in newsData.find({}):
        desc = doc_news['description']
        title = doc_news['title'].lower()
        id = str(doc_news['heading'])

        newsDoc = news.find_one({"_id":ObjectId(id)})
        url = newsDoc['url']
        desc = desc.split(' ')
        token = []
        for w in desc:
            token.append(p_stemmer.stem(w))
        count = dict(Counter(token))
        
        WCD[id] = {'count':count, 'url': url, 'title': title}
        

def calculate_IDF():

    '''
        Adding all words in IDF arrat
    '''
    for item in WCD:
        for word in WCD[item]['count']:
            if word not in IDF:
                IDF[word] = 1
            else:
                IDF[word] += 1
    
    '''
        calculating IDF 
    '''
    size = len(WCD)
    for word, count in IDF.items():
        IDF[word] = 1 + log(count/size)
    

def calculate_Tf_IDF():

    for item in WCD:
        tf = WCD[item]['count']
        size = len(tf)
        for key, val in tf.items():
            tf[key] = val/float(size) * IDF[key]
        TF_IDF[item] = tf


def calculate():
    print('WCD....')
    wordCountDict()
    print('IDF.......')
    calculate_IDF()
    print('TF-IDF.......')
    calculate_Tf_IDF()
    db = client[constants.db]
    td_idf_db = db['tf_idf']
    td_idf_db.drop()
    td_idf_db.insert_one({'WCD': WCD, 'IDF': IDF, 'TF_IDF':TF_IDF})



def letsStart():

    #filtering data
    # filterateData()

    #calculating tf-idf
    calculate()
    

    
    
