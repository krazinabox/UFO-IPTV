# -*- coding: utf-8 -*-
import sys
import os
import json
import urllib
import urllib2
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import load_channels
import hashlib
import re
import time
import xbmc
import net
import server
import config
import shutil
import unicodedata
import xbmc
import base64

from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.i4atv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
iconboxing = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/boxing.png')
iconmisc = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/misc.png')
icontna = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/prem.png')
iconufc = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/ufc.png')
iconwwe = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/wwe.png')
iconmaint = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/maint.png')
iconinter = xbmc.translatePath('special://home/addons/plugin.video.i4atv/media/inter.png')
usrdata = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.i4atv/')
Decode = base64.decodestring
directory = xbmc.translatePath('special://home/userdata/addon_data/script.tvguidetecbox/')
destinaddons = xbmc.translatePath('special://home/userdata/addon_data/script.tvguidetecbox/addons.ini')
destinsets = xbmc.translatePath('special://home/userdata/addon_data/script.tvguidetecbox/settings.xml')
directoryr = xbmc.translatePath('special://home/userdata/addon_data/script.renegadestv/')
destinaddonsr = xbmc.translatePath('special://home/userdata/addon_data/script.renegadestv/addons2.ini')
destinsetsr = xbmc.translatePath('special://home/userdata/addon_data/script.renegadestv/settings.xml')
destmw1dir = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.i4atv/')
destinf1 = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.i4atv/http_mw1_iptv66_tv-genres')
destinf2 = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.i4atv/http_mw1_iptv66_tv')
passreset = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.i4atv/settings.xml')
metaset = selfAddon.getSetting('enable_meta')

plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.i4atv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
online_m3u = mysettings.getSetting('online_m3u')
local_m3u = mysettings.getSetting('local_m3u')
online_xml = ('http://shanghai.watchkodi.com/Sections/Sports/Live%20games%20+%20Events/Live%20Football.xml')
local_xml = mysettings.getSetting('local_xml')
xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
u_tube = 'http://www.youtube.com'

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('profile') ) 

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
go = True;

xbmcplugin.setContent(addon_handle, 'movies')

net = net.Net()
dialog = xbmcgui.Dialog()

