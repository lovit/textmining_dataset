# 네이버 뉴스기사 및 댓글 데이터

`2016-10-20` ~ `2016-10-29` 사이의 네이버 뉴스와 댓글을 수집한 데이터입니다.

data 폴더에는 news 와 comments 가 있습니다. 각각 뉴스 기사와 댓글을 포함하고 있으며, 이들은 텍스트 파일인 \*.txt 와 각 줄에 해당하는 기사, 댓글의 아이디 등이 저장된 \*.index 로 구성되어 있습니다.

```
|-- data
    |-- news
        |-- 2016-10-20.txt
        |-- 2016-10-20.index
        |-- 2016-10-21.txt
        |-- ...
    |-- comments
        |-- 2016-10-20.txt
        |-- 2016-10-20.index
        |-- 2016-10-21.txt
        |-- ...
|-- models
    |-- 2016-10-20_bow_noun.pkl
    |-- ...
```

## 뉴스 데이터 형식

`DATE.txt` 파일에는 한 줄에 하나의 뉴스 기사가 포함되어 있으며, 하나의 뉴스 기사에서의 줄바꿈은 두 칸 띄어쓰기로 구분됩니다. 예시로 `data/news/2016-10-20.txt` 파일은 30,091 줄의 텍스트 파일입니다. 뉴스 기사가 30,091 개라는 의미이며, 어떤 줄에는 두 칸 띄어쓰기가 5 개 포함된 경우도 있습니다. 그 줄은 6 문장으로 이뤄진 뉴스기사라는 의미입니다.

