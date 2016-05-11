from sklearn.feature_extraction.text import CountVectorizer
import pandas
from scipy import spatial


path = "lyrics_all.tsv"

data = pandas.read_csv(path, header = 0, delimiter = "\t", names=['name','lyrics'] )


vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

bow = vectorizer.fit_transform(data['lyrics'])

bow_array = bow.toarray()



l = len(bow_array)

#closest song to first:

m = 0
n = 0

for i in range(1,l):
    res = 1 - spatial.distance.cosine(bow_array[0], bow_array[i])
    if (res > m):
        m = res
        n = i


print(m, data[name][n])
