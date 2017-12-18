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


import re,urllib,urllib2,urlparse,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control

from resources.lib import resolvers
from resources.lib.libraries import workers
from resources.lib.libraries import control
from resources.lib.resolvers import cloudzilla
from resources.lib.resolvers import openload
from resources.lib.resolvers import uptobox
from resources.lib.resolvers import zstream
from resources.lib.resolvers import streamin


class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response

class source:
    def __init__(self):
        self.base_link = 'https://watchseriesfree.to'
        self.search_link = '/AdvancedSearch/%s-%s/by_popularity/%s'
        self.episode_link = '/episode/%s_s%s_e%s.html'
        self.headers = {}


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % (str(int(year)-1), str(int(year)+1), urllib.quote_plus(tvshowtitle))
            print query

            result = ''
            result = client.request(urlparse.urljoin(self.base_link, query))
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, 'div', attrs = {'class': 'episode-summary'})[0]
            result = client.parseDOM(result, 'tr')

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(re.compile('href=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[0], client.parseDOM(i, 'a')[-1]) for i in result]
            result = [(i[0], re.sub('<.+?>|</.+?>','', i[1])) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            result = [(client.replaceHTMLCodes(i[0]), i[1]) for i in result]
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            #print result,tvshowtitle,cleantitle.tv(result[0][1])

            match = [i[0] for i in result if cleantitle.tv(i[1]) in tvshowtitle]
            print match
            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0:
                        url = match[0]
                        break
                    result = client.request(self.base_link + i, headers=self.headers)
                    if str(imdb) in str(result):
                        url = i
                        break
                except:
                    pass

            url = url.encode('utf-8')
            return url
        except Exception as e:
            control.log('ERROR watchser GET %s' % e)
            return None


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, season, episode)
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def get_sources(self, url, hosthdDict, hostDict, locDict):

        try:
            self.sources =[]
            mylinks = []
            #hostDict = hostDict.sort()
            #for i in hostDict:
            #    control.log("WA HO %s" % i)
            if url == None: return self.sources

            url = url.replace('/json/', '/')

            result = ''

            r100 = client.request(urlparse.urljoin(self.base_link, url), output='extended')
            cookie = r100[4];headers = r100[3];result = r100[0]

            self.headers['Referer'] = urlparse.urljoin(self.base_link, url)
            self.headers['Cookie'] = cookie

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, 'div', attrs = {'id': 'lang_1'})[0]

            links = re.compile('href=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>].+?title=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(result)
            links = [x for y,x in enumerate(links) if x not in links[:y]]

            for i in links:
                try:
                    host = i[1]
                    host = host.split('.', 1)[0]
                    host = host.strip().lower()
                    #if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = i[0]
                    url = client.replaceHTMLCodes(url)
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    if not url.startswith('http'): url = urlparse.urljoin(self.base_link, url)
                    if not '/cale/' in url: raise Exception()
                    url = url.encode('utf-8')

                    url = url.replace('/json/', '/')
                    url = urlparse.urlparse(url).path
                    mylinks.append([url, 'SD'])
                except:
                    pass

            threads = []
            for i in mylinks[:15]: threads.append(workers.Thread(self.check, i, hostDict))
            [i.start() for i in threads]
            for i in range(0, 10 * 2):
                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(0.5)
            return self.sources
        except Exception as e:
            control.log('ERROR watchseries %s' % e)
            return self.sources


    def check(self, i, hostDict):
        try:
            url = client.replaceHTMLCodes(i[0])
            url = url.encode('utf-8')
            result = ''
            result = client.request(urlparse.urljoin(self.base_link, url), headers=self.headers)
            url = re.compile('class=[\'|\"]*myButton.+?href=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(result)[0]
            #print("URL2",url,i[1])
            #control.log("WATCHSERIES CHECK %s | url: %s" % (url,i[0]))
            url = client.replaceHTMLCodes(url)

            host = urlparse.urlparse(url).netloc
            host = host.replace('www.', '').replace('embed.', '')
            host = host.lower()
            if not host in hostDict:
                #control.log("WATCHSERIES HOST %s" % host)
                raise Exception()

            host = host.rsplit('.', 1)[0]
            host = client.replaceHTMLCodes(host)
            host = host.encode('utf-8')

            self.sources.append({'source': host, 'quality': i[1], 'provider': 'Watchseries', 'url': url})
        except:
            pass

    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return

