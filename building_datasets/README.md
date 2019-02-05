# Dataset building codes

Dataset 및 각 data 를 이용하여 미리 학습된 models 를 만들기 위한 코드들입니다. IPython notebook 파일들로 이뤄져 있습니다.

`soynlp` 및 `lovit_textmining_dataset` 의 위치를 sys.path 에 추가한 config.py 를 만드셔서 이용하시기 바랍니다.


```python
# config.py

soynlp_dir = 'YOURS'
dataset_dir = '../'

import sys
sys.path.append(soynlp_dir)
sys.path.append(dataset_dir)
sys.path.append(dataset_dir+'/lovit_textmining_dataset/')

import soynlp
print('soynlp == {}'.format(soynlp.__version__))

import gensim
print('gensim == {}'.format(gensim.__version__))

import konlpy
print('konlpy == {}'.format(konlpy.__version__))
```

