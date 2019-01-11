import os
import pickle

installpath = os.path.sep.join(
    os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

def load_lalaland_movie_comments_texts(tokenize=None, directory=None):
    """
    Arguments
    ---------
    tokenzie : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'soynlp']

    Returns
    -------    
    texts : list of str
        라라랜드 영화 평 리스트

    Usage
    -----
    texts = load_lalaland_movie_comments_texts(tokenize='komoran')
    """

    idxs, texts, rates = load_movie_comments(tokenize=tokenize, directory=directory)
    texts_ = []
    for idx, text, rate in zip(idxs, texts, rates):
        if idx == '134963' and text.strip():
            texts_.append(text.strip())
    return texts_

def load_movie_comments(large=False, tokenize=None, num_doc=-1, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenzie : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'soynlp']
    num_doc : int
        The number of sampled data.
        Default is -1 (all data)

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
    """

    # set default directory
    if directory is None:
        directory = '{}/movie_comments/data/'.format(installpath)

    # set data size
    size = 'large' if large else 'small'

    # set tokenizer type
    if tokenize is 'komoran':
        tokenization = '_komoran'
    elif tokenize is 'soynlp':
        tokenization = '_soynlp'
    else:
        tokenization = ''

    # set data path
    path = '{}/data_{}{}.txt'.format(directory, size, tokenization)

    # load data
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip().split('\t') for doc in f]

    # check format
    docs = [doc for doc in docs if len(doc) == 3]

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
        directory = '{}/movie_comments/data/'.format(installpath)
    path = '{}/id_to_movie.pkl'.format(directory)
    with open(path, 'rb') as f:
        id_to_movie =  pickle.load(f)
    return id_to_movie

def load_sentiment_dataset(large=False, tokenize='komoran', directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenzie : str
        Choose ['komoran', 'soynlp']
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
    """

    # set default directory
    if directory is None:
        directory = '{}/movie_comments/models/'.format(installpath)

    # set data size
    size = 'large' if large else 'small'

    # set tokenizer type
    if tokenize is 'komoran':
        tokenization = '_komoran'
    elif tokenize is 'soynlp':
        tokenization = '_soynlp'
    else:
        raise ValueError('Set tokenize as komoran or soynlp')

    texts_path = '{}/sentiment_{}{}_texts.txt'.format(directory, size, tokenization)
    x_path = '{}/sentiment_{}{}_x.pkl'.format(directory, size, tokenization)
    y_path = '{}/sentiment_{}{}_y.pkl'.format(directory, size, tokenization)
    vocab_path = '{}/sentiment_{}{}_vocab.txt'.format(directory, size, tokenization)

    with open(texts_path, encoding='utf-8') as f:
        texts = [text.split() for text in f]
    with open(x_path, 'rb') as f:
        x = pickle.load(f)
    with open(y_path, 'rb') as f:
        y = pickle.load(f)
    with open(vocab_path, encoding='utf-8') as f:
        idx_to_vocab = [vocab.strip() for vocab in f]

    return texts, x, y, idx_to_vocab