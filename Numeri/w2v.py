import gensim, logging
import numpy as np
from scipy import spatial
import sys
import re
import json

from nltk.corpus import stopwords


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

path_json = "music2.json"

with open(path_json) as data_file:    
    data = json.load(data_file)

sentences = []
names = []
reviews = []

for key in data:
    tmp =  data[key]
    if "id3" in tmp:
        id = tmp["id3"]
        if ("artist" in id) and ("title" in id):
            artist_name =  id["artist"]
            title_name = id["title"]

            nm = artist_name + ':' + title_name
            lyr = id["lyrics"]

            if (len(lyr)>1):
            
                lyr = re.sub("[^a-zA-Z]"," ", lyr)
                words = lyr.lower().split()

                stops = set(stopwords.words("english"))
                review = [w for w in words if not w in stops]
                
                sentences.append(words)
                names.append(nm)
                reviews.append(review)


model = gensim.models.Word2Vec(sentences, min_count=5, size=200)


# from https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-3-more-fun-with-word-vectors


def makeFeatureVec(words, model, num_features):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,),dtype="float32")
    #
    nwords = 0.
    # 
    # Index2word is a list that contains the names of the words in 
    # the model's vocabulary. Convert it to a set, for speed 
    index2word_set = set(model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set: 
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])
    # 
    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec,nwords)
    return featureVec


def getAvgFeatureVecs(reviews, model, num_features):
    # Given a set of reviews (each one a list of words), calculate 
    # the average feature vector for each one and return a 2D numpy array 
    # 
    # Initialize a counter
    counter = 0.
    # 
    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    # 
    # Loop through the reviews
    for review in reviews:
       
       # Print a status message every 1000th review
       # if (counter%1000. == 0.):
       #    print ("Review %d of %d", (counter, len(reviews)))
        
       # Call the function (defined above) that makes average feature vectors
    
       reviewFeatureVecs[counter] = makeFeatureVec(review, model, num_features)
       
       # Increment the counter
       counter = counter + 1.
    return reviewFeatureVecs



DataVecs = getAvgFeatureVecs(reviews, model, 200)
l = DataVecs.shape[0]

f = open("w2v_num.tsv", 'w')

for i in range(l):
    tmp = '"%s" \t %s \n' % (names[i], str(DataVecs[i]))
    f.write(tmp)

    
