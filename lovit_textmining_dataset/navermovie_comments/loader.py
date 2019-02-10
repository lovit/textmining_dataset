import os
import numpy as np
import pickle

installpath = os.path.dirname(os.path.realpath(__file__))

def get_movie_comments_path(large=False, tokenize=None, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenzie : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'soynlp_unsup', 'fasttext']

    Returns
    -------
    path : str
        File path
    """

    # set default directory
    if directory is None:
        directory = '{}/data/'.format(installpath)

    # set data size
    size = 'large' if large else 'small'

    # set tokenizer type
    if tokenize is 'komoran':
        tokenization = '_komoran'
    elif tokenize is 'soynlp_unsup':
        tokenization = '_soynlp_unsup'
    elif tokenize is 'fasttext':
        tokenization = '_fasttext'
    else:
        tokenization = ''

    # set data path
    path = '{}/data_{}{}.txt'.format(directory, size, tokenization)
    return path

def get_facebook_fasttext_data(large=False, supervise=False, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True, it returns data_large.
        Else, it returns data_small.
        Default is False
    supervise : Boolean
        If True, it returns path of data for supervised FastText
        Else, it returns path of data for unsupervised (subword) FastText

    Returns
    -------
    path : str
        File path
    """

    # set default directory
    if directory is None:
        directory = '{}/data/'.format(installpath)

    # set data size
    size = 'large' if large else 'small'

    # suffix
    suffix = 'classification' if supervise else 'subword'

    # set data path
    path = '{}/data_{}_fasttext_facebook_{}.txt'.format(directory, size, suffix)
    return path

def load_movie_comments(large=False, tokenize=None, num_doc=-1, idxs=None, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenzie : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'soynlp_unsup', 'fasttext']
    num_doc : int
        The number of sampled data.
        Default is -1 (all data)
    idxs : set of str
        Specific movie id set
        Defaulf is None, load data of all movies

    Returns
    -------    
    idxs : list of str
        영화 아이디 리스트
    texts : list of str
        영화 평 리스트
    rates : list of int
        영화 평점 리스트

    Usage
    -----

        idxs, texts, rates = load_movie_comments(large=False, tokenize=None)
        idxs, texts, rates = load_movie_comments(large=False, tokenize='komoran')
        idxs, texts, rates = load_movie_comments(large=False, tokenize='soynlp_unsup')

        # getting raw text of La La Land
        idxs, texts, rates = load_movie_comments(idxs='134963')

        # getting text of La La Land that tokenized with Komoran
        idxs, texts, rates = load_movie_comments(tokenize='soynlp_unsup', idxs='134963')
    """

    # get path
    path = get_movie_comments_path(large, tokenize, directory)

    # load data
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip().split('\t') for doc in f]

    # check format
    docs = [doc for doc in docs if len(doc) == 3]

    # check idx
    if idxs is not None:
        if isinstance(idxs, str):
            idxs = {idxs}
        docs = [doc for doc in docs if doc[0] in idxs]

    # select
    if num_doc > 0:
        docs = docs[:num_doc]

    # re-formatting
    idxs, texts, rates = zip(*docs)
    rates = [int(r) for r in rates]

    return idxs, texts, rates

def load_id_to_movie(directory=None):
    """
    Returns
    -------
    id_to_movie : dict
        {str : str} format

        Snapshot
        {
            '67240': '슈퍼 마우스',
            '113736': '사두',
            ...
        }

    Usage
    -----

        id_to_movie = load_id_to_movie()
    """

    if directory is None:
        directory = '{}/data/'.format(installpath)
    path = '{}/id_to_movie.pkl'.format(directory)
    with open(path, 'rb') as f:
        id_to_movie =  pickle.load(f)
    return id_to_movie

def load_sentiment_dataset(data_name='small', tokenize='komoran', directory=None):
    """
    Arguments
    ---------
    data_name : str
        Tokenized data name. Choose ['small', '10k']
        Default is small
    tokenzie : str
        Choose ['komoran', 'soynlp_unsup']
        Default is 'komoran'

    Returns
    -------
    texts : list of list of str
        Tokenized texts
    x : scipy.sparse.csr_matrix
        Term frequency matrix with shape (n_docs, n_terms)
    y : numpy.ndarray
        Sentiment label with shape (n_docs,)
        1 is positive, -1 is negative
    idx_to_vocab : list of str
        Term list

    Usage
    -----

        texts, x, y, idx_to_vocab = load_sentiment_dataset(data_name='10k', tokenize='komoran')
        texts, x, y, idx_to_vocab = load_sentiment_dataset(data_name='small', tokenize='komoran')
    """

    # set default directory
    if directory is None:
        directory = '{}/models/'.format(installpath)

    # set tokenizer type
    if tokenize is 'komoran':
        tokenization = '_komoran'
    elif tokenize is 'soynlp_unsup':
        tokenization = '_soynlp_unsup'
    elif tokenize is 'fasttext':
        tokenization = '_fasttext'
    else:
        raise ValueError('Set tokenize as komoran or soynlp')

    texts_path = '{}/sentiment_{}{}_texts.txt'.format(directory, data_name, tokenization)
    x_path = '{}/sentiment_{}{}_x.pkl'.format(directory, data_name, tokenization)
    y_path = '{}/sentiment_{}{}_y.pkl'.format(directory, data_name, tokenization)
    vocab_path = '{}/sentiment_{}{}_vocab.txt'.format(directory, data_name, tokenization)

    with open(texts_path, encoding='utf-8') as f:
        texts = [text.split() for text in f]
    with open(x_path, 'rb') as f:
        x = pickle.load(f)
    with open(y_path, 'rb') as f:
        y = pickle.load(f)
    if isinstance(y, list):
        y = np.asarray(y, dtype=np.int)
    with open(vocab_path, encoding='utf-8') as f:
        idx_to_vocab = [vocab.strip() for vocab in f]

    return texts, x, y, idx_to_vocab

def load_trained_embedding(data_name='large', tokenize='soynlp_unsup',
    embedding='word2vec', directory=None):
    """
    Arguments
    ---------
    data_name : str
        Tokenized data name. Choose ['small', 'large']
        Default is large
    tokenzie : str
        Choose ['komoran', 'soynlp_unsup']
        Default is 'soynlp_unsup'
    embedding : str
        Choose ['word2vec', 'doc2vec', 'fasttext']
        Default is 'word2vec'

    Returns
    -------
    trained_model

    Usage
    -----

        word2vec_model = load_sentiment_dataset(data_name='large',
            tokenize='soynlp_unsup', embedding='word2vec')
    """

    # set default directory
    if directory is None:
        directory = '{}/models/'.format(installpath)

    # set tokenizer type
    if tokenize is 'komoran':
        tokenization = 'komoran'
    elif tokenize is 'soynlp_unsup':
        tokenization = 'soynlp_unsup'
    elif tokenize is 'fasttext':
        tokenization = 'fasttext'
    else:
        raise ValueError('Set tokenize as komoran or soynlp')

    path = '{}/models/{}_{}_{}_gensim3-6.pkl'.format(installpath, embedding, data_name, tokenization)
    if not os.path.exists(path):
        raise ValueError('Not yet trained {}'.format(path))

    with open(path, 'rb') as f:
        return pickle.load(f)
