from setuptools import setup, find_packages
import os
import platform

DESCRIPTION = "A simple python wrapper for the Azure Bing Search API."

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='bingsearch',
    version='1.1',
    author=u'gimbel0893',
    author_email='mgimbel@rightbrainnetworks.com',
    py_modules=['bingsearch'],
    url='http://github.com/gimbel0893/bingsearch',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=['requests'],
)
