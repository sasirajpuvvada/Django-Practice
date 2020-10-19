from sklearn.feature_extraction.text import TfidfVectorizer

firstV = 'the  car is friven on the roadway'
secondV = 'the truck is driven on the highway'

vectorize = TfidfVectorizer()

response = vectorize.fit_transform([firstV,secondV])

print(response)