import os
import requests
import zipfile

installpath = os.path.dirname(os.path.realpath(__file__))
version_url = 'https://raw.githubusercontent.com/lovit/textmining_dataset/master/lovit_textmining_dataset/versions'
fetchurls_url = 'https://raw.githubusercontent.com/lovit/textmining_dataset/master/lovit_textmining_dataset/fetch_urls'
wget_headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

def fetch(dataset=None, content=None):
    # version check
    fetch_list = version_check(True)

    # do nothing if all data, contents are latest version
    if not fetch_list:
        return

    # filtering fetch list
    if dataset is not None:
        fetch_list = [name for name in fetch_list if name.split('.')[0] == dataset]
        if content is not None:
            fetch_list = [name for name in fetch_list if name.split('.')[1] == content]

    # Impossible (dataset=None, content='data')
    elif content is not None:
        raise ValueError('Content must be speficied with dataset')

    fetch_urls = download_fetch_urls()
    for name in fetch_list:
        url = fetch_urls.get(name, None)
        if url is None:
            raise ValueError('URL of {} is not specified'.format(name))
        dataset, content = name.split('.')
        fetch_from_a_url(dataset, content, url)

def fetch_from_a_url(dataset, content, url):
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

    download_fname = url.split('?')[0].split('/')[-1]
    download_path = os.path.abspath('{}/{}'.format(installpath, download_fname))
    if download_a_file(url, download_path):
        print('Successed to download {}.{}'.format(dataset, download_fname))
    else:
        raise IOError('Failed to download {} '.format(dataset, download_fname))

    unzip_path = os.path.abspath('{}/{}/{}'.format(installpath, dataset, content))
    if unzip(download_path, unzip_path):
        print('Successed to unzip {}.{}'.format(dataset, content))
    else:
        raise IOError('Failed to unzip {}.{}'.format(dataset, content))

    os.remove(download_path)

def version_check(return_fetch_list=False):
    # load local versions
    with open('{}/versions'.format(installpath), encoding='utf-8') as f:
        local_versions = dict(doc.strip().split(' = ') for doc in f)

    # download repository version
    repo_versions = download_versions()

    # version check
    fetch_list = []
    for name, repo_ver in repo_versions.items():

        # prepare variables
        local_ver = local_versions.get(name, '')
        dirname = '{}/{}'.format(installpath, name.replace('.', os.sep))

        if not (name in local_versions) or not os.path.exists(dirname):
            print('[{}] newly uploaded. need to download'.format(name))
            fetch_list.append(name)
        elif local_ver < repo_ver:
            print('[{}] need to be upgrade ({} -> {})'.format(name, local_ver, repo_ver))
            fetch_list.append(name)
        else:
            print('[{}] is latest version ({})'.format(name, local_ver))

    if return_fetch_list:
        return fetch_list

def download_versions():
    docs = download_as_str(version_url)
    versions = dict(sent.split(' = ') for sent in docs.split('\n') if sent)
    return versions

def download_fetch_urls():
    docs = download_as_str(fetchurls_url)
    urls = dict(doc.strip().split() for doc in docs.split('\n') if doc.strip())
    return urls

def download_as_str(url):
    try:
        r = requests.get(url, stream=True, headers=wget_headers)
        docs = ''.join([chunk.decode('utf-8') for chunk in r.iter_content(chunk_size=1024)])
        return docs
    except Exception as e:
        print(e)
        raise ValueError('Failed to download version file')

def download_a_file(url, fname):
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