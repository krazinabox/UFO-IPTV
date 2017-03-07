import urllib,urllib2, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, re
import common,xbmcvfs,zipfile,downloader,extract
import GoDev
from datetime import datetime, timedelta
import base64, time
AddonID = 'plugin.video.area51'
Addon = xbmcaddon.Addon(AddonID)
ADDON = xbmcaddon.Addon(id='plugin.video.area51')
fanart = "ZmFuYXJ0LmpwZw=="
Username=xbmcplugin.getSetting(int(sys.argv[1]), 'Username')
Password=xbmcplugin.getSetting(int(sys.argv[1]), 'Password')
ServerURL = "http://server.iptv-area-51.tv:2095/get.php?username=%s&password=%s&type=m3u&output=hls"%(Username,Password,)
AccLink = "http://server.iptv-area-51.tv:2095/panel_api.php?username=%s&password=%s"%(Username,Password,)
addonDir = Addon.getAddonInfo('path').decode("utf-8")
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources/'));
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
    os.makedirs(addon_data_dir)
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
def Open_URL(AccLink):
        req = urllib2.Request(url)
        #req.add_header('User-Agent' , "Magic Browser")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link		
def MainMenu():
        AddDir('My Account',AccLink,1,Images + 'MyAcc.png')
        AddDir('Live TV','url',2,Images + 'Live TV.png')
        AddDir('Movies (Coming Soon)','Movies',8,Images + 'movies.png')
        AddDir('TVShows (Coming Soon)','TVshows',9,Images + 'tvshows.png')
        AddDir('Extras','Extras',5,Images + 'extras.png')
        AddDir('Clear Cache','Clear Cache',7,Images + 'cache.png')
        AddDir('Settings','settings',4,Images + 'settings.png')
def LiveTv(url):
    list = common.m3u2list(ServerURL)
    for channel in list:
        name = common.GetEncodeString(channel["display_name"])
        AddDir(name ,channel["url"], 3, iconimage, isFolder=False)
