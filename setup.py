#!/usr/bin/python3
# Setup script to install this package.
# M.Blakeney, May 2022.

from pathlib import Path
from setuptools import setup

name = 'nbtopy'
module = name.replace('-', '_')
here = Path(__file__).resolve().parent

setup(
    name=name,
    version='1.0',
    description='Converts Jupyter notebook file[s] to Python '
    '(interactive) file[s].',
    long_description=here.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/bulletmark/{name}',
    author='Mark Blakeney',
    author_email='mark.blakeney@bullet-systems.net',
    keywords='jupyter notebook nbconvert vscode',
    license='GPLv3',
    py_modules=[module],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        (f'share/{name}', ['README.md']),
    ],
    entry_points={
        'console_scripts': [f'{name}={module}:main'],
    },
)
