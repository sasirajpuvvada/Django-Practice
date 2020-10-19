import pandas as pd
import sklearn as sk
import math

first = 'The car is driven on the road'
second = 'the truck is driven on the highway'

first = first.split(' ')
second = second.split(' ')

total = set(first).union(set(second))


wordDictA = dict.fromkeys(total,0)
wordDictB = dict.fromkeys(total,0)

for word in first:
    wordDictA[word]+=1

for word in second:
    wordDictB[word]+=1

pd.DataFrame([wordDictA,wordDictB])