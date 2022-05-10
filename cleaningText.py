import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer


from string import punctuation

def cleaningText(text):
    #Tokenizes the text
    tokens = word_tokenize(text)
    #tokens = list(map(str.lower,tokens))

    #if we want to remove stopwords ("this, and , are , is") and punctuation such as (., , , ?, !)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words and not w in punctuation]

    #stemming the text with SnowballStemmer this is in general better, and can take different language such as danish!
    #Init the stemmer
    #sn_stemmer = SnowballStemmer("english") # Can be change to danish
    #words=["connect","connected","connection","connections","connects","house","housing"] #Word to see if the stemmer is working 
    #tokens = [sn_stemmer.stem(word=word) for word in tokens]

    #Lemmatization considers the context and converts the word to its meaningful base form, which is called Lemma. Sometimes, the same word can have multiple different Lemmas
    #Init the lemma.
    lemmatizer = WordNetLemmatizer()
    #words=["trouble","troubling","troubled","troubles"] #Words to see if the lemma is working. 
    tokens = [lemmatizer.lemmatize(word=word,pos='v') for word in tokens]

    #gives a pos tag to every word
    tokens = nltk.pos_tag(tokens)

    #Ner tagging
    tokens = nltk.ne_chunk(tokens)

    return tokens


if __name__ == '__main__':
    text = "Hello NASA my name isn't Kasper but August. CAN YOU believe that? I am born in 1993. I have $2.1 million and I work for GooglE. and did you give birth to a young boy? Look at that bear!"
    print(cleaningText(text))


