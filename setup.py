import os.path
import pathlib
from setuptools import setup
from unittest import TestLoader

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

def tests():
    return TestLoader().discover('test', pattern='test_*.py')


setup(
    name='xr',
    version='1.0.0',
    description="Easy Regular expression builder for people.",
    url="https://xr.deprince.io",
    author="Adam DePrince",
    license="Apache",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",],
    packages=[
        'xr/',
        'xr/regex/'
    ],
    requires=[
        "six"
    ],
    test_suite='setup.tests',
    test_dir='tests',
    scripts=[])
