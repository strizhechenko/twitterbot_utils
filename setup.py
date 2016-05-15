#!/usr/bin/env python

'''The setup and build script for the twitterbot-utils library.'''

import os

from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='twitterbot_utils',
    version='0.1.8',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    license='GPL',
    url='https://github.com/strizhechenko/twitterbot_utils',
    keywords='twitter api bot',
    description='wrapper around the Tweepy',
    long_description=(read('README.rst')),
    packages=find_packages(exclude=['tests*']),
    install_requires=['tweepy==3.1.0', 'requests==2.4.3', 'requests-oauthlib==0.4.1', 'pymorphy2'],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Operating System :: MacOS',
      'Operating System :: POSIX',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development',
      'Topic :: Utilities',
    ],
)
