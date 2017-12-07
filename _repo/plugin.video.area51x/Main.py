#############################################################
#################### START ADDON IMPORTS ####################
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import os
import re
import sys
import urllib
import urllib2
import urlparse
import webbrowser
import base64
import json
import list


import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon

dialog = xbmcgui.Dialog()


#############################################################
#################### SET ADDON ID ###########################
_addon_id_ = 'plugin.video.area51x'
_self_ = xbmcaddon.Addon(id=_addon_id_)
username = _self_.getSetting('Username')
password = _self_.getSetting('Password')
global username
global password

#############################################################
#################### SET ADDON THEME DIRECTORY ##############
_theme_			= _self_.getSetting('Theme')
_images_		= '/resources/' + _theme_	



baseurl = base64.b64decode('aHR0cDovL2lwdHYtYXJlYS01MS50djoyMDk1Lw==')
auth = ('player_api.php?username=%s&password=%s' %(username,password))

#############################################################
#################### SET ADDON THEME IMAGES #################
Background_Image	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'bgf.gif'))

ButtonbF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'accinfof.gif'))
ButtonbNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'accinfo.gif'))

ButtoncF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'LiveChannelsf.gif'))
ButtoncNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'LiveChannels.gif'))

ButtondF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'VideoOnDemandf.gif'))
ButtondNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'VideoOnDemand.gif'))

ButtoneF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'Settingsf.gif'))
ButtoneNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'Settings.gif'))

ButtonfF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'webf.png'))
ButtonfNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'web.png'))


#############################################################
########## Function To Call That Starts The Window ##########
def MainWindow():

    window = Main('area51x')
    window.doModal()
    del window
    xbmc.executebuiltin("Dialog.Close(busydialog)")

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
        
def openpage(self):
    if myplatform == 'android':
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://area-51-hosting.host' ) )
    else:
        opensite = webbrowser . open('http://area-51-hosting.host')
        
def checksub(self):

    url = baseurl + auth
    link = Get_Data(url)
    data = json.loads(link)
    serveruser = data['user_info']['username']
    substatus = data['user_info']['status']
    expiry = data['user_info']['exp_date']
    dialog.ok('[COLOR green]Area 51 X[/COLOR]','[COLOR white]User Name :: ' + str(serveruser)+ '\nSubscription Status :: ' + str(substatus) + '\nSubscription Exp Date :: ' + str(expiry) + '\n\n[COLOR green]Thank You For Choosing Area 51 X[/COLOR]')
    

myplatform = platform()

def sendtolistlive(self):

    self.close
    list.listwindow('Live')
    
def sendtolistvod(self):

    self.close
    list.listwindow('Vod')

    


#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='area51x'):
        super(Main, self).__init__(title)

        self.setGeometry(1280, 720, 100, 50)

        Background  = pyxbmct.Image(Background_Image)

        self.placeControl(Background, -10, -1, 123, 52)

        self.set_info_controls()

        self.set_active_controls()

        self.set_navigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.button1, lambda:checksub(self))
        self.connect(self.button2, lambda:sendtolistlive(self))
        self.connect(self.button3, lambda:sendtolistvod(self))
        self.connect(self.button4, lambda:_self_.openSettings())
        self.connect(self.button5, lambda:openpage(self))
        self.setFocus(self.button1)

    def set_info_controls(self):
        self.Hello = pyxbmct.Label('', textColor='0xFFF44248', font='font60', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.Hello, -4, 1, 1, 50)

    def set_active_controls(self):
        self.button1 = pyxbmct.Button('',   focusTexture=ButtonbF,   noFocusTexture=ButtonbNF)
        self.placeControl(self.button1, 10, 0,  15, 15)
        
        self.button2 = pyxbmct.Button('',   focusTexture=ButtoncF,   noFocusTexture=ButtoncNF)
        self.placeControl(self.button2, 30, 0,  15, 15)
        
        self.button3 = pyxbmct.Button('',   focusTexture=ButtondF,   noFocusTexture=ButtondNF)
        self.placeControl(self.button3, 50, 0,  15, 15)
        
        self.button4 = pyxbmct.Button('',   focusTexture=ButtoneF,   noFocusTexture=ButtoneNF)
        self.placeControl(self.button4, 70, 0,  13, 13)
        
        self.button5 = pyxbmct.Button('',   focusTexture=ButtonfF,   noFocusTexture=ButtonfNF)
        self.placeControl(self.button5, 101, 0,  8, 12)



    def set_navigation(self):
        #set the navigation for if user presses Right when eliment if focused
        self.button1.controlDown(self.button2)
        self.button2.controlDown(self.button3)
        self.button3.controlDown(self.button4)
        self.button4.controlDown(self.button5)
        self.button5.controlDown(self.button1)
        
        self.button1.controlUp(self.button5)
        self.button2.controlUp(self.button1)
        self.button3.controlUp(self.button2)
        self.button4.controlUp(self.button3)
        self.button5.controlUp(self.button4)
        
      
        
        
