import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

# Fonction pour mapper les étiquettes POS (Part-of-Speech= étiquettage morphosyntaxique) de NLTK aux étiquettes de WordNet
def get_wordnet_pos(word):
    """Mappe les étiquettes POS aux étiquettes attendues par lemmatize()"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,    # Adjectif
        'N': wordnet.NOUN,   # Nom
        'V': wordnet.VERB,   # Verbe
        'R': wordnet.ADV     # Adverbe
    }
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize(tokens):
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return ' '.join(lemmatized_tokens)