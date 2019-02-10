# Movie comments dataset

네이버 영화에서 수집한 `영화 평`, `영화 평점` 데이터로, 크기에 따라 두 개의 파일로 구성되어 있습니다.

```
data/data_small.txt 
data/data_large.txt 
```

두 데이터는 아래와 같이 세 개의 columns 이 tap separated 형식으로 저장되어 있으며, headless 입니다. Column 은 <영화 아이디, 영화 평, 영화 평점> 입니다.

```
45290   크리스토퍼 놀란 에게 우리는 놀란 다     10
45290   인셉션 정말 흥미진진하게 봤었고 크리스토퍼 놀란 감독님 신작 인터스텔라도 이번주 일요일에 보러갑니다 완전 기대중 10
45290   놀란이면 무조건 봐야 된다 왜냐하면 모든 작품을 다 히트 쳤으니깐 10
45290   나는 감탄할 준비가 되어있다     10
...
```

## Set system path

이 데이터셋은 `lovit_textmining_dataset` 의 하위 패키지입니다. 아래처럼 이용할 수 있습니다.

```python
from lovit_textmining_dataset.navermovie_comments import load_movie_comments

idxs, texts, rates = load_movie_comments()
```

이 패키지만 이용할 경우에는 아래와 같이 sys.path 에 `navermovie_comments` 의 주소를 입력합니다. 이때는 fetch 를 이용할 수 없습니다.

```python
import sys

navermovie_comments_path = '/abc/def/lovit_textmining_dataset/'
sys.path.append(navermovie_comments_path)
```

아래처럼 `navermovie_comments` 에서 import 를 할 수 있습니다.

```python
from navermovie_comments import load_movie_comments

idxs, texts, rates = load_movie_comments()
```

## Functions

navermovie_comments 에서는 세 가지 종류의 함수를 제공합니다.

### load movie comments data

데이터를 손쉽게 사용하기 위하여 다음의 함수들을 제공합니다. arguments 인 large, tokenize 를 설정할 수 있습니다. Returns 은 세 개의 tuples 입니다. 세 tuples 는 <영화 아이디, 영화 평, 영화 평점> 입니다.

| Argument | Default | Description |
| --- | --- | --- |
| large | False | True 이면 data_large 를 이용합니다. <br>False 이면 data_small 을 이용합니다. |
| tokenize | None | 설정을 하지 않으면 토크나이징이 되지 않은 데이터를 읽습니다. <br>`komoran`, `soynlp_unsup` 를 설정할 수 있습니다. |
| num_doc | -1 | 로딩하는 문서의 최대 개수로, 지정하지 않으면 모든 데이터를 가져옵니다.<br>값을 지정할 경우, 파일의 앞에서부터 num_doc 줄의 정보를 return 합니다|
| idxs | None | str 형식으로 한 영화의 id 나 set of str 형식으로 여러 영화의 id 를 입력합니다.<br>해당 영화들의 정보만을 return 합니다. 기본값은 모든 영화 입니다|

```python
from navermovie_comments import load_movie_comments

idxs, texts, rates = load_movie_comments()
idxs, texts, rates = load_movie_comments(large=False, tokenize='komoran')
idxs, texts, rates = load_movie_comments(large=False, tokenize='soynlp_unsup')
```

영화 `라라랜드`의 아이디는 `134963` 입니다. 이를 입력하면 영화 라라랜드의 정보들을 가져올 수 있습니다.

```python
idxs, texts, rates = load_movie_comments(idxs='134963')
len(texts) # 15599
```

### load movie id dictionary

영화 아이디를 key 로, 영화 이름을 value 로 지니는 Python dict 를 불러올 수 있습니다.

Usage examples

```python
from navermovie_comments import load_id_to_movie

id_to_movie = load_id_to_movie()
```

### load tokenized bag of words model for classification

Sentiment classification 용 데이터를 로딩할 수 있습니다.

```python
x, y, idx_to_vocab = load_sentiment_dataset(model_name='10k', tokenize='komoran')
```

### Facebook Research FastText

Facebook Research 에서 제공하는 FastText 는 unsupervised 와 supervised embedding 방법을 모두 제공합니다. 이들은 text file path 를 input 으로 받습니다. 이 알고리즘의 실습을 위하여 만든 영화 리뷰 데이터의 path 를 가져올 수 있습니다. 이 데이터는 한글의 초/중/종성이 분리되어 있으며, 종성이 빈칸일 경우 (받침이 없을 경우)에는 '-' 처리가 되어 있습니다.

| Argument | Type | Default | Help |
| --- | --- | --- | --- |
| large | Boolean | False | True 이면 data_large 를 이용합니다 |
| supervise | Boolean | False | True 이면 supervised FastText 용 데이터 path 를 return 합니다.</br>띄어쓰기 기준 맨 앞 단어에 `__label__pos` 나 `__label__neg` 처럼 sentiment label 이 추가되어 있습니다.<br>False 이면 unsupervised (subword) FastText 용 데이터 path 가 return 됩니다.</br>이 데이터는 초/중/종성이 분리된 한글로만 이뤄져 있습니다.|

```python
from navermovie_comments import get_facebook_fasttext_data

path = get_facebook_fasttext_data(large=False, supervise=False)
path = get_facebook_fasttext_data(large=False, supervise=True)
```
