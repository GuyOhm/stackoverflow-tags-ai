import nltk
from nltk.tokenize import word_tokenize

def tokenize(sentence) :
    word_tokens = word_tokenize(sentence)
    return word_tokens