def Main():
	addDir('[COLOR yellow]          *** Welcome to I4ATV ***[/COLOR]','',0,icon, fanart)
	addDir('[COLOR yellow]*** Please Select An Option Below ***[/COLOR]','',0,icon, fanart)
	addDir('[COLOR magenta][I]###--Maintenance Tools Below--###[/I][/COLOR]','',0,icon, fanart)
	addDir('[COLOR blue]Clear Cache[/COLOR]','0',1000,iconmaint, fanart)
	addDir('[COLOR blue]Delete Packages[/COLOR]','0',1001,iconmaint, fanart)
	addDir('[COLOR blue]Reset I4ATV Extra user/pass[/COLOR]','0',1004,iconmaint, fanart)
	addDir('[COLOR blue]Delete I4ATV userdata[/COLOR]','0',1006,iconmaint, fanart)
	addDir('[COLOR magenta][I]###--TV Guide Integration Below--###[/I][/COLOR]','',0,icon, fanart)
	addDir('[COLOR green]Ivue Integration - I4ATV Only[/COLOR]','0',9,iconinter, fanart)
	addDir('[COLOR green]Renegades Integration - I4ATV Only[/COLOR]','0',10,iconinter, fanart)
	addDir('[COLOR magenta][I]###--Live TV/PPV Below--###[/I][/COLOR]','',0,icon, fanart)
	addDir('[COLOR red]I4ATV Extra[/COLOR] [COLOR yellow][I]>IPTV<[/I][/COLOR]','0',111,icon, fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')

def PassRes():
	if not os.path.exists(passreset):
		dialog.ok(addonname, 'There is no password set please click i4atv extra to set the password')
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		
	if os.path.exists(passreset):
		os.remove(passreset)
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		
def UsrDel():
	if not os.path.exists(usrdata):
		dialog.ok(addonname, 'There is no userdata present for i4atv')
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		
	if os.path.exists(usrdata):
		shutil.rmtree(usrdata)
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		
def Ivue():
	if not os.path.exists(directory):
		dialog.ok(addonname, 'Please makesure you have ivue tv guide installed and you have run it at least once then use this function to enable integration')
		dialog.notification(addonname, 'please install and run ivue tv guide at least once', xbmcgui.NOTIFICATION_ERROR );
	
	if os.path.exists(directory):
		try: 
			os.makedirs(destmw1dir)
		except OSError:
			if not os.path.isdir(destmw1dir):
				raise
			
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/fixer_files/addons.ini", destinaddons)
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/fixer_files/settings.xml", destinsets)
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/http_mw1_iptv66_tv", destinf2)
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/http_mw1_iptv66_tv-genres", destinf1)
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')
	
def Reneg():
	if not os.path.exists(directoryr):
		dialog.ok(addonname, 'Please makesure you have renegades tv guide installed and you have run it at least once then use this function to enable integration')
		dialog.notification(addonname, 'please install and run renegades tv guide at least once', xbmcgui.NOTIFICATION_ERROR );
	
	if os.path.exists(directoryr):
		try: 
			os.makedirs(destmw1dir)
		except OSError:
			if not os.path.isdir(destmw1dir):
				raise
				
		addonsinir = urllib.URLopener()
		addonsinir.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/addons2.ini", destinaddonsr)
		addonsinir = urllib.URLopener()
		addonsinir.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/settings.xml", destinsetsr)
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/http_mw1_iptv66_tv", destinf2)
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/http_mw1_iptv66_tv-genres", destinf1)
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')

def DELETECACHE(url):
    print '###DELETING STANDARD CACHE###'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete KODI Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
    
	addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')
	
def DELETEPACKAGES(url):
    print '###DELETING PACKAGES###'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
                else:
                        pass
            else:
				addDir('[COLOR yellow]*** No Packages To Delete ***[/COLOR]','0',0,icon,'',fanart)
				addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
    except: 
		addDir('[COLOR yellow]*** There Was An Error ***[/COLOR]','0',0,icon,'',fanart)
		addDir('[COLOR yellow]*** All Done Now Press Back ***[/COLOR]','0',0,icon,'',fanart)
    return
	
def RESOLVE(url,name): 
    play=xbmc.Player(GetPlayerCore())
    import urlresolver
    try: play.play(url)
    except: pass
    from urlresolver import common
    dp = xbmcgui.DialogProgress()
    dp.create('[COLORlime]Architects@Work[/COLOR]','Opening %s Now'%(name))
    if dp.iscanceled(): 
        print "[COLORred]STREAM CANCELLED[/COLOR]" # need to get this part working    
        dp.update(100)
        dp.close()
        dialog = xbmcgui.Dialog()
        if dialog.yesno("[B]CANCELLED[/B]", '[B]Was There A Problem[/B]','', "",'Yes','No'):
            dialog.ok("Message Send", "Your Message Has Been Sent")
        else:
	         return
    else:
        try: play.play(url)
        except: pass
        try: ADDON.resolve_url(url) 
        except: pass 
  
def GetContent():
	user = selfAddon.getSetting('username')
	passw = selfAddon.getSetting('password')

	if user == '' or passw == '':
		dialog.ok(addon_id, 'Please be aware that you will get authorization errors if you do remember to open context/settings menu on live i4atv and clear cache then reload if it dont work repeat the process. Please consider making donations to keep this addon alive and you can find the donation link in the settings of this addon. Thank You.')
		dialog.ok(addon_id, 'For the i4atv extra part of the i4atv addon credit should be given to mettlekettle for the code. Thank You!')
		ret = dialog.yesno('I4ATV EXTRA', 'Please enter inside4ndroid for both','','','Cancel','Login')
		if ret == 1:
			keyb = xbmc.Keyboard('', 'Enter Username')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search = keyb.getText()
				username=search
				keyb = xbmc.Keyboard('', 'Enter Password:')
				keyb.doModal()
				if (keyb.isConfirmed()):
					search = keyb.getText()
					password=search
					selfAddon.setSetting('username',username)
					selfAddon.setSetting('password',password)
		else:quit()
	
	user = selfAddon.getSetting('username')
	passw = selfAddon.getSetting('password')
	headers={'VXNlci1BZ2VudA=='.decode('base64'):'QXBhY2hlLUh0dHBDbGllbnQvVU5BVkFJTEFCTEUgKGphdmEgMS40KQ=='.decode('base64'),
			 'Q29udGVudC1UeXBl'.decode('base64'):'YXBwbGljYXRpb24veC13d3ctZm9ybS11cmxlbmNvZGVk'.decode('base64'),
			 'YXBwLXNlc3Npb24='.decode('base64'):'Mjc1ZjI2ZTMyMTcyNmI5YTk5ZThkOTVjM2VmZTg4YWI='.decode('base64'),
			 'Q29ubmVjdGlvbg=='.decode('base64'):'S2VlcC1BbGl2ZQ=='.decode('base64'),
			 'SG9zdA=='.decode('base64'):'dWt0dm5vdy5kZXNpc3RyZWFtcy50dg=='.decode('base64')}
	net.http_POST('aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYvRGVzaVN0cmVhbXMvaW5kZXgyMDIucGhwP3RhZz1sb2dpbiZ1c2VybmFtZT0='.decode('base64')+user+'&password='+passw,'',headers=headers)
	net.http_POST('aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYvRGVzaVN0cmVhbXMvaW5kZXgyMDIucGhwP3RhZz1nZXRfcGFja2FnZV9uYW1l'.decode('base64'),'',headers=headers)
	net.http_POST('aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYvRGVzaVN0cmVhbXMvaW5kZXgyMDIucGhwP3RhZz1nZXRfYW5ub3Vj'.decode('base64'),'',headers=headers)
	net.http_POST('aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYvRGVzaVN0cmVhbXMvaW5kZXgyMDIucGhwP3RhZz1nZXRfcGFja2FnZV9uYW1l'.decode('base64'),'',headers=headers)
	response=net.http_POST('aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYvRGVzaVN0cmVhbXMvaW5kZXgyMDIucGhwP3RhZz1nZXRfYWxsX2NoYW5uZWwmdXNlcm5hbWU9'.decode('base64')+user,'',headers=headers)
	response=response.content.replace('none','Ch')
	channels=json.loads(response)
	return channels

def GetChannels(url):
	channels = GetContent()
	data=channels['channel']
	for item in data:
		name=item['name']
		if name==None:name='Channel'
		thumb=item['img']
		cat=item['cat_id']
		thumb='aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYv'.decode('base64')+thumb
		if url=='0':
			addLink(name,'url',2,thumb,fanart)
		if cat==url:
			addLink(name,'url',2,thumb,fanart)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
	xbmc.executebuiltin('Container.SetViewMode(50)')

def GetStreams(name):
	channels = GetContent()
	data=channels['channel']
	streamname=[]
	streamurl=[]
	streamthumb=[]
	for item in data:
		thumb=item['img']
		if item['name'] == name:			
			streamurl.append( item['stream_url'] )
			streamurl.append( item['stream_url2'] )
			streamurl.append( item['stream_url3'] )
			streamname.append( 'Stream 1' )
			streamname.append( 'Stream 2' )
			streamname.append( 'Stream 3' )
			streamthumb.append( thumb )
			streamthumb.append( thumb )
			streamthumb.append( thumb )		
	select = dialog.select(name,streamname)
	if select == -1:
		return
	else:
		url = streamurl[select]
		iconimage = 'aHR0cDovL3VrdHZub3cuZGVzaXN0cmVhbXMudHYv'.decode('base64')+streamthumb[select]
		ok=True
		liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		xbmc.Player().play(url, liz, False)
		return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				e4=sys.argv[2]
				cleanedparams=e4.replace('?','')
				if (e4[len(e4)-1]=='/'):
						e4=e4[0:len(e4)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]	
		return param
		   
e4=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url=urllib.unquote_plus(e4["url"])
except:pass
try:name=urllib.unquote_plus(e4["name"])
except:pass
try:mode=int(e4["mode"])
except:pass
try:iconimage=urllib.unquote_plus(e4["iconimage"])
except:pass

if mode==None or url==None or len(url)<1:Main()
elif mode==111:GetChannels(url)
elif mode==2:GetStreams(name)
elif mode==9:Ivue()
elif mode==10:Reneg()
elif mode==1000:DELETECACHE(url)
elif mode==1001:DELETEPACKAGES(url)
elif mode==1002:RESOLVE(url,name)
elif mode==1004:PassRes()
elif mode==1006:UsrDel()

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def main():
	if len(online_xml) > 0:	
		add_dir('[COLOR red]PPV Events[COLOR yellow]/[/COLOR]Live Sports[/COLOR]', u_tube, 3004, icon, fanart)
		
def main2():
	if len(online_xml) > 0:
		add_dir('[COLOR red]UFC[/COLOR]', u_tube, 4, iconufc, fanart)
		add_dir('[COLOR red]Boxing[/COLOR]', u_tube, 5, iconboxing, fanart)
		add_dir('[COLOR red]WWE[/COLOR]', u_tube, 6, iconwwe, fanart)
		add_dir('[COLOR red]MISC[/COLOR]', u_tube, 8, iconmisc, fanart)
		add_dir('[COLOR red]UK Leaugue Football[/COLOR]', u_tube, 7, icontna, fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')

def xml_online():			
	content = make_request('https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/old-stuff/pufc.xml')
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def xml_onlineb():			
	contentb = make_request('https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/old-stuff/pboxing.xml')
	match = re.compile(xml_regex).findall(contentb)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def xml_onlinew():			
	contentw = make_request('https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/old-stuff/pwrestle.xml')
	match = re.compile(xml_regex).findall(contentw)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass

def xml_onlinet():
	dialog.ok(addon_id, 'When selecting a game if you get an authorization error keep trying it will eventually work. All games are sky sports only fixtures.')
	contentt = make_request('https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/old-stuff/pfoot.xml')
	match = re.compile(xml_regex).findall(contentt)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass	

def xml_onlinem():			
	contentm = make_request('https://raw.githubusercontent.com/Inside4ndroid/kodi-15/master/old-stuff/pmisc.xml')
	match = re.compile(xml_regex).findall(contentm)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def xml_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if len(thumb) > 0:	
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if len(thumb) > 0:		
			add_link(name, url, 1, thumb, thumb)			
		else:			
			add_link(name, url, 1, icon, fanart)	
	
def play_video(url):
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
		
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)		

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	play_video(url)
	
elif mode == 4:
	xml_online()
	
elif mode == 5:
	xml_onlineb()
	
elif mode == 6:
	xml_onlinew()
	
elif mode == 7:
	xml_onlinet()

elif mode == 8:
	xml_onlinem()
	
elif mode == 3004:
	main2()

def addPortal(portal):

	if portal['url'] == '':
		return;

	url = build_url({
		'mode': 'genres', 
		'portal' : json.dumps(portal)
		});
	
	cmd = 'XBMC.RunPlugin(' + base_url + '?mode=cache&stalker_url=' + portal['url'] + ')';	
	
	li = xbmcgui.ListItem(portal['name'], iconImage=icon,)
	li.addContextMenuItems([ ('Clear Cache', cmd) ]);

	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
	
	
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)


