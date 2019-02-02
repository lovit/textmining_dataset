import os
import requests
import zipfile

installpath = os.path.dirname(os.path.realpath(__file__))
version_url = 'https://raw.githubusercontent.com/lovit/textmining_dataset/master/lovit_textmining_dataset/versions'
wget_headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

def version_check():
    with open('{}/versions'.format(installpath), encoding='utf-8') as f:
        local_versions = dict(doc.strip().split(' = ') for doc in f)
    repo_versions = download_versions()
    for name, repo_ver in repo_versions.items():
        local_ver = local_versions.get(name, '')
        dirname = '{}/{}'.format(installpath, name.replace('.', os.sep))
        if not (name in local_versions) or not os.path.exists(dirname):
            print('[{}] newly uploaded. need to download'.format(name))
        elif local_ver < repo_ver:
            print('[{}] need to be upgrade {} -> {}'.format(name, local_ver, repo_ver))
        else:
            print('[{}] is latest version {}'.format(name, local_ver))

def download_versions():
    try:
        r = requests.get(version_url, stream=True, headers=wget_headers)
        docs = ''.join([chunk.decode('utf-8') for chunk in r.iter_content(chunk_size=1024)])
        versions = dict(sent.split(' = ') for sent in docs.split('\n') if sent)
        return versions
    except Exception as e:
        print(e)
        return False

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