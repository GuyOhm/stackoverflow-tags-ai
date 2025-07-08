from .clean_html import clean_html
from .tokenize import tokenize
from .remove_stopwords import remove_stopwords_and_punctuation
from .lemmatize import lemmatize


def process_text(text: str) -> str:
    """Pipeline rapide de pré-traitement.

    1. Supprime le HTML.
    2. Tokenise.
    3. Retire stopwords + ponctuation.
    4. Lemmatisation.

    Renvoie une chaîne prête pour vectorisation TF-IDF.
    """
    # 1. Nettoyage HTML
    cleaned = clean_html(text)

    # 2. Tokenisation
    tokens = tokenize(cleaned)

    # 3. Stopwords + ponctuation
    filtered_tokens = remove_stopwords_and_punctuation(tokens)

    # 4. Lemmatisation
    lemmatized = lemmatize(filtered_tokens)

    return lemmatized 