import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

# Function to map NLTK's POS (Part-of-Speech) tags to WordNet's tags
def get_wordnet_pos(word):
    """Maps POS tags to the format expected by lemmatize()"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,    # Adjective
        'N': wordnet.NOUN,   # Noun
        'V': wordnet.VERB,   # Verb
        'R': wordnet.ADV     # Adverb
    }
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_tokens(tokens):
    """Lemmatizes a list of tokens."""
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return ' '.join(lemmatized_tokens)