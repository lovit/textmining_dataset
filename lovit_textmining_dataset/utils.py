import os
import requests
import zipfile

installpath = os.path.dirname(os.path.realpath(__file__))
version_url = 'https://s3.ap-northeast-2.amazonaws.com/lovit-textmining-dataset/versions'
version_path = '{}/versions'.format(installpath)
fetchurls_url = 'https://raw.githubusercontent.com/lovit/textmining_dataset/master/lovit_textmining_dataset/fetch_urls'
wget_headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

def fetch(dataset=None, content=None):
    """
    Arguments
    ---------
    dataset : str or None
        Dataset name
    content : str or None
        Content of dataset name. It could be specified only when dataset is not None.

    Usage
    -----

        from lovit_textmining_dataset import fetch

        fetch()

        # or
        fetch(dataset='navernews_10days')

        # or
        fetch(dataset='navernews_10days', content='models')
    """

    def filter(compare):
        if dataset is None and content is not None:
            raise ValueError('Content must be speficied with dataset')
        if dataset is not None:
            compare = [cols for cols in compare if cols[0].split('.')[0] == dataset]
        if content is not None:
            compare = [cols for cols in compare if cols[0].split('.')[1] == content]
        return compare

    # version check
    compare = compare_versions()

    # argument check
    compare = filter(compare)

    # fetch
    urls = download_fetch_urls()
    for name, flag, local_ver, repo_ver in compare:
        print_fetch_status(name, flag, local_ver, repo_ver)
        if flag == 0:
            continue
        url = urls.get(name, None)
        if url is None:
            raise ValueError('URL of {} is not specified'.format(name))
        dataset, content = name.split('.')
        fetch_from_a_url(dataset, content, url, update_local_version=False)

    # update local version
    download_a_file(version_url, version_path)

def fetch_from_a_url(dataset, content, url, update_local_version=True):
    """
    Arguments
    ---------
    dataset : str
        Dataset name
    content : str
        Content name
    url : str
        URL of file to be downloaded
    update_local_version : Boolean
        If True, update local version. Default is True.

    Usage
    -----

        repository_url = 'https://...'
        fetch(dataset='navernews_10days', content='models', url=repository_url)
    """

    download_fname = url.split('?')[0].split('/')[-1]
    download_path = os.path.abspath('{}/{}'.format(installpath, download_fname))
    if download_a_file(url, download_path):
        print('  - successed to download {}.{}'.format(dataset, download_fname))
    else:
        raise IOError('  - failed to download {}\rurl = {}'.format(dataset, download_fname, url))

    unzip_path = os.path.abspath('{}/{}/{}'.format(installpath, dataset, content))
    if unzip(download_path, unzip_path):
        print('  - successed to unzip {}.{}'.format(dataset, content))
    else:
        raise IOError('  - failed to unzip {}.{}'.format(dataset, content))

    os.remove(download_path)

    if not update_local_version:
        return

    # update versions
    local_ver = read_local_version()
    repo_ver = download_versions()
    key = '{}.{}'.format(dataset, content)
    local_ver[key] = repo_ver[key]
    write_local_version(local_ver)

def version_check():
    """
    It shows version of dataset installed and repository-stored

    Usage
    -----

        from lovit_textmining_dataset import version_check

        version_check()
    """

    compare = compare_versions()
    for name, flag, local_ver, repo_ver in compare:
        print_fetch_status(name, flag, local_ver, repo_ver)

def print_fetch_status(name, flag, local_ver, repo_ver):
    if flag == 2:
        message = '[{}] newly uploaded. need to download'.format(name)
    elif flag == 1:
        message = '[{}] need to upgrade ({} -> {})'.format(name, local_ver, repo_ver)
    else:
        message = '[{}] is latest ({})'.format(name, local_ver)
    print(message)

def read_local_version():
    if not os.path.exists(version_path):
        return {}
    with open(version_path, encoding='utf-8') as f:
        local_versions = dict(doc.strip().split(' = ') for doc in f)
    return local_versions

def write_local_version(versions):
    with open(version_path, 'w', encoding='utf-8') as f:
        for name, ver in versions.items():
            f.write('{} = {}\n'.format(name, ver))

def compare_versions():

    # read local version
    local_versions = read_local_version()

    # download repository version
    repo_versions = download_versions()

    # 0 : latest version
    # 1 : need to be update
    # 2 : newly uploaded
    compare = []
    for name, repo_ver in repo_versions.items():

        # prepare variables
        local_ver = local_versions.get(name, '')
        dirname = '{}/{}'.format(installpath, name.replace('.', os.sep))

        if not (name in local_versions) or not os.path.exists(dirname):
            flag = 2
        elif local_ver < repo_ver:
            flag = 1
        else:
            flag = 0

        compare.append((name, flag, local_ver, repo_ver))
    return compare

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