# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

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

import re,urllib,urlparse,json,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import dom_parser
from resources.lib.libraries import trakt
from resources.lib.libraries import tvmaze
from resources.lib.libraries import jsunpack
from resources.lib.libraries import source_utils


import cookielib, os
cookie_file = os.path.join(control.dataPath , 'mycookie'+'.cookies')
cj = cookielib.LWPCookieJar()

class source:
    def __init__(self):
        self.base_link = 'http://www.pelispedia.tv'
        self.moviesearch_link = '/pelicula/%s/'
        self.tvsearch_link = '/serie/%s/'
        self.protect_link = 'http://player.pelispedia.tv/template/protected.php'



    def get_movie(self, imdb, title, year):
        try:
            url = self.__search(self.moviesearch_link, title, year)
            if not url: url = self.__search(self.tvsearch_link, title + '-', year)
            if not url: url = self.__search(self.moviesearch_link, trakt.getMovieTranslation(imdb, 'es'), year)
            return url
        except:
            pass

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = self.__search(self.tvsearch_link, tvshowtitle, year)
            if not url: url = self.__search(self.tvsearch_link, tvshowtitle + '-', year)
            if not url: url = self.__search(self.tvsearch_link, tvmaze.tvMaze().getTVShowTranslation(tvdb, 'es'), year)


            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = dom_parser.parse_dom(r, 'article', {'class': 'SeasonList'})
            r = dom_parser.parse_dom(r, 'ul')
            r = dom_parser.parse_dom(r, 'li')
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('[^"]+-season-%s-episode-%s(?!\d)[^"]*' % (season, episode))}, req='href')[0].attrs['href']

            return source_utils.strip_domain(r)
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        control.log("><><><><> PELISPEDIA SOURCE %s" % url)
        #sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Pelispedia', 'url': i['url']})
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'div', {'class': 'repro'})

            r = dom_parser.parse_dom(r[0].content, 'iframe', req='src')
            f = r[0].attrs['src']

            r = client.request(f)
            r = dom_parser.parse_dom(r, 'div', {'id': 'botones'})
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], urlparse.urlparse(i.attrs['href']).netloc) for i in r]

            links = []

            for u, h in r:
                if not 'pelispedia' in h:
                    valid, host = source_utils.is_host_valid(u, hostDict)
                    if not valid: continue

                    links.append({'source': host, 'quality': 'SD', 'url': u})
                    continue

                result = client.request(u, headers={'Referer': f}, timeout='10')

                try:
                    if 'pelispedia' in h: raise Exception()

                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')\s*,\s*label\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)
                    url = [i[0] for i in url if '720' in i[1]][0]

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url})
                except:
                    pass

                try:
                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)

                    for i in url:
                        try:
                            links.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'url': i})
                        except:
                            pass
                except:
                    pass

                try:
                    post = re.findall('gkpluginsphp.*?link\s*:\s*"([^"]+)', result)[0]
                    post = urllib.urlencode({'link': post})

                    url = urlparse.urljoin(self.base_link, '/gkphp_flv/plugins/gkpluginsphp.php')
                    url = client.request(url, post=post, XHR=True, referer=u, timeout='10')
                    url = json.loads(url)['link']

                    links.append({'source': 'gvideo', 'quality': 'HD', 'url': url})
                except:
                    pass

                try:
                    post = re.findall('var\s+parametros\s*=\s*"([^"]+)', result)[0]

                    post = urlparse.parse_qs(urlparse.urlparse(post).query)['pic'][0]
                    post = urllib.urlencode({'sou': 'pic', 'fv': '25', 'url': post})

                    url = client.request(self.protect_link, post=post, XHR=True, timeout='10')
                    url = json.loads(url)[0]['url']

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url})
                except:
                    pass

                try:
                    if not jsunpack.detect(result): raise Exception()

                    result = jsunpack.unpack(result)
                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*.*?\'(.+?)\'', url)
                    for i in url:
                        try:
                            i = client.request(i, headers={'Referer': f}, output='geturl', timeout='10')
                            links.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'url': i})
                        except:
                            pass
                except:
                    pass

                try:
                    post = re.findall('var\s+parametros\s*=\s*"([^"]+)', result)[0]

                    post = urlparse.parse_qs(urlparse.urlparse(post).query)['pic'][0]
                    token = 'eyJjdCI6InZGS3QySm9KRWRwU0k4SzZoZHZKL2c9PSIsIml2IjoiNDRkNmMwMWE0ZjVkODk4YThlYmE2MzU0NDliYzQ5YWEiLCJzIjoiNWU4MGUwN2UwMjMxNDYxOCJ9'
                    post = urllib.urlencode({'sou': 'pic', 'fv': '0', 'url': post, 'token': token})

                    url = client.request(self.protect_link, post=post, XHR=True, timeout='10')
                    js = json.loads(url)
                    url = [i['url'] for i in js]
                    for i in url:
                        try:
                            i = client.request(i, headers={'Referer': f}, output='geturl', timeout='10')
                            links.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'url': i})
                        except:
                            pass
                except:
                    pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'url': i['url'], 'provider': 'Pelispedia'})

            return sources

        except Exception as e:
            control.log('ERROR PELISP %s' % e)
            return sources


    def resolve(self, url):
        control.log("##pelispedia %s " % url)

        return url


    def __search(self, search_url, title, year):
        try:
            url = search_url % cleantitle.geturl(title)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1', timeout='10')
            r = dom_parser.parse_dom(r, 'title')[0].content
            return url if year in r else None
        except:
            pass


