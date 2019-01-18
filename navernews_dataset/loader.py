import os
from glob import glob


dataset = 'navernews_dataset'
installpath = os.path.sep.join(
    os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

def get_news_paths(tokenize=None, date=None):
    if tokenize is None:
        t = ''
    elif tokenize == 'komoran':
        t = '_komoran'

    if isinstance(date, str):
        path = '{}/{}/data/news/{}{}.txt'.format(installpath, dataset, date, t)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('News of tokenize={}, date={} does not exist'.format(tokenize, date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/{}/data/news/*{}.txt'.format(installpath, dataset, t)))
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_news_index_paths(date=None):
    if isinstance(date, str):
        path = '{}/{}/data/news/{}.index'.format(installpath, dataset, date)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Index on {} does not exist'.format(date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/{}/data/news/*.index'.format(installpath, dataset)))
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_comments_paths(tokenize=None, date=None):
    if tokenize is None:
        t = ''
    elif tokenize == 'komoran':
        t = '_komoran'

    if isinstance(date, str):
        path = '{}/{}/data/comments/{}{}.txt'.format(installpath, dataset, date, t)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Comments of tokenize={}, date={} does not exist'.format(tokenize, date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/{}/data/comments/*{}.txt'.format(installpath, dataset, t)))
    paths = [os.path.abspath(p) for p in paths]
    return paths

def get_comments_index_paths(date=None):
    if isinstance(date, str):
        path = '{}/{}/data/comments/{}.index'.format(installpath, dataset, date)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('Index on {} does not exist'.format(date))
        return os.path.abspath(path)

    paths = sorted(glob('{}/{}/data/comments/*.index'.format(installpath, dataset)))
    paths = [os.path.abspath(p) for p in paths]
    return paths