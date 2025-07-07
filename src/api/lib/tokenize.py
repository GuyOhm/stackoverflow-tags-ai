import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')

def tokenize(sentence) :
    word_tokens = word_tokenize(sentence)
    return word_tokens