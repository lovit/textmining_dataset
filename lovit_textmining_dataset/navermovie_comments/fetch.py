import cgi
import os
import requests
import zipfile

dataset = 'movie_comments'

installpath = os.path.sep.join(
    os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

def download(url, fname):
    """
    Arguments
    --------
    url : str
        URL address of file to be downloaded
    fname : str
        Download file address

    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # If you do not set user-agent, downloading from url is stalled.
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
    try:
        r = requests.get(url, stream=True, headers=headers)
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(e)
        return False

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

def check_url(url, name):
    """
    url : str
        URL address
    name : str
        str that the url must have.

    Returns
    -------
    flag : Boolean
        Whether url contain name as last element

        for example,
            url = 'https://github.com/lovit/files.zip?s=0'
            name = 'files.zip'
        It returns True
    """

    if url.split('/')[-1].split('?')[0] != name:
        raise ValueError('Check url %s' % url)
    return True

def fetch_all(data_url, model_url):
    """
    Arguments
    ---------
    data_url : str
        URL address of data.zip
    model_url : str
        URL address of models.zip
    """

    fetch_data(data_url)
    fetch_model(model_url)

def fetch_data(data_url):
    """
    Arguments
    ---------
    data_url : str
        URL address of data.zip
    """
    _fetch(data_url, 'data.zip', 'data/')

def fetch_model(model_url):
    """
    Arguments
    ---------
    model_url : str
        URL address of data.zip
    """
    _fetch(model_url, 'models.zip', 'models/')

def _fetch(url, download_fname, directory):
    """
    Arguments
    ---------
    url : str
        URL of file to be downloaded
    download_fname : str
        Path of local download file
    directory : str
        Directory path for unzip
    """

    check_url(url, download_fname)

    download_path = os.path.abspath('{}/movie_comments/{}'.format(installpath, download_fname))
    if download(url, download_path):
        print('Success to download {} {}'.format(dataset, download_fname))
    else:
        raise IOError('Failed to download {} '.format(dataset, download_fname))

    unzip_path = os.path.abspath('{}/movie_comments/{}'.format(installpath, directory))
    if unzip(download_path, unzip_path):
        print('Success to unzip {} {}'.format(dataset, download_fname))
    else:
        raise IOError('Failed to unzip {} {}'.format(dataset, download_fname))

    os.remove(download_path)
