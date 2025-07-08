from .clean_html import clean_html
from .tokenize import tokenize
from .remove_stopwords import remove_stopwords_and_punctuation
from .lemmatize import lemmatize_tokens


def process_text(text: str) -> str:
    """
    Applies a fast pre-processing pipeline to the input text.

    1. Removes HTML tags.
    2. Tokenizes the text.
    3. Removes stopwords and punctuation.
    4. Lemmatizes the tokens.

    Returns a string ready for TF-IDF vectorization.
    """
    # 1. Clean HTML
    cleaned = clean_html(text)

    # 2. Tokenization
    tokens = tokenize(cleaned)

    # 3. Stopwords and punctuation
    filtered_tokens = remove_stopwords_and_punctuation(tokens)

    # 4. Lemmatization
    lemmatized = lemmatize_tokens(filtered_tokens)

    return lemmatized 