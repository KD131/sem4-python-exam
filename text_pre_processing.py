from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from string import punctuation
from dateutil import parser
import parsedatetime as pdt

def download():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

def process(sentence):
    # [_three-word]
    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
        if (t1 == 'NN' and t3 == 'CD'):
            print(w1, w2, w3)  # [_print-words]
            print(t1, t2, t3)
        if (t1 == 'CD' and t3 == 'NN'):
            print(w1, w2, w3)  # [_print-words]
            print(t1, t2, t3)

def tokenize(text):
    return word_tokenize(text)

def remove_stopwords(tokens, lang):
    stop_words = set(stopwords.words(lang))
    return [w for w in tokens if not w in stop_words and not w in punctuation]

def snowball_stem(tokens, lang):
    #stemming the text with SnowballStemmer this is in general better, and can take different language such as danish!
    sn_stemmer = SnowballStemmer(lang) # Can be change to danish
    return [sn_stemmer.stem(word=word) for word in tokens]

def lemmatize(tokens):
    #Lemmatization considers the context and converts the word to its meaningful base form, which is called Lemma. 
    #Sometimes, the same word can have multiple different Lemmas
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word=word,pos='v') for word in tokens]

def pos_tag(tokens):
    return nltk.pos_tag(tokens)

def ner_tag(tokens):
    return nltk.ne_chunk(tokens)

def pre_process_text(text):
    lang = 'english'
    tokens = tokenize(text)
    tokens_minus_stopwords = remove_stopwords(tokens, lang)
    # Either stem or lem
    #tokens_stemmed = snowball_stem(tokens_minus_stopwords)
    tokens_lemmatized = lemmatize(tokens_minus_stopwords)
    #tokens_pos_tagged = pos_tag(tokens_stemmed)
    tokens_pos_tagged = pos_tag(tokens_lemmatized)
    tokens_ner_tagged = ner_tag(tokens_pos_tagged)
    return tokens_ner_tagged


if __name__ == '__main__':
    text = "Hello Johan. Would you like to hangout tonight? We meet at struenseegade 29 st. tv. 2200 København N"
    #text = tokenize(text)
    #text = pos_tag(text)
    result = pre_process_text(text)
    print(result)
    #print(type(output))
    #output = pre_process_text(text)
    #print(output)


