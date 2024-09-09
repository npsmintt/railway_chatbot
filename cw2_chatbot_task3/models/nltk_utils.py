import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence):
    # simple function to tokenize the sentence
    return nltk.word_tokenize(sentence)


def stem(word):
    # find the root form of the word
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    # this function returns an array, if the word is in the word list, it is represented by 1; if not, it is represented by 0.
    # first, stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    # and change the number  to 1 where the word is in the list
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
    return bag
