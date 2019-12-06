# 텍스트 마이닝 실습을 위한 데이터셋

텍스트 마이닝 실습에 이용되는 데이터셋을 핸들링하는 함수 집합입니다.

`lovit_textmining_dataset` 의 하위 폴더들은 각 데이터셋의 이름이며 현재 정리된 데이터셋의 이름은 아래와 같습니다. 데이터 별 특징은 각 데이터 폴더 안의 README 에 기록하였습니다.

| Dataset name | Description |
| --- | --- |
| navermovie_comments | 네이버영화에서 수집한 영화별 사용자 작성 커멘트와 평점 |
| navernews_10days | 네이버뉴스에서 수집한 2016-10-20 ~ 2016-10-29 (10일) 간의 뉴스와 댓글 |

폴더는 아래처럼 구성되어 있습니다. 데이터셋 폴더 아래의 data 는 각 데이터셋별 raw data 이며, models 는 raw data 를 이용하여 학습을 한 모델들이 저장된 폴더 입니다. 예를 들어 영화 평점 분류 문제를 위하여 텍스트들로부터 Bag-of-Words Models 를 만들고, 이를 이용하여 학습데이터 (X, Y) 를 미리 만들어 둘 수 있습니다. 이러한 모델들을  models 안에 모아뒀습니다.

각 데이터셋 안에는 데이터셋 핸들링에 관련된 Python 파일들이 포함되어 있습니다. 사용법은 각 데이터 폴더 안의 README 를 참고하세요.

```
lovit_textmining_dataset
    |-- navermovie_comments
        |-- __init__.py
        |-- loader.py
        |-- README.md
        |-- data
            |-- data_large.txt
            |-- ...
        | models
            |-- ...
    |-- navernews_10days
        |-- __init__.py
        |-- loader.py
        |-- README.md
        |-- data
            |-- 2016-10-20.txt
            |-- ...
        | models
            |-- ...
```

## Install

Github 에 데이터 파일을 저장하면 불편한 점들이 있어서 github 에서는 패키지 함수들을 제공하고, 이 함수를 이용하여 모델을 다운로드 받습니다. 즉 github 의 코드에는 위의 디렉토리 구조에서 `navermovie_comments/loader.py` 는 존재하지만, `navermovie_comments/data` 폴더는 존재하지 않습니다. 이는 `fetch` 함수를 이용하여 다운로드 합니다.

데이터 패키지는 git clone 을 이용하여 설치합니다.

```
git clone https://github.com/lovit/textmining_dataset.git
cd textmining_dataset
python setup.py install
```

설치 후 `version_check` 함수를 이용하여 현재 설치된 데이터들과 설치해야 할 데이터들을 확인합니다. local 의 버전과 data repository 의 버전을 확인합니다.

```python
from lovit_textmining_dataset import version_check

version_check()
```

README 작성 당시 두 개의 데이터셋 각각 data 와 models 를 제공하고 있습니다. 네 개의 파일 모두 설치가 되지 않았다는 메시지가 출력됩니다.

```
[navermovie_comments.data] newly uploaded. need to download
[navermovie_comments.models] newly uploaded. need to download
[navernews_10days.data] newly uploaded. need to download
[navernews_10days.models] newly uploaded. need to download
```

`fetch` 함수를 이용하여 데이터를 다운로드 받습니다.

```python
from lovit_textmining_dataset import fetch

fetch()
```

Update 혹은 download 해야 하는 파일들을 다운로드 받아 설치합니다.

```
[navermovie_comments.data] newly uploaded. need to download
  - successed to download navermovie_comments.data.zip
  - successed to unzip navermovie_comments.data
[navermovie_comments.models] newly uploaded. need to download
  - successed to download navermovie_comments.models.zip
  - successed to unzip navermovie_comments.models
[navernews_10days.data] newly uploaded. need to download
  - successed to download navernews_10days.data.zip
  - successed to unzip navernews_10days.data
[navernews_10days.models] newly uploaded. need to download
  - successed to download navernews_10days.models.zip
  - successed to unzip navernews_10days.models
```

설치가 완료되면 `version_check` 나 `fetch` 를 실행시켜도 아래처럼 메시지가 출력됩니다.

```pyton
fetch() # or version_check()
```

```
[navermovie_comments.data] is latest version (0.0.1)
[navermovie_comments.models] is latest version (0.0.1)
[navernews_10days.data] is latest version (0.0.1)
[navernews_10days.models] is latest version (0.0.1)
```

### Download only a data

모든 데이터가 아닌 하나의 데이터만을 download 혹은 update 할 수 있습니다.

`navernews_10days` 의 models 만 업데이트 하려면 아래처럼 입력합니다. `content` 는 dataset 의 하위 폴더 입니다.

```python
fetch(dataset='navernews_10days', content='models')
```

`navernews_10days` 의 `data` 와 `models` 를 모두 다운로드 하려면 `dataset` 만 지정합니다.

```python
fetch(dataset='navernews_10days')
```

## Dataset usage

각 데이터셋마다 제공되는 함수가 다릅니다. 데이터셋의 README 에 각 데이터셋이 제공하는 함수들의 사용법을 정리하였습니다. 아래 문서들을 살펴보세요.

- [navernews_10days](/lovit_textmining_dataset/navernews_10days/README.md): 2016-10-20 ~ 2016-10-29, 10 일 간의 뉴스 및 뉴스 댓글 데이터
- [navermovie_comments](/lovit_textmining_dataset/navermovie_comments/README.md): 네이버 영화에서 수집한 영화 평, 평점 데이터