def homeLevel():
	global portal_1, portal_2, portal_3, go;
	
	#todo - check none portal

	if go:
		addPortal(portal_1);
		addPortal(portal_2);
		addPortal(portal_3);
	
		xbmcplugin.endOfDirectory(addon_handle);

def genreLevel():
	
	try:
		data = load_channels.getGenres(portal['mac'], portal['url'], portal['serial'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		
		return;

	data = data['genres'];
		
	url = build_url({
		'mode': 'vod', 
		'portal' : json.dumps(portal)
	});
			
	li = xbmcgui.ListItem('VoD', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
	
	
	for id, i in data.iteritems():

		title 	= i["title"];
		
		url = build_url({
			'mode': 'channels', 
			'genre_id': id, 
			'genre_name': title.title(), 
			'portal' : json.dumps(portal)
			});
			
		if id == '10':
			iconImage = 'OverlayLocked.png';
		else:
			iconImage = 'DefaultVideo.png';
			
		li = xbmcgui.ListItem(title.title(), iconImage=iconImage)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
		

	xbmcplugin.endOfDirectory(addon_handle);

def vodLevel():
	
	try:
		data = load_channels.getVoD(portal['mac'], portal['url'], portal['serial'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;
	
	
	data = data['vod'];
	
		
	for i in data:
		name 	= i["name"];
		cmd 	= i["cmd"];
		logo 	= i["logo"];
		
		
		if logo != '':
			logo_url = portal['url'] + logo;
		else:
			logo_url = 'DefaultVideo.png';
				
				
		url = build_url({
				'mode': 'play', 
				'cmd': cmd, 
				'tmp' : '0', 
				'title' : name.encode("utf-8"),
				'genre_name' : 'VoD',
				'logo_url' : logo_url, 
				'portal' : json.dumps(portal)
				});
			

		li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url)
		li.setInfo(type='Video', infoLabels={ "Title": name })

		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_UNSORTED);
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);
	xbmcplugin.endOfDirectory(addon_handle);

def channelLevel():
	stop=False;
		
	try:
		data = load_channels.getAllChannels(portal['mac'], portal['url'], portal['serial'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;
	
	
	data = data['channels'];
	genre_name 	= args.get('genre_name', None);
	
	genre_id_main = args.get('genre_id', None);
	genre_id_main = genre_id_main[0];
	
	if genre_id_main == '10' and portal['parental'] == 'true':
		result = xbmcgui.Dialog().input('Parental', hashlib.md5(portal['password'].encode('utf-8')).hexdigest(), type=xbmcgui.INPUT_PASSWORD, option=xbmcgui.PASSWORD_VERIFY);
		if result == '':
			stop = True;

	
	if stop == False:
		for i in data.values():
			
			name 		= i["name"];
			cmd 		= i["cmd"];
			tmp 		= i["tmp"];
			number 		= i["number"];
			genre_id 	= i["genre_id"];
			logo 		= i["logo"];
		
			if genre_id_main == '*' and genre_id == '10' and portal['parental'] == 'true':
				continue;
		
		
			if genre_id_main == genre_id or genre_id_main == '*':
		
				if logo != '':
					logo_url = portal['url'] + '/stalker_portal/misc/logos/320/' + logo;
				else:
					logo_url = 'DefaultVideo.png';
				
				
				url = build_url({
					'mode': 'play', 
					'cmd': cmd, 
					'tmp' : tmp, 
					'title' : name.encode("utf-8"),
					'genre_name' : genre_name,
					'logo_url' : logo_url,  
					'portal' : json.dumps(portal)
					});
			

				li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url);
				li.setInfo(type='Video', infoLabels={ 
					'title': name,
					'count' : number
					});

				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li);
		
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_PLAYLIST_ORDER);
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_PROGRAM_COUNT);
		
		
		xbmcplugin.endOfDirectory(addon_handle);

