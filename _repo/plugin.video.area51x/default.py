#############################################################
#################### START ADDON IMPORTS ####################
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import time

import os
import re
import sys
import Main
from datetime import datetime
from datetime import timedelta
import base64
import urllib
import urllib2
import json
import time
import webbrowser
import autoexec

import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon

dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
oldaddon = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.area51')


#############################################################
#################### SET ADDON ID ###########################
_addon_id_  = 'plugin.video.area51x'
_self_  = xbmcaddon.Addon(id=_addon_id_)
addon   = Addon(_addon_id_, sys.argv)

username = _self_.getSetting('Username')
password = _self_.getSetting('Password')

baseurl = base64.b64decode('aHR0cDovL2lwdHYtYXJlYS01MS50djoyMDk1Lw==')
auth = ('player_api.php?username=%s&password=%s' %(username,password))


def Get_Data(url):

    req = urllib2.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
    response = urllib2.urlopen(req, timeout=30)
    data = response.read()
    response.close()

    return data
    
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

myplatform = platform()

def openpage():
    if myplatform == 'android':
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://area-51-hosting.host' ) )
    else:
        opensite = webbrowser . open('http://area-51-hosting.host')

def checkuser():

    if username =='':
        dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR green]Welcome New User, Please Enter Your Login Details[/COLOR]")
        user =''
        keyboard = xbmc.Keyboard(user, '[COLOR green]Enter User Name[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            user = keyboard.getText()
            if len(user)>=1:
                _self_.setSetting('Username', user)
            else:
                quit()
    if password =='':
        passw =''
        keyboard = xbmc.Keyboard(passw, '[COLOR green]Enter Password[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            passw = keyboard.getText()
            if len(passw)>=1:
                _self_.setSetting('Password', passw)
                dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR green]Thank you, Please Re-Open Addon and Enjoy[/COLOR]")
                quit()
            else:
                quit()
    

def checksubstatus():

    username = _self_.getSetting('Username')
    password = _self_.getSetting('Password')
    url = baseurl + ('player_api.php?username=%s&password=%s' %(username,password))
    link = Get_Data(url)
    try:
        data = json.loads(link)
        serveruser = data['user_info']['username']
        expiry = data['user_info']['exp_date']
        if expiry == None:
            Main.MainWindow()
        else:
            d = int(expiry[:10])
            expiry = datetime.fromtimestamp(d).strftime('%Y-%m-%d')
            start = datetime.strptime(expiry, "%Y-%m-%d")
            end = start - timedelta(days=3)
            now = time.strftime("%Y-%m-%d")
            now = datetime.strptime(now, "%Y-%m-%d")
            if now in (start,end):
                source = dialog.select("[COLOR red]Sub Almost Expired[/COLOR]", ['[COLOR green]Renew Sub[/COLOR]', '[COLOR red]Continue[/COLOR]'])
                if source ==0:
                    openpage()
                elif source ==1:
                    Main.MainWindow()
                else:
                    Main.MainWindow()
            else:
                Main.MainWindow()
    except:
        source = dialog.select("[COLOR red]It Seems Your User or Password Is Wrong, Or Your Sub Has Expired[/COLOR]", ['[COLOR green]Renew Sub[/COLOR]', '[COLOR red]Quit[/COLOR]'])
        if source ==0:
            _self_.setSetting('Username', '')
            _self_.setSetting('Password', '')
            openpage()
            quit()
        elif source ==1:
            _self_.setSetting('Username', '')
            _self_.setSetting('Password', '')
            quit()
        else:
            quit()
            
def clearup():

    cachePath     = xbmc.translatePath(os.path.join('special://home/cache'))
    thumbPath     = xbmc.translatePath(os.path.join('special://profile/Thumbnails'))
    packcagesPath = xbmc.translatePath(os.path.join('special://home/addons/packages'))
    
    i =[(cachePath,'Cache'),(thumbPath,'Thumbnails'),(packcagesPath,'Packages')]
    for r in i:
        for root,dirs,files in os.walk(r[0]):
            for f in files:
                if (f.endswith('.log')): continue
                try: os.unlink(os.path.join(root, f))
                except: pass
    xbmc.executebuiltin('Container.Refresh')
    
def Remove_Old():

    try:
        addontoremove = ['plugin.video.area51']
        approve = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in addontoremove)
        if approve:
            #dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR red]You Still Have The Old Area 51 Installed\nYou No Longer Need this\nClick Ok To Remove It[/COLOR]")
            import shutil
            shutil.rmtree(oldaddon)
            xbmc.executebuiltin('Container.Refresh')
    except: pass
def START():

    clearup()
    
    checkuser()
    checksubstatus()
    try:
        Main.MainWindow()
    except (RuntimeError, SystemError):
        pass
Remove_Old()
START()