이처럼 각 줄을 두 칸 띄어쓰기로 구분하는 텍스트를 손쉽게 다루기 위하여 [`soynlp`](https://github.com/lovit/soynlp/) 의 DoublespaceLineCorpus 를 이용할 수 있습니다. 이는 iteration 의 단위를 문장 혹은 문서로 할지를 iter_sent 라는 변수로 조절할 수 잇습니다.

```python
from soynlp.utils import DoublespaceLineCorpus

corpus_path = ''
corpus = DoublespaceLineCorpus(corpus_path, iter_sent=True)
corpus.iter_sent = False
```

`DATE.index` 파일에는 `DATE.txt` 의 각 줄에 해당하는 댓글의 메타 정보가 포함되어 있습니다. Tap 으로 구분되어 있는 테이블 형식이며, 각 컬럼의 예시는 다음과 같습니다.

| Column | Example | Description |
| --- | --- | --- |
| Press id | 001 | 네이버 뉴스 기준 언론사 아이디 입니다 |
| Date | 2016-10-20 | `-` 로 구분된 날짜입니다 |
| Article id | 0008765175 | 네이버 뉴스 기준 각 기사입니다 |
| category | 104 | 네이버 뉴스 기준의 뉴스 카테고리 입니다 |
| written time | 2016-10-20 00:00 | yyyy-mm-dd hh-MM 형식의 뉴스 기사 작성 시간 혹은 최종 수정 시간입니다 |

```
001    2016-10-22    0008770556    104    2016-10-22 00:00
001    2016-10-22    0008770558    104    2016-10-22 00:05
001    2016-10-22    0008770559    104    2016-10-22 00:12
```

Press id, Date, Article id 를 조합하면 기사별 unique key 를 만들 수 있습니다.

```
press_idx = '001'
date = '2016-10-20'
article_idx = '0008765175'

unique_key = '-'.join([press_idx, date, article_idx])
```

## 뉴스 댓글 데이터 형식

`DATE.txt` 파일은 한 줄에 하나의 댓글로 구성된 텍스트 파일입니다.

```
자살할놈이 뭐 방탄조끼 저거누가 좀 안죽이나
제발 처벌강화해서 조지자 제발부탁이다
...
```

`DATE.index` 파일에는 `DATE.txt` 의 각 줄에 해당하는 댓글의 메타 정보가 포함되어 있습니다. 띄어쓰기로 구분되어 있는 테이블 형식이며, 각 컬럼의 예시는 다음과 같습니다.

| Date | Press id | Article id | Comment id | Agree | Disagree |
| --- | --- | --- | --- | --- | --- |
| 2016-10-25 | 001 | 0008775566 | 716126142 | 7 | 0 |

Press id, Date, Article id 를 혼합하면 댓글의 뉴스 기사를 탐색할 수 있습니다.

```python
press_idx = '001'
date = '2016-10-25'
article_idx = '0008775566'

unique_key = '-'.join([press_idx, date, article_idx])
```

## Set system path

이 데이터셋은 `lovit_textmining_dataset` 의 하위 패키지입니다. 아래처럼 이용할 수 있습니다.

```python
from lovit_textmining_dataset.navernews_10days import get_news_paths

paths = get_news_paths()
```

이 패키지만 이용할 경우에는 아래와 같이 sys.path 에 `navernews_10days` 의 주소를 입력합니다. 이때는 fetch 를 이용할 수 없습니다.

```python
import sys

navernews_10days_path = '/abc/def/lovit_textmining_dataset/'
sys.path.append(navernews_10days_path)
```

아래처럼 `navernews_10days` 에서 import 를 할 수 있습니다.

```python
from navernews_10days import get_news_paths

paths = get_news_paths()
```

## Functions

navernews_10days 는 다음과 같은 기능을 제공합니다.

### Get data file paths

뉴스, 댓글 데이터는 `soynlp` 의 DoublespaceLineCorpus 와 함께 이용하기 위하여 각 파일의 절대 주소를 return 하는 기능을 제공합니다.

뉴스의 raw texts 를 가져오려면 argument 의 기본값으로 함수를 실행합니다. 각자의 환경에 다운로듸 된 2016-10-20 ~ 2016-10-29 간의 뉴스 기사 파일의 절대 주소가 list of str 로 return 됩니다.

```python
from lovit_textmining_dataset.navernews_10days import get_news_paths

paths = get_news_paths()
```

미리 토크나이징이 된 데이터를 불러올 수도 있습니다. 현재 tokenize 는 `komoran`, `okt` 를 이용할 수 있습니다. 그 외에는 raw texts 를 읽어들여 각자 토크나이징 하시기 바랍니다.

```python
paths = get_news_paths(tokenize='komoran')
```

특정 날짜에 토크나이저로 토크나이징이 된 텍스트를 가져오려면 `date` 와 `tokenize` 를 설정합니다. 이때는 하루의 뉴스 기사이므로 str 형식으로 하나의 파일 주소가 return 됩니다.

```python
path = get_news_paths(date='2016-10-20', tokenize='komoran')
```

뉴스 댓글의 파일 절대 주소도 동일한 방법으로 가져올 수 있습니다.

```python
from lovit_textmining_dataset.navernews_10days import get_comments_paths

paths = get_comments_paths()
```

`.index` 파일에 대한 utils 은 추가될 예정입니다.

### Load Bag-of-Words

문서 군집화나 키워드 추출과 같은 작업은 벡터라이징이 된 input 이 필요합니다. 이를 위해서 bag of words model 로 표현된 문서 집합을 제공합니다.

현재는 `2016-10-20` 뉴스 기사에 대하여 `soynlp` 의 `LRNounExtractor_v2` 를 이용하여 추출된 명사로 이뤄진 bow model 만 제공됩니다.

```python
from lovit_textmining_dataset.navernews_10days import get_bow

x, idx_to_vocab, vocab_to_idx = get_bow(date='2016-10-20', tokenize='noun')
```

Term frequency matrix `x`, list of str 형식의 `idx_to_vocab`, {str:int} 형식의 `vocab_to_idx` 이 return 됩니다.

```python
x.shape # (30091, 9774)
idx_to_vocab[5537] # 아이오아이
vocab_to_idx['아이오아이'] # 5537
```

이후 10 일간의 데이터에 다양한 종류의 토크나이저가 적용된 bow models 를 추가할 예정입니다.
