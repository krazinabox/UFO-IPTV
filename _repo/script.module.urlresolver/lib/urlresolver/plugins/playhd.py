"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

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
"""

import re
import urllib
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class PlayHDResolver(UrlResolver):
    name = "playhd.video"
    domains = ["www.playhd.video"]
    pattern = '(?://|\.)(playhd\.video)/embed\.php?.*?vid=([0-9]+)[\?&]*'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        resp = self.net.http_GET(web_url)
        html = resp.content
        headers = dict(resp._response.info().items())
        r = re.search('"content_video".*\n.*?src="(.*?)"', html)
        if r:
            stream_url = r.group(1) + '|' + urllib.urlencode({'Cookie': headers['set-cookie']})
        else:
            raise ResolverError('no file located')

        return stream_url

    def get_url(self, host, media_id):
        return 'http://www.playhd.video/embed.php?vid=%s' % (media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        return re.search(self.pattern, url) or self.name in host
