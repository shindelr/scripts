from setuptools import setup, find_packages

setup(
    name='rdl',
    version='0.1.0',
    py_modules=['rdl'],
    install_requires=find_packages(),
    
    entry_points={
        'console_scripts': [
            'rdl = rdl:cli',
        ],
    },
)