"""
cloudyvideos urlresolver plugin
Copyright (C) 2015 Lynx187

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
import urllib
from lib import jsunpack
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError
import xbmc

class CloudyVideosResolver(UrlResolver):
    name = "cloudyvideos"
    domains = ["cloudyvideos.com"]
    pattern = '(?://|\.)(cloudyvideos\.com)/([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content
        form_values = {}
        stream_url = ''
        for i in re.finditer('<input type="hidden" name="([^"]+)" value="([^"]+)', html):
            form_values[i.group(1)] = i.group(2)

        xbmc.sleep(2000)
        header = {'Referer': web_url}
        html = self.net.http_POST(web_url, form_data=form_values, headers=header).content

        r = re.search("file\s*:\s*'([^']+)'", html)
        if r:
            stream_url = r.group(1)

        for match in re.finditer('(eval\(function.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            match2 = re.search('<param\s+name="src"\s*value="([^"]+)', js_data)
            if match2:
                stream_url = match2.group(1)
            else:
                match2 = re.search('<embed.*?type="video.*?src="([^"]+)', js_data)
                if match2:
                    stream_url = match2.group(1)

        if stream_url:
            return stream_url + '|' + urllib.urlencode({'User-Agent': common.IE_USER_AGENT, 'Referer': web_url})

        raise ResolverError('Unable to resolve cloudyvideos link. Filelink not found.')

    def get_url(self, host, media_id):
        return 'http://cloudyvideos.com/%s' % (media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        return re.search(self.pattern, url) or self.name in host
