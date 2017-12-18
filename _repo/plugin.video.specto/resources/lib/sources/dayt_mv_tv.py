# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse

from resources.lib.libraries import client
from resources.lib.libraries import directstream


class source:
    def __init__(self):
        self.base_link = 'http://cyro.se'
        self.watch_link = '/watch/%s'
        self.watch_series_link = '/watch/%s/s%s/e%s'

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'title': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url is None: return
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = {'imdb': imdb, 'title': data['title'], 'year': data['year'], 'season': season, 'episode': episode}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = (data['title'].translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
            try:
                is_movie = not (int(data['episode']) > 0)
            except:
                is_movie = True

            if is_movie:
                url = urlparse.urljoin(self.base_link, self.watch_link % title)
            else:
                url = urlparse.urljoin(self.base_link, self.watch_series_link % (title, data['season'], data['episode']))

            r = client.request(url, output='geturl')

            if r is None: raise Exception()

            r = client.request(url)
            r = re.sub(r'[^\x00-\x7F]+',' ', r)
            result = r

            y = re.findall('Date\s*:\s*.+?>.+?(\d{4})', r)
            y = y[0] if len(y) > 0 else None

            if is_movie:
                if not (data['imdb'] in r or data['year'] == y): raise Exception()

            q = client.parseDOM(r, 'title')
            q = q[0] if len(q) > 0 else None

            quality = '1080p' if ' 1080' in q else 'HD'
            r = client.parseDOM(r, 'div', attrs = {'id': '5throw'})[0]
            r = client.parseDOM(r, 'a', ret='href', attrs = {'rel': 'nofollow'})

            links = []

            for url in r:
                try:
                    if 'yadi.sk' in url:
                        url = directstream.yandex(url)
                    elif 'mail.ru' in url:
                        url = directstream.cldmailru(url)
                    else:
                        raise Exception()

                    if url == None: raise Exception()
                    links += [{'source': 'cdn', 'url': url, 'quality': quality, 'direct': False}]
                except:
                    pass

            try:
                r = client.parseDOM(result, 'iframe', ret='src')
                if is_movie:
                    r = [i for i in r if 'pasmov' in i][0]
                else:
                    r = [i for i in r if 'pasep' in i][0]

                for i in range(0, 4):
                    try:
                        if not r.startswith('http'):
                            r = urlparse.urljoin(self.base_link, r)
                        r = client.request(r)
                        r = re.sub(r'[^\x00-\x7F]+',' ', r)
                        r = client.parseDOM(r, 'iframe', ret='src')[0]
                        if 'google' in r: break
                    except:
                        break

                if not 'google' in r: raise Exception()
                r = directstream.google(r)

                for i in r:
                    try:
                        links += [{'source': 'gvideo', 'url': i['url'], 'quality': i['quality']}]
                    except:
                        pass
            except:
                pass

            for i in links:
                sources.append({'source': i['source'], 'quality': i['quality'], 'url': i['url'], 'provider': 'Dayt'})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url