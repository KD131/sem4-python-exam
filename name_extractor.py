import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize

def download_names():
    nltk.download('names')

def extract_names(text):
    tokens = word_tokenize(text)
    with open('data/danish_names/fornavne-m-alle.txt', encoding='utf8') as dmn_file:
        with open('data/danish_names/fornavne-k-alle.txt', encoding='utf8') as dfn_file:
            danish_female_names = dfn_file.readlines()
            danish_male_names = dmn_file.readlines()
            global_names = nltk.corpus.names.words()
            # Combine all lists, map lambda to normalise strings, convert to set to eliminate duplicates, and return as list:
            all_names = list(set((map(lambda n: n.lower().strip(), danish_male_names + danish_female_names + global_names))))
            #print("Checking", len(words), "words for matches among", len(all_names), "names..")
            return ", ".join([t for t in tokens for n in all_names if t.lower() == n])

if __name__ == '__main__':
    print(extract_names("Hej Jeg hedder Johan. Hedder du Hieu eller Lisa?"))
    #print(extract_names(['Johan', 'Kasper', 'Tina', 'Muhammad', 'AUGUST', 'Hieu', 'Road', 'Kickstarter', 'Lisa', 'Ben', 'Smed', 'René', 'Jeg', 'Johan-Emil', 'Søren', 'Flystyrt']))
