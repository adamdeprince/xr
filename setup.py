import os.path
from setuptools import setup
from unittest import TestLoader

def tests():
    return TestLoader().discover('test', pattern='test_*.py')


setup(
    name='xr',
    version='1.0.4',
    description="Easy Regular expression builder for people.",
    long_description = os.path.join(os.path.dirname(__file__), 'README.md'),
    long_description_content_type="text/markdown",
    url="https://xr.deprince.io",
    author="Adam DePrince",
    author_email="adamdeprince@gmail.com",
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
    install_requires=[
        "six"
    ],
    test_suite='setup.tests',
    test_dir='tests',
    scripts=[])
