from glob import glob
import os
import numpy as np
import pickle

installpath = os.path.dirname(os.path.realpath(__file__))
available_tokenize = {'soynlp_unsup', 'fasttext', 'komoran', 'soynlp_cohesion'}

def check_tokenize(tokenize):
    if tokenize is None:
        return ''
    if (not tokenize in available_tokenize) or not isinstance(tokenize, str):
        raise ValueError('does not provide tokenize = {}'.format(tokenize))
    return '_{}'.format(tokenize)

def get_movie_comments_path(large=False, tokenize=None, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenize : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'fasttext', 'soynlp_cohesion', 'soynlp_unsup']

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
    tokenize = check_tokenize(tokenize)

    # set data path
    path = '{}/data_{}{}.txt'.format(directory, size, tokenize)
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

def get_comments_image_path(large=False, tokenize=None, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenize : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['soynlp_unsup']

    Returns
    -------
    x_path : str
        Sentece image path
        In x_path
            0 37 25 4
            255 9693 12 633
            ...
    y_path : str
        Rate path
    vocab_path : str
        Vocabulary index path
    """

    # set default directory
    if directory is None:
        directory = '{}/data/'.format(installpath)

    # set data size
    size = 'large' if large else 'small'

    # set tokenizer type
    tokenize = check_tokenize(tokenize)

    # set data path
    x_path = '{}/comments_image{}_{}_x'.format(directory, tokenize, size)
    y_path = '{}/comments_image{}_{}_y'.format(directory, tokenize, size)
    vocab_path = '{}/comments_image{}_{}_vocab.txt'.format(directory, tokenize, size)
    return x_path, y_path, vocab_path

def load_comments_image(large=False, tokenize=None, max_len=20, n_data=-1, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenize : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['soynlp_unsup']
    max_len : int
        Maximum length of sentence.
        If sentence is longer than max_len, use first max_len terms
    n_data : int
        Number of sampled data. If it is negative, use all data.
        Default is -1

    Returns
    -------
    X : numpy.ndarray
        Sentence image. shape = (n sent, max_len) with padding
    y : numpy.ndarray
        Rate array
    idx_to_vocab : list of str
        Vocabulary index
    """

    X, y, idx_to_vocab = load_comments_image_without_padding(large, tokenize, n_data, directory)

    padding_idx = len(idx_to_vocab)
    idx_to_vocab.append('<padding>')

    # padding
    X_ = []
    for x in X:
        n_vocabs = len(x)
        if n_vocabs >= max_len:
            x = x[:max_len]
        elif n_vocabs < max_len:
            x = x + [padding_idx] * (max_len - n_vocabs)
        X_.append(np.asarray(x, dtype=np.int))
    X_ = np.asarray(np.vstack(X_), dtype=np.int)

    y = np.asarray(y, dtype=np.int)

    return X_, y, idx_to_vocab

def load_comments_image_without_padding(large=False, tokenize=None, n_data=-1, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenize : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['soynlp_unsup']

    Returns
    -------
    X : list of list of int
        Sentences that all vocabs have been encoded to idx.
    y : list of int
        Rate array
    idx_to_vocab : list of str
        Vocabulary index
    """

    x_path, y_path, vocab_path = get_comments_image_path(large, tokenize, directory)

    # load vocabulary index
    with open(vocab_path, encoding='utf-8') as f:
        idx_to_vocab = [vocab.strip() for vocab in f]

    # load sentence image
    X = []
    with open(x_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if n_data > 0 and i == n_data:
                break
            vocabs = [int(v) for v in line.split() if v]
            X.append(vocabs)

    # load rate
    with open(y_path, encoding='utf-8') as f:
        y = [int(line.strip()) for line in f]
    if n_data > 0:
        y = y[:n_data]

    return X, y, idx_to_vocab

def load_movie_comments(large=False, tokenize=None, num_doc=-1, idxs=None, directory=None):
    """
    Arguments
    ---------
    large : Booolean
        If True it returns data_large.
        Else, it returns data_small.
        Default is False
    tokenize : None or str
        If None, it returns raw (not-tokenized) texts
        Choose ['komoran', 'fasttext', 'soynlp_cohesion', 'soynlp_unsup']
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
    tokenize : str
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
    tokenize_ = check_tokenize(tokenize)

    texts_path = '{}/sentiment_{}{}_texts.txt'.format(directory, data_name, tokenize_)
    x_path = '{}/sentiment_{}{}_x.pkl'.format(directory, data_name, tokenize_)
    y_path = '{}/sentiment_{}{}_y.pkl'.format(directory, data_name, tokenize_)
    vocab_path = '{}/sentiment_{}{}_vocab.txt'.format(directory, data_name, tokenize_)

    if not os.path.exists(texts_path):
        print('Available tokenizers')
        paths = glob('{}/sentiment_{}*_x.pkl'.format(directory, dataname))
        for p in paths:
            print('  - {}'.format(p.split('/')[-1][:-6]))
        raise ValueError('Not provide sentiment dataset with tokenize = {}'.format(tokenize_))

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
    tokenize : str
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
    tokenize = check_tokenize(tokenize)
    path = '{}/models/{}_{}{}_gensim3-6.pkl'.format(installpath, embedding, data_name, tokenize)
    if not os.path.exists(path):
        raise ValueError('Not yet trained {}'.format(path))

    with open(path, 'rb') as f:
        return pickle.load(f)
