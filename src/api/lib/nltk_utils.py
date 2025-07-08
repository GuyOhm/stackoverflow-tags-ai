import nltk
import ssl

def download_nltk_data():
    """
    Downloads the necessary NLTK data packages.
    Handles SSL certificate verification issues.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    packages = [
        "wordnet",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
        "punkt",
        "punkt_tab",
        "stopwords",
    ]

    for package in packages:
        try:
            nltk.data.find(f"tokenizers/{package}")
        except LookupError:
            nltk.download(package) 