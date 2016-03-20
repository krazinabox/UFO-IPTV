"""
    urlresolver XBMC Addon
    Copyright (C) 2015 tknorris

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
import json
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class RPnetResolver(UrlResolver):
    name = "RPnet"
    domains = ["*"]

    def __init__(self):
        self.net = common.Net()
        self.patterns = None
        self.hosts = None

    # UrlResolver methods
    def get_media_url(self, host, media_id):
        username = self.get_setting('username')
        password = self.get_setting('password')
        url = 'https://premium.rpnet.biz/client_api.php?'
        query = urllib.urlencode({'username': username, 'password': password, 'action': 'generate', 'links': media_id})
        url = url + query
        response = self.net.http_GET(url).content
        response = json.loads(response)
        if 'links' in response and response['links']:
            link = response['links'][0]
            if 'generated' in link:
                return link['generated']
            elif 'error' in link:
                raise ResolverError(link['error'])
        else:
            raise ResolverError('No Link Returned')

    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return 'rpnet.biz', url

    def get_all_hosters(self):
        if self.patterns is None:
            url = 'http://premium.rpnet.biz/hoster.json'
            response = self.net.http_GET(url).content
            hosters = json.loads(response)
            common.log_utils.log_debug('rpnet patterns: %s' % hosters)
            self.patterns = [re.compile(pattern) for pattern in hosters['supported']]
        return self.patterns

    def get_hosts(self):
        if self.hosts is None:
            url = 'http://premium.rpnet.biz/hoster2.json'
            response = self.net.http_GET(url).content
            common.log_utils.log_debug('rpnet hosts: %s' % response)
            self.hosts = json.loads(response)['supported']

    def valid_url(self, url, host):
        if url:
            self.get_all_hosters()
            for pattern in self.patterns:
                if pattern.search(url):
                    return True
        elif host:
            self.get_hosts()
            if host.startswith('www.'): host = host.replace('www.', '')
            if host in self.hosts or any(host in item for item in self.hosts):
                return True

        return False

    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting id="%s_login" type="bool" label="login" default="false"/>' % (cls.__name__))
        xml.append('<setting id="%s_username" enable="eq(-1,true)" type="text" label="Username" default=""/>' % (cls.__name__))
        xml.append('<setting id="%s_password" enable="eq(-2,true)" type="text" label="Password" option="hidden" default=""/>' % (cls.__name__))
        return xml

    @classmethod
    def isUniversal(self):
        return True
