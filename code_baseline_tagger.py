import nltk
from nltk.corpus import brown
import matplotlib.pyplot as plt
import matplotlib as mpl

#nltk.download('universal_tagset')

def frequency():
    tagged_corpus = brown.tagged_words(tagset='universal')
    tag_fd = nltk.FreqDist(tag for (word, tag) in tagged_corpus)
    
    word_tag_pairs = nltk.bigrams(tagged_corpus)
    noun_preceders = [a[1] for (a, b) in word_tag_pairs if b[1] == 'NOUN']
    fdist = nltk.FreqDist(noun_preceders)
    most_common_noun_preceders = [tag for (tag, _) in fdist.most_common()]
    word_tag_fd = nltk.FreqDist(tagged_corpus)
    most_common_verbs_sorted = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'VERB']
    cfd1 = nltk.ConditionalFreqDist(tagged_corpus)
    output = cfd1['yield'].most_common()
    print(output)

def process(sentence):
    # [_three-word]
    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
        # [_verb-to-verb]
        if (t1.startswith('V') and t2 == 'TO' and t3.startswith('V')):
            print(w1, w2, w3)  # [_print-words]

if __name__ == '__main__':
    process("Can you meet me at 12:00 tomorrow?")
    print("done")