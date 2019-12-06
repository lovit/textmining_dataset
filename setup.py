import lovit_textmining_dataset as td
import setuptools
from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lovit_textmining_dataset",
    version=td.__version__,
    author=td.__author__,
    author_email='soy.lovit@gmail.com',
    description="Dataset for textmining",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lovit/textmining_dataset',
    packages=setuptools.find_packages(),
)