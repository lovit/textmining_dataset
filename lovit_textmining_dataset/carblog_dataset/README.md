## Carblog dataset

This dataset consists of blog posts that have been scraped from Naver blog which created from 2010. 01. 01 to 2015. 08. 01.

This dataset includes 27 sub-datasets that scraped with a query term (Each blog posts in a sub-dataset includes the query term). Query terms (term index) are described in `car_index` file.

It needs about 15 GB disk space to decompress zip files and store text files.

## Usage

To load text data

```python
from carblog_dataset import load_text

category = 7
texts = load_text()
```

To load meta information such as date, user generated tags, or title.

```python
from carblog_dataset import load_index

category = 7
index = load_index(category)
# or
index = load_index(category, date=True, tags=False, title=False)
```
