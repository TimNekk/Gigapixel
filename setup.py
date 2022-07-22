from io import open
from setuptools import setup


version = '0.1.0'
name = 'gigapixel'


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=name,
    version=version,

    author='TimNekk',
    author_email='herew26@gmail.com',

    description=(
        'Topaz Gigapixel AI automation tool'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/TimNekk/Gigapixel',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=[name],
    install_requires=[
        'pywinauto',
        'clipboard',
        'loguru',
    ],
    extras_require={
        'dev': [
            'flake8==4.0.1',
            'mypy==0.961'
        ]
    },

    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools-git-versioning"],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
