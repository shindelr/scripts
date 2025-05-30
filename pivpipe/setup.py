from setuptools import setup, find_packages

setup(
    name='pivpipe',
    version='0.1.0',
    py_modules=['pivpipe'],
    install_requires=['PyYAML', 'click'],
    
    entry_points={
        'console_scripts': [
            'pivpipe = pivpipe:main',
        ],
    },
)