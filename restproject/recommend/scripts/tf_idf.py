
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


def pre_processing():

    '''
        removes stop words and special characthers
    '''
    
    db = client[constants.db]
    newsData = db[constants.newsData]
    for newsVal in newsData.find({}):
        status = newsVal['status']
        if not status:
            desc = newsVal['description']
            
            desc = remove_special_characthers(desc)
            desc = remove_stop_words(desc)
            
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
        Adding all words in IDF array
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
        IDF[word] = 1 + log(size/count)
    

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
    pre_processing()

    #calculating tf-idf
    calculate()


def remove_tokens(words):

    token = []
    words = words.split(' ')
    for w in words:
        token.append(p_stemmer.stem(w))
    return token

def processTitle(title, words):
    title = remove_special_characthers(title)
    title = remove_stop_words(title)
    title = remove_tokens(title)
    value = 0
    for titleWord in title:
        if titleWord in words:
            value = value + 1
    # print(title)
    return value



def find_favourites(words):
    ans = {}

    for key,value in TF_IDF.items():
        count = 0
        for word in words:
            if word in value:
                count += value[word]
        
        wcd = WCD[key]
        title = wcd['title']
        url = wcd['url']
        count += processTitle(title, words)
        ans.update({url:count})
        
    
    favs = sorted(ans.items(), key=lambda x: x[1], reverse = True)

    return favs[:10]
        



def get_values():
    db = client[constants.db]
    for obj in db['tf_idf'].find():
        WCD.update(obj['WCD'])
        TF_IDF.update(obj['TF_IDF'])



def search(words):
    words = 'artificial intelligence'
    get_values()
    words = remove_special_characthers(words)
    words = remove_stop_words(words)
    words = remove_tokens(words)
    favs = find_favourites(words)
    return favs
    