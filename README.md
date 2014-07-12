Usage
=====

    >>> from bingsearch import BingSearch
    >>>
    >>> bing = BingSearch('APIKey')
    >>>
    >>> r = bing.search('Python Software Foundation', limit=25, offset=5, format='json')
    >>> len(r)
    50
    >>> r[0].description
    u'Python Software Foundation Home Page. The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to ...'
    >>> r[0].url
    u'http://www.python.org/psf/'
    >>>
    >>> r = bing.search_all('Python Software Foundation', limit=175, offset=200, format='json')
    >>> len(r)
    175
