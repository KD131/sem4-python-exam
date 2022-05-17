import os, sys
import random
import string
from nltk import word_tokenize
from collections import defaultdict
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pickle


stop_words = set(stopwords.words('english'))
stop_words.add('said')
stop_words.add('Diller')
stop_words.add('Mand')

files_dir = 'emailDummyData/'
Labels = ['business', 'entertainment']
#, 'politics', 'sport', 'tech'
#News Articles
#emailDummyData

def create_data_set():
    with open('data.txt', 'w', encoding='utf8') as outfile:
        for label in Labels:
            dir = '%s/%s' % (files_dir, label)
            for filename in os.listdir(dir):
                fullfilename = '%s/%s' % (dir, filename)
                #print(fullfilename)
                with open(fullfilename, 'rb') as file:
                    text = file.read().decode(errors='replace').replace('\n', '')
                    text = file.read().decode(errors='replace').replace('\r', '')
                    outfile.write('%s\t%s\t%s\n' % (label, filename, text))


def setup_docs():
    docs = []
    with open('data.txt', 'r', encoding='utf8') as datafile:
        for row in datafile:
            parts = row.split('\t')
            doc = (parts[0], parts[2].strip())
            docs.append(doc)
    return docs


def get_tokens(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if not t in stop_words]
    return tokens

def clean_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    return text


def print_frequency_dist(docs):
    tokens = defaultdict(list)
    for doc in docs:
        doc_label = doc[0]
        doc_text = clean_text(doc[1])
        doc_tokens = get_tokens(doc_text)
        tokens[doc_label].extend(doc_tokens)

    for category_label, category_tokens in tokens.items():
        print(category_label)
        fd = FreqDist(category_tokens)
        print(fd.most_common(20))


def get_splits(docs):
    random.shuffle(docs)

    x_train = [] #training document
    y_train = [] #corresponding training labels

    x_test = [] #test document
    y_test = [] #corresponding test labels

    pivot = int(.80 * len(docs))

    for i in range(0, pivot):
        x_train.append(docs[i][1])
        y_train.append(docs[i][0])

    for i in range(pivot, len(docs)):
        x_test.append(docs[i][1])
        y_test.append(docs[i][0])

    return x_train, x_test, y_train, y_test



def evaluate_classifier(title, classifier, vectorizer, x_test, y_test):
    x_test_tfidf = vectorizer.transform(x_test)
    y_pred = classifier.predict(x_test_tfidf)

    #what dis?
    precision = metrics.precision_score(y_test, y_pred, average = 'micro')
    recall = metrics.recall_score(y_test, y_pred, average = 'micro')
    f1 = metrics.f1_score(y_test,y_pred, average = 'micro')

    print("%s\t%f\t%f\t%f\n" % (title, precision, recall, f1))


def train_classifier(docs):
    x_train, x_test, y_train, y_test = get_splits(docs)

    #the object that turns text into vectors
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1,3), min_df=3, analyzer = 'word' )

    #Create doc-term matrix
    dtm = vectorizer.fit_transform(x_train)

    #train naive bayes classifier whats dis?
    naive_bayes_classifier = MultinomialNB().fit(dtm, y_train)

    evaluate_classifier("Naive Bayes\tTRAIN\t", naive_bayes_classifier, vectorizer, x_train, y_train)
    evaluate_classifier("Naive Bayes\tTEST\t", naive_bayes_classifier, vectorizer, x_test, y_test)

    #store the classifier
    clf_filename = 'naive_bayes_classifer.pkl'
    pickle.dump(naive_bayes_classifier, open(clf_filename, 'wb'))

    #also store the vectorizer so we can transform new data
    vec_filename = 'count_vectorizer.pkl'
    pickle.dump(vectorizer, open(vec_filename, 'wb'))


def classify(text):
    #load classifier
    clf_filename = 'naive_bayes_classifer.pkl'
    nb_clf = pickle.load(open(clf_filename, 'rb'))

    #vectorize the new text
    vec_filename = 'count_vectorizer.pkl'
    vectorizer = pickle.load(open(vec_filename, 'rb'))

    pred = nb_clf.predict(vectorizer.transform([text]))

    print(pred[0])
    return pred[0]


if __name__ == '__main__':
    #create_data_set()
    #docs = setup_docs()

    #print_frequency_dist(docs)

    #train_classifier(docs)

    new_doc = "Hello Diller Mand. We would like to get you in to have a meeting with us. Because we think you are good at IT and would be perfect for our Job applicaiton"

    classify(new_doc)

    print('done')