def playLevel():
	
	dp = xbmcgui.DialogProgressBG();
	dp.create('Channel', 'Loading ...');
	
	title 	= args['title'][0];
	cmd 	= args['cmd'][0];
	tmp 	= args['tmp'][0];
	genre_name 	= args['genre_name'][0];
	logo_url 	= args['logo_url'][0];
	
	try:
		if genre_name != 'VoD':
			url = load_channels.retriveUrl(portal['mac'], portal['url'], portal['serial'], cmd, tmp);
		else:
			url = load_channels.retriveVoD(portal['mac'], portal['url'], portal['serial'], cmd);

	
	except Exception as e:
		dp.close();
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;

	
	dp.update(80);
	
	title = title.decode("utf-8");
	
	title += ' (' + portal['name'] + ')';
	
#	li = xbmcgui.ListItem(title, iconImage=logo_url); <modified 9.0.19
	li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=logo_url);
	li.setInfo('video', {'Title': title, 'Genre': genre_name});
	xbmc.Player().play(item=url, listitem=li);
	
	dp.update(100);
	
	dp.close();


mode = args.get('mode', None);
portal =  args.get('portal', None)


if portal is None:
	portal_1 = config.portalConfig('1');
	portal_2 = config.portalConfig('2');
	portal_3 = config.portalConfig('3');	

