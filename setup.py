from setuptools import setup
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import d1ct

setup(
    name="d1ct",
    version=re.search(
        '__version__ = "(?P<content>.+)"',
        open("d1ct/__init__.py", encoding="utf8").read(),
    )["content"],
    packages=["d1ct"],
    package_dir={},
    url="https://www.github.com/ultrafunkamsterdam/d1ct",
    license="GPL",
    author="UltrafunkAmsterdam",
    author_email="info@ultrafunk.nl",
    description=re.search(
        '__description__ = "(?P<content>.+)"',
        open("d1ct/__init__.py", encoding="utf8").read(),
    )["content"],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf8").read(),
)
