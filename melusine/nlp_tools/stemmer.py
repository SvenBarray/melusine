from nltk.stem import SnowballStemmer


def stemming_tokens(row, language: str = 'french'): 
    """Compute list Series which return the stemmed version of a list of tokens
    Stemming is the process of reducing a word to its word stem that affixes to suffixes and prefixes or to the roots of words.

    To be used with methods such as: `apply(func, axis=1)`

    Parameters
    ----------
    row : row of pd.Dataframe, columns ['tokens']
    language : str,
        Language of the tokens to be stemmed.
        Supported languages : 'arabic', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish' 
        Default value, 'french'

    Returns
    -------
    pd.Series

    Examples
    --------
        >>> # where data is a dataframe that contains a 'tokens' column

        >>> from melusine.prepare_email.cleaning import stemming_tokens
        >>> stemming_tokens(data.iloc[0])  # apply for 1 sample
        >>> data.apply(stemming_tokens, axis=1)  # apply to all samples

    """
    token_list = row.tokens
    stemmer = SnowballStemmer(language)
    stemmed_tokens = [stemmer.stem(word) for word in token_list]
    return stemmed_tokens