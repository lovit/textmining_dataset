import cgi
import os
import requests
import zipfile

dataset = 'movie_comments'

installpath = os.path.sep.join(
    os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

def download(url, fname):
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
    if url.split('/')[-1].split('?')[0] != name:
        raise ValueError('Check url %s' % url)
    return True

def fetch_all(data_url, model_url):
    fetch_data(data_url)
    fetch_model(model_url)

def fetch_data(shared_url):
    _fetch(shared_url, 'data.zip', 'data/')

def fetch_model(shared_url):
    _fetch(shared_url, 'models.zip', 'models/')

def _fetch(shared_url, download_fname, directory):
    check_url(shared_url, download_fname)

    download_path = os.path.abspath('{}/movie_comments/{}'.format(installpath, download_fname))
    if download(shared_url, download_path):
        print('Success to download {} {}'.format(dataset, download_fname))
    else:
        raise IOError('Failed to download {} '.format(dataset, download_fname))

    unzip_path = os.path.abspath('{}/movie_comments/{}'.format(installpath, directory))
    if unzip(download_path, unzip_path):
        print('Success to unzip {} {}'.format(dataset, download_fname))
    else:
        raise IOError('Failed to unzip {} {}'.format(dataset, download_fname))

    os.remove(download_fname)
