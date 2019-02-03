import pickle
import os
from glob import glob

installpath = os.path.dirname(os.path.realpath(__file__))

def get_news_paths(tokenize=None, date=None):
    """
    Arguments
    ---------
    tokenize : None or str
        Tokenizer name
    date : str
        yyyy-mm-dd form

    Returns
    -------
    If date is None, it returns list of str
        List of absolute paths
    If date is specified, it returns str

    Usage
    -----

        paths = get_news_paths() # list of str type
        paths = get_news_paths(tokenize='komoran') # list of str type
        path = get_news_paths(date='2016-10-20', tokenize='komoran') # str type
    """

    if tokenize == 'komoran':
        suffix = '_komoran.txt'
    else:
        tokenize = None
        suffix = '.txt'

    if isinstance(date, str):
        path = '{}/data/news/{}{}'.format(installpath, date, suffix)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('News of tokenize={}, date={} does not exist'.format(tokenize, date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/data/news/*{}'.format(installpath, suffix)))
    if tokenize is None:
        paths = [p for p in paths if p.split('/')[-1][10] != '_']
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_news_index_paths(date=None):
    """
    Arguments
    ---------
    date : str
        yyyy-mm-dd form

    Returns
    -------
    If date is None, it returns list of str
        List of absolute paths
    If date is specified, it returns str

    Usage
    -----

        paths = get_news_index_paths() # list of str type
        path = get_news_index_paths(date='2016-10-20') # str type
    """

    if isinstance(date, str):
        path = '{}/data/news/{}.index'.format(installpath, date)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Index on {} does not exist'.format(date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/data/news/*.index'.format(installpath)))
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_comments_paths(tokenize=None, date=None):
    """
    Arguments
    ---------
    tokenize : None or str
        Tokenizer name
    date : str
        yyyy-mm-dd form

    Returns
    -------
    If date is None, it returns list of str
        List of absolute paths
    If date is specified, it returns str

    Usage
    -----

        paths = get_comments_paths() # list of str type
        paths = get_comments_paths(tokenize='komoran') # list of str type
        path = get_comments_paths(date='2016-10-20', tokenize='komoran') # str type
    """

    if tokenize == 'komoran':
        suffix = '_komoran.txt'
    else:
        tokenize = None
        suffix = '.txt'

    if isinstance(date, str):
        path = '{}/data/comments/{}{}'.format(installpath, date, suffix)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Comments of tokenize={}, date={} does not exist'.format(tokenize, date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/data/comments/*{}'.format(installpath, suffix)))
    if tokenize is None:
        paths = [p for p in paths if p.split('/')[-1][10] != '_']
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_comments_index_paths(date=None):
    """
    Arguments
    ---------
    date : str
        yyyy-mm-dd form

    Returns
    -------
    If date is None, it returns list of str
        List of absolute paths
    If date is specified, it returns str

    Usage
    -----

        paths = get_comments_index_paths() # list of str type
        path = get_comments_index_paths(date='2016-10-20') # str type
    """

    if isinstance(date, str):
        path = '{}/data/comments/{}.index'.format(installpath, date)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Index on {} does not exist'.format(date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/data/comments/*.index'.format(installpath)))
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_bow(date='2016-10-20', tokenize='noun'):
    """
    Arguments
    ---------
    date : str
        yyyy-mm-dd form
    tokenize : str
        Tokenizer name that used to create Bag of words model

    Returns
    -------
    x : scipy.sparse.csr_matrix
        Bag of Words Model with shape = (n_docs, n_terms)
    idx_to_vocab : list of str
        Vocabulary list with len(idx_to_vocab) == n_terms
    vocab_to_idx : {str:int}
        Vocabulary to index dictionary with len(vocab_to_idx) == n_terms

    Usage
    -----

        x, idx_to_vocab, vocab_to_idx = get_bow()
        # or
        x, idx_to_vocab, vocab_to_idx = get_bow(date='2016-10-20', tokenize='noun')
    """

    path = '{}/models/{}_bow_{}.pkl'.format(installpath, date, tokenize)
    with open(path, 'rb') as f:
        params = pickle.load(f)
        x = params['x']
        idx_to_vocab = params['idx_to_vocab']
        vocab_to_idx = params['vocab_to_idx']
    return x, idx_to_vocab, vocab_to_idx
