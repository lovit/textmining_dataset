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

## Loader

데이터를 손쉽게 사용하기 위하여 다음의 함수들을 제공합니다. arguments 인 large, tokenize 를 설정할 수 있습니다. Returns 은 세 개의 tuples 입니다. 세 tuples 는 <영화 아이디, 영화 평, 영화 평점> 입니다.

| Argument | Default | Description |
| --- | --- | --- |
| large | False | True 이면 data_large 를 이용합니다. False 이면 data_small 을 이용합니다. |
| tokenize | None | 설정을 하지 않으면 토크나이징이 되지 않은 데이터를 읽습니다. `komoran`, `soynlp` 를 설정할 수 있습니다. |

Usage examples,

```python
from movie_comments import load_movie_comments

idxs, texts, rates = load_movie_comments()
idxs, texts, rates = load_movie_comments(large=False, tokenize='komoran')
```

영화 아이디를 key 로, 영화 이름을 value 로 지니는 Python dict 를 불러올 수 있습니다.

Usage examples

```python
from movie_comments import load_id_to_movie

id_to_movie = load_id_to_movie()
```

Sentiment classification 용 데이터를 로딩할 수 있습니다.

```python
x, y, idx_to_vocab = load_sentiment_dataset(large=False, tokenize='komoran')
```