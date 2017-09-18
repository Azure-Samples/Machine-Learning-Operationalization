# Training file based on the scikit learn example: Working With Text Data
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html#loading-the-20-newsgroups-dataset

from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
import pickle

categories = ['comp.graphics', 'rec.autos','sci.med', 'misc.forsale']
#Running this will copy the file to the home directory. Will take a couple of minuts to download the first time.
twenty_train = fetch_20newsgroups(data_home='./data',subset='train',categories=categories, shuffle=True, random_state=42)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])

text_clf.fit(twenty_train.data, twenty_train.target)  

import numpy as np
twenty_test = fetch_20newsgroups(subset='test',categories=categories, shuffle=True, random_state=42)
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target)   

#Save the model to file
print("Export the model to model.pkl")
f = open('./outputs/model.pkl', 'wb')
pickle.dump(text_clf, f)
f.close()

docs_new = ["SUVs are very popular"]
predicted = text_clf.predict(docs_test)
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))