else:
	portal = json.loads(portal[0]);

#  Modification to force outside call to portal_1 (9.0.19)

	portal_2 = config.portalConfig('2');
	portal_3 = config.portalConfig('3');	

	if not ( portal['name'] == portal_2['name'] or portal['name'] == portal_3['name'] ) :
		portal = config.portalConfig('1');

	

if mode is None:
	homeLevel();

elif mode[0] == 'cache':	
	stalker_url = args.get('stalker_url', None);
	stalker_url = stalker_url[0];	
	load_channels.clearCache(stalker_url, addondir);

elif mode[0] == 'genres':
	genreLevel();
		
elif mode[0] == 'vod':
	vodLevel();

elif mode[0] == 'channels':
	channelLevel();
	
elif mode[0] == 'play':
	playLevel();
	
elif mode[0] == 'server':
	port = addon.getSetting('server_port');
	
	action =  args.get('action', None);
	action = action[0];
	
	dp = xbmcgui.DialogProgressBG();
	dp.create('IPTV', 'Just A Second ...');
	
	if action == 'start':
	
		if server.serverOnline():
			xbmcgui.Dialog().notification(addonname, 'Server already started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO );
		else:
			server.startServer();
			time.sleep(5);
			if server.serverOnline():
				xbmcgui.Dialog().notification(addonname, 'Server started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO );
			else:
				xbmcgui.Dialog().notification(addonname, 'Server not started. Wait one moment and try again. ', xbmcgui.NOTIFICATION_ERROR );
				
	else:
		if server.serverOnline():
			server.stopServer();
			time.sleep(5);
			xbmcgui.Dialog().notification(addonname, 'Server stopped.', xbmcgui.NOTIFICATION_INFO );
		else:
			xbmcgui.Dialog().notification(addonname, 'Server is already stopped.', xbmcgui.NOTIFICATION_INFO );
			
	dp.close();



	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
xbmcplugin.endOfDirectory(plugin_handle)