def MyAccDetails(url):
        link = Open_URL(url)
        match=re.compile('"username":"(.+?)"').findall(link)
        match1=re.compile('"status":"(.+?)"').findall(link)
        match2=re.compile('"exp_date":"(.+?)"').findall(link) 	
        match3=re.compile('"active_cons":"(.+?)"').findall(link)
        match4=re.compile('"created_at":"(.+?)"').findall(link)
        match5=re.compile('"max_connections":"(.+?)"').findall(link)
        match6=re.compile('"is_trial":"1"').findall(link)
        for url in match:
                AddAccInfo('My Account Information','','',Images +'MyAcc.png')
                AddAccInfo('Username:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match1:
                AddAccInfo('Status:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match4:
                dt = datetime.fromtimestamp(float(match4[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Created:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match2:
                dt = datetime.fromtimestamp(float(match2[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Expires:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match3:
                AddAccInfo('Active Connection:  %s'%(url),'','',Images +'MyAcc.png')
        for url in match5:
                AddAccInfo('Max Connection:  %s'%(url),'','',Images +'MyAcc.png') 
        for url in match6:
                AddAccInfo('Trial: Yes','','',Images +'MyAcc.png')
	     
def PlayUrl(name, url, iconimage=None):
        _NAME_=name
        list = common.m3u2list(ServerURL)
        for channel in list:
            name = common.GetEncodeString(channel["display_name"])
            stream=channel["url"]
            if _NAME_ in name:
                listitem = xbmcgui.ListItem(path=stream, thumbnailImage=iconimage)
                listitem.setInfo(type="Video", infoLabels={ "Title": name })
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)				
def AddAccInfo(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)				
def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    a=sys.argv[0]+"?url=None&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    #print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+a
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
def Get_Params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0].lower()] = splitparams[1]
    return param
	
def correctPVR():

	area51 = xbmcaddon.Addon('plugin.video.area51')
	username_text = area51.getSetting(id='Username')
	password_text = area51.getSetting(id='Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = "http://server.iptv-area-51.tv:2095/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u&output=mpegts"
	EPGurl     = "http://server.iptv-area-51.tv:2095/xmltv.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	choice = xbmcgui.Dialog().ok("[COLOR white]PVR SETUP DONE[/COLOR]",'[COLOR white]We\'ve copied your AREA 51 to the PVR Guide[/COLOR]',' ','[COLOR white]This includes the EPG please allow time to populate now click launch PVR[/COLOR]')
	

def LaunchPVR():
	xbmc.executebuiltin('ActivateWindow(TVGuide)')
	
def OpenSettings():
    ADDON.openSettings()
    MainMenu()	
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear your Cache?', 'If you still cant see your account after ok button is clicked your details are incorrect', nolabel='Cancel',yeslabel='OK')
    if choice == 1:
        GoDev.Wipe_Cache()

def wizard2(name,url,description,showcontext=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
def playXml(url):
        xbmc.executebuiltin('PlayMedia(%s)' % url)
	
def wizard3():
	dialog = xbmcgui.Dialog()
	path = xbmc.translatePath( 'special://home/addons/plugin.video.ottalpha-3.0/' )
	d = os.listdir(path)
	if 'plugin.video.testpiece' in d:
		xbmc.executebuiltin('RunAddon(plugin.video.testpiece)')
	else:
		dialog.ok('Not Installed','You need ivue guide in order to use this')

def addXMLMenu(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def ExtraMenu():
    link = OPEN_URL('http://matsbuilds.uk/jack/SportsCatchUp/football.txt').replace('\n','').replace('\r','')  #Spaf
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,FanArt,description in match:
        addXMLMenu(name,url,13,iconimage,FanArt,description)
def Movies():
	dialog = xbmcgui.Dialog()
	path = xbmc.translatePath( 'special://home/addons' )
	d = os.listdir(path)
	if 'plugin.program.fixtures' in d:
		xbmc.executebuiltin('RunAddon(plugin.program.fixtures)')
	else:
		dialog.ok('Not Installed','You need extended info to use this')

def TVShows():
	dialog = xbmcgui.Dialog()
	path = xbmc.translatePath( 'special://home/addons' )
	d = os.listdir(path)
	if 'plugin.program.mtvguidepro' in d:
		xbmc.executebuiltin('RunAddon(plugin.program.mtvguidepro)')
	else:
		dialog.ok('Not Installed','You need mayfair pro guide in order to use this you can get it from here http://mayfairguides.com/pro')

def gettextdata(url):
    mayfair_show_busy_dialog()
    try:
        req = urllib2.Request(url)
        reqq = urllib2.urlopen(req)
        data = reqq.read()
        reqq.close()
        mayfair_hide_busy_dialog()
        if data == '':
            data = 'No message to display, please check back later!'
        return data
    except:
        import sys
        import traceback as tb
        (etype, value, traceback) = sys.exc_info()
        tb.print_exception(etype, value, traceback)
        mayfair_hide_busy_dialog()
        dialog = xbmcgui.Dialog()
        dialog.ok("Error!","Error connecting to server!","","Please try again later.")

def mayfair_show_busy_dialog():
    xbmc.executebuiltin('ActivateWindow(10138)')

def mayfair_hide_busy_dialog():
    xbmc.executebuiltin('Dialog.Close(10138)')
    while xbmc.getCondVisibility('Window.IsActive(10138)'):
        xbmc.sleep(100)

		


params=Get_Params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url = urllib.unquote_plus(params["url"])
except:pass
try:name = urllib.unquote_plus(params["name"])
except:pass
try:iconimage = urllib.unquote_plus(params["iconimage"])
except:pass
try:mode = int(params["mode"])
except:pass
try:description = urllib.unquote_plus(params["description"])
except:pass

if mode == 7:
	Clear_Cache()
elif mode == 8:
	Movies()
elif mode == 9:
	TVShows()
elif mode == 1:
    MyAccDetails(url)
elif mode == 2:
    LiveTv(url)
elif mode == 3:
    PlayUrl(name, url, iconimage)
elif mode == 4:
	OpenSettings()
elif mode == 5:
	ExtraMenu()
elif mode == 6:
	wizard2(name,url,description)
elif mode == 10:
	wizard3()
elif mode == 11:
	correctPVR()
elif mode == 12:
	LaunchPVR()
elif mode == 13:
	playXml(url)