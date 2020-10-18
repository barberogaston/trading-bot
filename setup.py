from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='trading_bot',
    version='0.0.1',
    packages=find_packages(where='.'),
    install_requires=[
        'keras',
        'tensorflow',
        'pandas',
        'numpy',
        'tqdm',
        'docopt',
        'coloredlogs',
        'jupyterlab',
        'altair',
        'ipython',
        'pycoingecko',
        'ta',
        'click',
        'fastapi',
        'uvicorn'
    ]
)
