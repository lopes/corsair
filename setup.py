#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Corsair',
    version='0.3.0',
    author='José Lopes de Oliveira Jr.',
    author_email='2897144+forkd@users.noreply.github.com',
    description='Python wrappers for some NSOC tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/forkd/corsair',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)