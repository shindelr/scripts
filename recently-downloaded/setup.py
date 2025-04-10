from setuptools import setup

setup(
    name='rdl',
    version='0.1.0',
    py_modules=['rdl'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'rdl = rdl:cli',
        ],
    },
)