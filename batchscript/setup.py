from setuptools import setup

setup(
    name='batcher',
    version='0.1.0',
    py_modules=['batcher'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'batcher = batcher:cli',
        ],
    },
)