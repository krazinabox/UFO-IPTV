"""
primeshare urlresolver plugin
Copyright (C) 2013 Lynx187

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
import urllib2
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class PrimeshareResolver(UrlResolver):
    name = "primeshare"
    domains = ["primeshare.tv"]
    pattern = '(?://|\.)(primeshare\.tv)/download/([0-9a-zA-Z-_]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)

        headers = {'User-Agent': common.IOS_USER_AGENT}

        html = self.net.http_GET(web_url, headers=headers).content

        r = re.search('<video (.+?)</video>', html, re.DOTALL)
        if not r:
            raise ResolverError('File Not Found or removed')

        r = re.search('src\s*=\s*"(.+?)"', r.group(1), re.DOTALL)
        if not r:
            raise ResolverError('Unable to resolve Primeshare link. Filelink not found.')
        else:
            stream_url = r.group(1)

        r = urllib2.Request(stream_url, headers=headers)
        r = urllib2.urlopen(r, timeout=15)
        r = int(r.headers['Content-Length'])

        if r < 1024:
            raise ResolverError('File removed.')
        else:
            return stream_url

    def get_url(self, host, media_id):
        return 'http://primeshare.tv/download/%s' % (media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        return re.search(self.pattern, url) or self.name in host
