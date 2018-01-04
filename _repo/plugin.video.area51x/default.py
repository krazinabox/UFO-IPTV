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
    

def checkuser():

    if username =='' or password =='':
        dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR green]Welcome New User, Please Enter Your Login Details then click ok[/COLOR]")
        _self_.openSettings()
        dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR red]Thank You, Please Re Launch Addon[/COLOR]")
        quit()
    else:
        checksubstatus()
    

def checksubstatus():

    username = _self_.getSetting('Username')
    password = _self_.getSetting('Password')
    url = baseurl + ('player_api.php?username=%s&password=%s' %(username,password))
    link = Get_Data(url)
    try:
        data = json.loads(link)
        serveruser = data['user_info']['username']
        expiry = data['user_info']['exp_date']
        try:
            Main.MainWindow()
        except:
            dialog.ok("[COLOR green]Area 51 X[/COLOR]","[COLOR red]Add on Failed To Run Contact Support[/COLOR]")
    except:
        dialog.ok("[COLOR red]Details Incorrect Or Sub Expired[/COLOR]","[COLOR green]Current User Name Entered : [COLOR white]" + username + "[/COLOR]\n[COLOR green]Current Password Entered : [COLOR white]" + password + "[/COLOR]\n\n[COLOR red]If You think this is wrong, screen-shot this window and send to support[/COLOR]")
        _self_.setSetting('Username', '')
        _self_.setSetting('Password', '')
        quit()

      
checkuser()
