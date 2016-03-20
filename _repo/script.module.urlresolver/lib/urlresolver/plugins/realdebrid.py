"""
    URLResolver Addon for Kodi
    Copyright (C) 2016 t0mm0, tknorris

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
import urllib2
import json
import xbmcgui
import xbmc
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

CLIENT_ID = 'MUQMIQX6YWDSU'
USER_AGENT = 'URLResolver for Kodi/%s' % (common.addon_version)
INTERVALS = 5

class RealDebridResolver(UrlResolver):
    name = "Real-Debrid"
    domains = ["*"]

    def __init__(self):
        self.net = common.Net()
        self.hosters = None
        self.hosts = None
        self.headers = {'User-Agent': USER_AGENT}

    def get_media_url(self, host, media_id, retry=False):
        try:
            url = 'https://api.real-debrid.com/rest/1.0/unrestrict/link'
            headers = self.headers
            headers['Authorization'] = 'Bearer %s' % (self.get_setting('token'))
            data = {'link': media_id}
            result = self.net.http_POST(url, form_data=data, headers=headers).content
        except urllib2.HTTPError as e:
            if not retry and e.code == 401:
                if self.get_setting('refresh'):
                    self.refresh_token()
                    return self.get_media_url(host, media_id, retry=True)
                else:
                    self.reset_authorization()
                    raise ResolverError('Real Debrid Auth Failed & No Refresh Token')
            else:
                try:
                    js_result = json.loads(e.read())
                    if 'error' in js_result:
                        msg = js_result['error']
                    else:
                        msg = 'Unknown Error (1)'
                except:
                    msg = 'Unknown Error (2)'
                raise ResolverError('Real Debrid Error: %s (%s)' % (msg, e.code))
        except Exception as e:
            raise ResolverError('Unexpected Exception during RD Unrestrict: %s' % (e))
        else:
            js_result = json.loads(result)
            links = []
            link = self.__get_link(js_result)
            if link is not None: links.append(link)
            if 'alternative' in js_result:
                for alt in js_result['alternative']:
                    link = self.__get_link(alt)
                    if link is not None: links.append(link)

            if len(links) == 1 or self.get_setting('autopick') == 'true':
                return links[0][1]
            elif len(links) > 1:
                sd = xbmcgui.Dialog()
                ret = sd.select('Select a Link', [link[0] for link in links])
                if ret > -1:
                    return links[ret][1]
            else:
                raise ResolverError('No usable link from Real Debrid')

    def __get_link(self, link):
        if 'download' in link:
            if 'quality' in link:
                label = '[%s] %s' % (link['quality'], link['download'])
            else:
                label = link['download']
            return (label, link['download'])

    # SiteAuth methods
    def login(self):
        if not self.get_setting('token'):
            self.authorize_resolver()

    def refresh_token(self):
        url = 'https://api.real-debrid.com/oauth/v2/token'
        client_id = self.get_setting('client_id')
        client_secret = self.get_setting('client_secret')
        refresh_token = self.get_setting('refresh')
        data = {'client_id': client_id, 'client_secret': client_secret, 'code': refresh_token, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        common.log_utils.log_debug('Refreshing Expired Real Debrid Token: |%s|%s|' % (client_id, refresh_token))
        try:
            js_result = json.loads(self.net.http_POST(url, data, headers=self.headers).content)
            common.log_utils.log_debug('Refreshed Real Debrid Token: |%s|' % (js_result))
            self.set_setting('token', js_result['access_token'])
            self.set_setting('refresh', js_result['refresh_token'])
        except Exception as e:
            # empty all auth settings to force a re-auth on next use
            self.reset_authorization()
            raise ResolverError('Unable to Refresh Real Debrid Token: %s' % (e))

    def authorize_resolver(self):
        url = 'https://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes' % (CLIENT_ID)
        js_result = json.loads(self.net.http_GET(url, headers=self.headers).content)
        pd = xbmcgui.DialogProgress()
        line1 = 'Go to URL: %s' % (js_result['verification_url'])
        line2 = 'When prompted enter: %s' % (js_result['user_code'])
        try:
            pd.create('URL Resolver Real Debrid Authorization', line1, line2)
            interval = js_result['interval'] * 1000
            device_code = js_result['device_code']
            while True:
                try:
                    url = 'https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s' % (CLIENT_ID, device_code)
                    js_result = json.loads(self.net.http_GET(url, headers=self.headers).content)
                except Exception as e:
                    common.log_utils.log_debug('Exception during RD auth: %s' % (e))
                    for _ in range(INTERVALS):
                        if pd.iscanceled(): return False
                        xbmc.sleep(interval / INTERVALS)
                else:
                    break
        finally:
            pd.close()

        url = 'https://api.real-debrid.com/oauth/v2/token'
        data = {'client_id': js_result['client_id'], 'client_secret': js_result['client_secret'], 'code': device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        self.set_setting('client_id', js_result['client_id'])
        self.set_setting('client_secret', js_result['client_secret'])
        common.log_utils.log_debug('Authorizing Real Debrid: %s' % (js_result['client_id']))
        js_result = json.loads(self.net.http_POST(url, data, headers=self.headers).content)
        common.log_utils.log_debug('Authorizing Real Debrid Result: |%s|' % (js_result))
        self.set_setting('token', js_result['access_token'])
        self.set_setting('refresh', js_result['refresh_token'])
        return True

    def reset_authorization(self):
        self.set_setting('client_id', '')
        self.set_setting('client_secret', '')
        self.set_setting('token', '')
        self.set_setting('refresh', '')
    
    def get_url(self, host, media_id):
        return media_id

    def get_host_and_id(self, url):
        return 'www.real-debrid.com', url

    def get_all_hosters(self):
        if self.hosters is None:
            try:
                url = 'https://api.real-debrid.com/rest/1.0/hosts/regex'
                self.hosters = []
                js_result = json.loads(self.net.http_GET(url, headers=self.headers).content)
                regexes = [regex.lstrip('/').rstrip('/').replace('\/', '/') for regex in js_result]
                self.hosters = [re.compile(regex) for regex in regexes]
            except Exception as e:
                common.log_utils.log_error('Error getting RD regexes: %s' % (e))
                self.hosters = []
        # common.log_utils.log_debug('RealDebrid hosters : %s' % self.hosters)
        return self.hosters

    def get_hosts(self):
        if self.hosts is None:
            try:
                url = 'https://api.real-debrid.com/rest/1.0/hosts/domains'
                self.hosts = json.loads(self.net.http_GET(url, headers=self.headers).content)
            except Exception as e:
                common.log_utils.log_error('Error getting RD hosts: %s' % (e))
                self.hosts = []
        common.log_utils.log_debug('RealDebrid hosts : %s' % self.hosts)

    @classmethod
    def _is_enabled(cls):
        return cls.get_setting('enabled') == 'true' and cls.get_setting('token')

    def valid_url(self, url, host):
        common.log_utils.log_debug('in valid_url %s : %s' % (url, host))
        if url:
            self.get_all_hosters()
            for host in self.hosters:
                # common.log_utils.log_debug('RealDebrid checking host : %s' %str(host))
                if re.search(host, url):
                    common.log_utils.log_debug('RealDebrid Match found')
                    return True
        elif host:
            self.get_hosts()
            if host.startswith('www.'): host = host.replace('www.', '')
            if any(host in item for item in self.hosts):
                return True
        return False

    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting id="%s_autopick" type="bool" label="Choose Primary Link Automatically" default="false"/>' % (cls.__name__))
        xml.append('<setting id="%s_auth" type="action" label="(Re)Authorize My Account" action="RunPlugin(plugin://script.module.urlresolver/?mode=auth_rd)"/>' % (cls.__name__))
        xml.append('<setting id="%s_reset" type="action" label="Reset My Authorization" action="RunPlugin(plugin://script.module.urlresolver/?mode=reset_rd)"/>' % (cls.__name__))
        xml.append('<setting id="%s_token" visible="false" type="text" default=""/>' % (cls.__name__))
        xml.append('<setting id="%s_refresh" visible="false" type="text" default=""/>' % (cls.__name__))
        xml.append('<setting id="%s_client_id" visible="false" type="text" default=""/>' % (cls.__name__))
        xml.append('<setting id="%s_client_secret" visible="false" type="text" default=""/>' % (cls.__name__))
        return xml

    @classmethod
    def isUniversal(self):
        return True
