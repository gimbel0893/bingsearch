import urllib2
import requests


class BingSearch(object):

    # Bing Search API 2.0
    QUERY_URL = 'https://api.datamarket.azure.com/Bing/Search/Web' \
                 + '?Query={}&$top={}&$skip={}&$format={}'
    MAX = 50

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query, limit=50, offset=0, format='json'):
        return self._search(query, limit, offset, format)

    def search_all(self, query, limit=50, offset=0, format='json'):
        results, left, offset = self._search_all(query, limit, offset, format)
        more_results = results
        while len(more_results) >= self.MAX and len(results) < limit:
            more_results, left, offset = self._search_all(query, left,
                                                          offset, format)
            results += more_results
        return results

    def _search_all(self, query, limit, offset, format):
        results = self._search(query, limit, offset, format)
        limit -= len(results)
        offset += len(results)
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
