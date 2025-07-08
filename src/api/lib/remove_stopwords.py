import nltk
from nltk.corpus import stopwords
import string


def remove_stopwords_and_punctuation(tokens):
    """
    Removes stopwords and punctuation from a list of tokens.

    Args:
        tokens: A list of tokens.

    Returns:
        A new list of tokens with stopwords and punctuation removed.
    """
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    filtered_tokens = [
        token for token in tokens if token.lower() not in stop_words and token not in punctuation
    ]
    return filtered_tokens