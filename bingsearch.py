import urllib2
import requests


class BingSearch(object):

    # Bing Search API 2.0
    QUERY_URL = 'https://api.datamarket.azure.com/Bing/Search/Web' \
                 + '?Query={}&$top={}&$skip={}&$format={}'
    MAX = 50

    def __init__(self, api_key):
        self.api_key = api_key
        self.counter = 0
        self.unique = {}

    def search(self, query, limit=50, offset=0, format='json'):
        return self._search(query, limit, offset, format)

    def search_all(self, query, limit=50, offset=0, format='json'):
        self.counter = 0
        print 'GIMBEL 1 - query={}, limit={}, offset={}, format={}.'.format(query, limit, offset, format)
        results, left, offset = self._search_all(query, limit, offset, format)
        more_results = results
        print 'limit={}, left={}, offset={}, more_results={}, results={}.'.format(limit, left, offset, len(more_results), len(results))
        while len(more_results) == self.MAX and len(results) < limit:
            more_results, left, offset = self._search_all(query, left,
                                                          offset, format)
            results += more_results
            print 'limit={}, left={}, offset={}, more_results={}, results={}.'.format(limit, left, offset, len(more_results), len(results))
        return results

    def _search_all(self, query, limit, offset, format):
        self.counter += 1
        print 'GIMBEL 1.1 - counter={}, limit={}, offset={}.'.format(self.counter, limit, offset)
        results = self._search(query, limit, offset, format)
        for r in results:
            self.unique[r.id] = 1
        limit -= len(results)
        offset += len(results)
        print 'GIMBEL 1.2 - results={}, unique={}, limit={}, offset={}.'.format(len(results), len(self.unique), limit, offset)
        return results, limit, offset

    def _search(self, query, limit, offset, format):
        url = self.QUERY_URL.format(urllib2.quote("'{}'".format(query)),
                                    limit, offset, format)
        r = requests.get(url, auth=('', self.api_key))
        try:
            results = Results(r.json()['d']['results'])
        except Exception as e:
            raise Exception(e, r.text)
        return results

class Results(object):

    class _Meta(object):
        def __init__(self, meta):
            self.type = meta['type']
            self.uri = meta['uri']

    class _Result(object):
        def __init__(self, result):
            self.id = result['ID']
            self.url = result['Url']
            self.display_url = result['DisplayUrl']
            self.title = result['Title']
            self.description = result['Description']
            self.meta = Results._Meta(result['__metadata'])

    def __init__(self, results):
        self.results = []
        for result in results:
            self.results.append(self._Result(result))

    def __getitem__(self, i):
        return self.results[i]

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        for result in self.results:
            yield result

    def __iadd__(self, results):
        self.results.extend(results.results)
        return self
