from .utils import check_setup
from .utils import installpath
from .utils import text_dir, index_dir, num_categories


text_path_base = '%s/{}.txt' % text_dir
date_path_base = '%s/{}.date' % index_dir
tags_path_base = '%s/{}.tags' % index_dir
title_path_base = '%s/{}.title' % index_dir

def load_category_index():
    """
    Returns
    -------
    list of str
        Each str corresponds a query that used to scrap blog posts

    Usage
    -----
        >>> from carblog_dataset import load_category_index
        >>> load_category_index()
    """

    path = '{}/../car_index'.format(installpath)
    with open(path, encoding='utf-8') as f:
        index = [doc.strip() for doc in f]
    return index

def load_file(path):
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip() for doc in f]
    return docs

def load_text(category):
    """
    Arguments
    ---------
    category : int
        Category index. Integer value between 0 and 26.

    Returns
    -------
    texts : list of str
        Each str is corresponding a blog post.
        No sentence seperator.

    Usage
    -----
        >>> from carblog_dataset import load_text

        >>> category = 10
        >>> texts = load_text(category)
    """

    check_setup()
    check_category(category)
    path = text_path_base.format(category)
    return load_file(path)

def load_index(category, date=False, tags=True, title=False):
    """
    Arguments
    ---------
    category : int
        Category index. Integer value between 0 and 26.
    date : Boolean
        If True, date information is included in return list.
        Default is False.
    tags : Boolean
        If True, tags information is included in return list.
        The value can be empty tuple of str
        Default is True.
    title : Boolean
        If True, title information is included in return list.
        The value can be empty str
        Default is False.

    Returns
    -------
    index : list of tuple
        Each tuple is corresponding a blog post
        Column of tuple is (date, tags ,title).

    Usage
    -----
        >>> from carblog_dataset import load_index

        >>> category = 10
        >>> load_index(category)[5:10]

        $ [(('만화·애니',),),
           (('굴비카드', '국민카드', '굴비엮기', '굴비신공', '굴비카드란', '굴비카드정의'),),
           (('',),),
           (('다이어리', '포토다이어리', '스냅스'),),
           (('메인보드', 'ECS', 'A55', 'MICROATX', '마이크로ATX', 'A55F-M2', 'IT·컴퓨터'),)]

        >>> load_index(category, date=True, tags=True, title=True)
    """
    check_setup()
    check_category(category)

    num_columns = date + tags + title
    if num_columns == 0:
        raise ValueError('Set column arguments as True at least one [date, tags, title]')

    loaded = []
    if date:
        path = date_path_base.format(category)
        loaded.append(load_file(path))
    if tags:
        path = tags_path_base.format(category)
        loaded_tags = load_file(path)
        loaded_tags = [tuple(t.split('\t')) for t in loaded_tags]
        loaded.append(loaded_tags)
    if title:
        path = title_path_base.format(category)
        loaded.append(load_file(path))
    grouped = [element for element in zip(*loaded)]
    return grouped

def check_category(category):
    if isinstance(category, str):
        category = int(category)
    if not (category == 10 or category == 21):
        raise ValueError("""Available only 10 or 21.
You can use dataset of full-category version with carblog-dataset
https://github.com/lovit/carblog_dataset""")
    #if not (0 <= category < num_categories):
    #    raise ValueError('Category id should be integer 0 ~ 26. However the inserted value is {}'.format(category))
    return True
