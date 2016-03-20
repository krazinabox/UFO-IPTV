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
'''
This module provides the main API for accessing the urlresolver features.

For most cases you probably want to use :func:`urlresolver.resolve` or
:func:`urlresolver.choose_source`.

.. seealso::
    
    :class:`HostedMediaFile`


'''
import sys
import os
import xbmcgui
import common
import xml.dom.minidom
from hmf import HostedMediaFile
from urlresolver.resolver import UrlResolver
from plugins import *

common.log_utils.log_notice('Initializing URLResolver version: %s' % (common.addon_version))
MAX_SETTINGS = 75

PLUGIN_DIRS = []

def add_plugin_dirs(dirs):
    global PLUGIN_DIRS
    if isinstance(dirs, basestring):
        PLUGIN_DIRS.append(dirs)
    else:
        PLUGIN_DIRS += dirs

def load_external_plugins():
    for d in PLUGIN_DIRS:
        common.log_utils.log_debug('Adding plugin path: %s' % (d))
        sys.path.insert(0, d)
        for filename in os.listdir(d):
            if not filename.startswith('__') and filename.endswith('.py'):
                mod_name = filename[:-3]
                imp = __import__(mod_name, globals(), locals())
                sys.modules[mod_name] = imp
                common.log_utils.log_debug('Loaded %s as %s from %s' % (imp, mod_name, filename))

def relevant_resolvers(domain=None, include_universal=None, include_external=False, include_disabled=False, order_matters=False):
    if include_external:
        load_external_plugins()

    if include_universal is None:
        include_universal = common.get_setting('allow_universal') == "true"
        
    classes = UrlResolver.__class__.__subclasses__(UrlResolver)
    relevant = []
    for resolver in classes:
        if include_disabled or resolver._is_enabled():
            if include_universal or not resolver.isUniversal():
                if domain is None or (any(domain in res_domain for res_domain in resolver.domains) or '*' in resolver.domains):
                    relevant.append(resolver)

    if order_matters:
        relevant.sort(key=lambda x: x._get_priority())

    common.log_utils.log_debug('Relevant Resolvers: %s' % (relevant))
    return relevant

def resolve(web_url):
    '''
    Resolve a web page to a media stream.

    It is usually as simple as::

        import urlresolver
        media_url = urlresolver.resolve(web_url)

    where ``web_url`` is the address of a web page which is associated with a
    media file and ``media_url`` is the direct URL to the media.

    Behind the scenes, :mod:`urlresolver` will check each of the available
    resolver plugins to see if they accept the ``web_url`` in priority order
    (lowest priotity number first). When it finds a plugin willing to resolve
    the URL, it passes the ``web_url`` to the plugin and returns the direct URL
    to the media file, or ``False`` if it was not possible to resolve.

    .. seealso::

        :class:`HostedMediaFile`

    Args:
        web_url (str): A URL to a web page associated with a piece of media
        content.

    Returns:
        If the ``web_url`` could be resolved, a string containing the direct
        URL to the media file, if not, returns ``False``.
    '''
    source = HostedMediaFile(url=web_url)
    return source.resolve()

def filter_source_list(source_list):
    '''
    Takes a list of :class:`HostedMediaFile`s representing web pages that are
    thought to be associated with media content. If no resolver plugins exist
    to resolve a :class:`HostedMediaFile` to a link to a media file it is
    removed from the list.

    Args:
        urls (list of :class:`HostedMediaFile`): A list of
        :class:`HostedMediaFiles` representing web pages that are thought to be
        associated with media content.

    Returns:
        The same list of :class:`HostedMediaFile` but with any that can't be
        resolved by a resolver plugin removed.

    '''
    return [source for source in source_list if source]


def choose_source(sources):
    '''
    Given a list of :class:`HostedMediaFile` representing web pages that are
    thought to be associated with media content this function checks which are
    playable and if there are more than one it pops up a dialog box displaying
    the choices.

    Example::

        sources = [HostedMediaFile(url='http://youtu.be/VIDEOID', title='Youtube [verified] (20 views)'),
                   HostedMediaFile(url='http://putlocker.com/file/VIDEOID', title='Putlocker (3 views)')]
        source = urlresolver.choose_source(sources)
        if source:
            stream_url = source.resolve()
            addon.resolve_url(stream_url)
        else:
            addon.resolve_url(False)

    Args:
        sources (list): A list of :class:`HostedMediaFile` representing web
        pages that are thought to be associated with media content.

    Returns:
        The chosen :class:`HostedMediaFile` or ``False`` if the dialog is
        cancelled or none of the :class:`HostedMediaFile` are resolvable.

    '''
    sources = filter_source_list(sources)
    if not sources:
        common.log_utils.log_warning('no playable streams found')
        return False
    elif len(sources) == 1:
        return sources[0]
    else:
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose your stream', [source.title for source in sources])
        if index > -1:
            return sources[index]
        else:
            return False

def display_settings():
    '''
    Opens the settings dialog for :mod:`urlresolver` and its plugins.

    This can be called from your addon to provide access to global
    :mod:`urlresolver` settings. Each resolver plugin is also capable of
    exposing settings.

    .. note::

        All changes made to these setting by the user are global and will
        affect any addon that uses :mod:`urlresolver` and its plugins.
    '''
    _update_settings_xml()
    common.addon.openSettings()

def _update_settings_xml():
    '''
    This function writes a new ``resources/settings.xml`` file which contains
    all settings for this addon and its plugins.
    '''
    try:
        os.makedirs(os.path.dirname(common.settings_file))
    except OSError:
        pass

    new_xml = [
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
        '<settings>',
        '<category label="URLResolver">',
        '<setting default="true" id="allow_universal" label="Enable Universal Resolvers" type="bool"/>',
        '<setting id="personal_nid" label="Your NID" type="text" visible="false"/>',
        '</category>',
        '<category label="Universal Resolvers">']

    resolvers = relevant_resolvers(include_universal=True, include_disabled=True)
    resolvers = sorted(resolvers, key=lambda x: x.name.upper())
    for resolver in resolvers:
        if resolver.isUniversal():
            new_xml.append('<setting label="%s" type="lsep"/>' % (resolver.name))
            new_xml += resolver.get_settings_xml()
    new_xml.append('</category>')
    new_xml.append('<category label="Resolvers 1">')

    i = 0
    cat_count = 2
    for resolver in resolvers:
        if not resolver.isUniversal():
            if i <= MAX_SETTINGS:
                new_xml.append('<setting label="%s" type="lsep"/>' % (resolver.name))
                res_xml = resolver.get_settings_xml()
                new_xml += res_xml
                i += len(res_xml) + 1
            else:
                new_xml.append('</category>')
                new_xml.append('<category label="Resolvers %s">' % (cat_count))
                cat_count += 1
                i = 0

    new_xml.append('</category>')
    new_xml.append('</settings>')

    try:
        with open(common.settings_file, 'r') as f:
            old_xml = f.read()
    except:
        old_xml = ''

    new_xml = ''.join(new_xml)
    new_xml = xml.dom.minidom.parseString(new_xml)
    new_xml = new_xml.toprettyxml()
    if old_xml != new_xml:
        common.log_utils.log_debug('Updating Settings XML')
        try:
            with open(common.settings_file, 'w') as f:
                f.write(new_xml)
        except:
            raise
    else:
        common.log_utils.log_debug('No Settings Update Needed')

_update_settings_xml()
