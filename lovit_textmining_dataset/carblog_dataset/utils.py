import csv
from datetime import datetime
from glob import glob
import os
import re
import zipfile

sep = os.path.sep

installpath = os.path.dirname(os.path.realpath(__file__))
text_dir = '{0}{1}texts{1}'.format(installpath, sep)
index_dir = '{0}{1}index{1}'.format(installpath, sep)
num_categories = 27

def load_list(path, dtype=None):
    """
    This function used to create carblog data with raw scraped data.
    """
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip() for doc in f]
    return docs

def parse_date(s):
    """
    This function used to create carblog data with raw scraped data.

    Usage
    -----
        >>> parse_date('2012-01-23')       # datetime.datetime(2012, 1, 23, 0, 0)
        >>> parse_date('2012-01-23 15:23') # datetime.datetime(2012, 1, 23, 0, 0)
    """
    date_pattern = re.compile('\d{4}-\d{2}-\d{2}')
    d = date_pattern.findall(s)
    if not d:
        return None
    return datetime.strptime(d[0], '%Y-%m-%d')

def parse_tags(line):
    """
    This function used to create carblog data with raw scraped data.

    Usage
    -----
        >>> parse_tags("'자동차', '중고차', 'BMW'")   # ['자동차', '중고차', 'BMW']
        >>> parse_tags("['자동차', '중고차', 'BMW']") # ['자동차', '중고차', 'BMW']
        >>> parse_tags('[]')                        # []
        >>> parse_tags('')                          # []
    """
    def strip(s):
        return s.strip()[1:-1].strip()

    if not line:
        return []
    if line[0] == '[' and line[-1] == ']':
        line = line[1:-1]
    tags = list(csv.reader([line], delimiter=','))[0]
    tags = [strip(s) for s in tags]
    return tags

def check_setup():
    """
    Check whether zip files are decompressed or not.
    If not, it will decompress all zip files automatically.
    If data files are set, it returns True. Else it will raise runtime error.
    """
    text_files = glob('{}/*.txt'.format(text_dir))
    index_files = glob('{}/*.date'.format(index_dir))
    if not text_files or not index_files:
        message = """You should first setup dataset using carblog_dataset.setup function.
        >>> from carblog_dataset import setup
        >>> setup(remove_zip=True) # or
        >>> setup(remove_zip=False)
        """
        raise RuntimeError(message)
    return True

def setup(remove_zip=False):

    def unzips(sources, filetype):
        for source in sources:
            source = os.path.abspath(source)
            dest_dir, dest_name = source.rsplit(os.path.sep, 1)
            unzip(source, dest_dir)
            if remove_zip:
                os.remove(source)
            print('Unzip {} file {}'.format(filetype, source))

    def sort(paths):
        return sorted(paths, key=lambda x:int(x.split(sep)[-1].split('.')[0]))

    text_sources = sort(glob('{}/*.txt.zip'.format(text_dir)))
    unzips(text_sources, 'text')

    index_sources = sort(glob('{}/*.zip'.format(index_dir)))
    unzips(index_sources, 'index')

    print('done')

def unzip(source, destination):
    """
    Arguments
    ---------
    source : str
        zip file address. It doesn't matter absolute path or relative path
    destination :
        Directory path of unzip
    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    abspath = os.path.abspath(destination)
    dirname = os.path.dirname(abspath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    try:
        downloaded = zipfile.ZipFile(source)
        downloaded.extractall(destination)
        return True
    except Exception as e:
        print(e)
        return False