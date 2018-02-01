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
import list2
import time
import datetime


import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon

dialog = xbmcgui.Dialog()


#############################################################
#################### SET ADDON ID ###########################
_addon_id_ = 'plugin.video.area51x'
_self_ = xbmcaddon.Addon(id=_addon_id_)
username = _self_.getSetting('Username')
password = _self_.getSetting('Password')
Date = time.strftime("%d/%m")
AddonTitle = '[COLOR green]Area 51 X[/COLOR]'
dp = xbmcgui.DialogProgress()
global username
global password

#############################################################
#################### SET ADDON THEME DIRECTORY ##############
_theme_			= _self_.getSetting('Theme')
_images_		= '/resources/' + _theme_	



baseurl = base64.b64decode('aHR0cDovL2lwdHYtYXJlYS01MS50djoyMDk1Lw==')
auth = ('player_api.php?username=%s&password=%s' %(username,password))
pvrsettings	= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))

#############################################################
#################### SET ADDON THEME IMAGES #################
Background_Image	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'bg.jpg'))
LOGO	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'area51.png'))
ButtonAccount = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'accountF.png'))
ButtonAccountNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'account.png'))
ButtonLive = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'liveF.png'))
ButtonLiveNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'live.png'))
ButtonSettings = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'settingsF.png'))
ButtonSettingsNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'settings.png'))
ButtonVOD = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vodF.png'))
ButtonVODNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vod.png'))
ButtonExit = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'exitF.png'))
ButtonExitNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'exit.png'))
ButtonWebsite = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'websiteF.png'))
ButtonWebsiteNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'website.png'))
ButtonAPK = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'androidF.png'))
ButtonAPKNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'android.png'))
ButtonPVR = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'pvrF.png'))
ButtonPVRNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'pvr.png'))



#############################################################
########## Function To Call That Starts The Window ##########
def MainWindow():

    window = Main('area51x')
    window.doModal()
    del window

def Get_Data(url):

    req = urllib2.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
    response = urllib2.urlopen(req, timeout=30)
    data = response.read()
    response.close()

    return data
    
def tick(self):

    self.DATE.setLabel("Today " + str(Date))
    
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
        
def installandroid(proc):
    xbmc.executebuiltin(proc)
        
def apkinstall(self):

    if myplatform == 'android':
        url = 'http://theuforepo.us/repo/Area-51.apk'
        HOME = xbmc.translatePath(os.path.join('special://home'))
        dialog.ok(AddonTitle,"[COLOR yellow]Please Choose Where To Save File To\n[COLOR green]( We Recommend Downloads Folder )[/COLOR]")
        saveto = dialog.browse(3, AddonTitle, 'files', '', False, False, HOME)
        file_name = 'UFO.apk'
        completeName = os.path.join(saveto,file_name)
        dp.create (AddonTitle,"[COLOR green]Sending Download Request[/COLOR]")
        dp.update(0)
        u = urllib2.urlopen(url)
        dp.update (25,"[COLOR green]Sending Download Request[/COLOR]")
        f = urllib.urlretrieve(url,completeName)
        dp.update (50,"[COLOR green]Request Accepted[/COLOR]")
        meta = u.info()
        dp.update (75,"[COLOR green]Housekeeping[/COLOR]")
        file_size = int(meta.getheaders("Content-Length")[0])
        dp.update (100,"[COLOR green]Starting Download[/COLOR]")
        time.sleep(2)
        dp.create (AddonTitle,"Starting Download: %s File Size: %s" % (file_name, file_size))
        dp.update(0)
        if dp.iscanceled():
            sys.exit()
        file_size_dl = 0
        block_sz = 12000
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            if dp.iscanceled():
                sys.exit()
            file_size_dl += len(buffer)
            status = "[%3.2f%%]" % (file_size_dl*100./file_size)
            status = status + chr(8)*(len(status)+1)
            dp.update (file_size_dl,"[COLOR green]Downloaded [COLOR yellow]%s[/COLOR][COLOR green] Of %s[/COLOR]"%(status,file_name))
        dialog.ok(AddonTitle,"[COLOR limegreen]" + file_name + " Downloaded[/COLOR]")
        yes = dialog.yesno(AddonTitle, "[COLOR limegreen]Would you like to install now?:[/COLOR]",)
        if yes == 1:
            dp.close()
            installandroid('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+completeName+'")')
        if yes == 0:
            dialog.ok(AddonTitle,"[COLOR limegreen]Ok Please Install Manually From The Folder You Saved Download To[/COLOR]")
            dp.close()
            exit()
    else:
        dialog.notification(AddonTitle, '[COLOR yellow]Sorry This Is Only For Android Devices[/COLOR]', LOGO, 3500)
        
def openpage(self):
    if myplatform == 'android':
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://area-51-hosting.host' ) )
    else:
        opensite = webbrowser . open('http://area-51-hosting.host')
        
def pvr(self):

    try:
        set = open(pvrsettings).read().replace('\n', '').replace('\r','').replace('\t','')
        check = re.compile ('<setting id="epgUrl" value="(.*?)" \/>').findall(set)[0]
        if len(check) <= 1:
            jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
            IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
            nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
            loginurl   = "http://iptv-area-51.tv:2095/get.php?username=" + username + "&password=" + password + "&type=m3u_plus&output=ts"
            EPGurl     = "http://iptv-area-51.tv:2095/xmltv.php?username=" + username + "&password=" + password + "&type=m3u_plus&output=ts"

            xbmc.executeJSONRPC(jsonSetPVR)
            xbmc.executeJSONRPC(IPTVon)
            xbmc.executeJSONRPC(nulldemo)

            sexyaddon = xbmcaddon.Addon('pvr.iptvsimple')
            dialog.ok("[COLOR green]Area 51 X[/COLOR]","Please click ok each time it says PVR needs to restart, It will say this 4 times")
            sexyaddon.setSetting(id='m3uUrl', value=loginurl)
            sexyaddon.setSetting(id='epgUrl', value=EPGurl)
            sexyaddon.setSetting(id='m3uCache', value="false")
            sexyaddon.setSetting(id='epgCache', value="false")
            killkodi()
            
        else:
            dialog.ok('[COLOR green]Area 51 X PVR[/COLOR]','[COLOR white]PVR Already Setup[/COLOR]')
        
    except:
        dialog.ok('[COLOR green]Area 51 X PVR[/COLOR]','[COLOR white]PVR Import Failed, Is PVR Client Enabled?[/COLOR]')
def killkodi():
    dialog.ok("[COLOR green]Area 51 X[/COLOR]","PVR Client Updated, Kodi needs to re-launch for changes to take effect, click ok to quit kodi and then please re launch")
    os._exit(1)
def checksub(self):

    url = baseurl + auth
    link = Get_Data(url)
    data = json.loads(link)
    serveruser = data['user_info']['username']
    substatus = data['user_info']['status']
    expiry = data['user_info']['exp_date']
    #try:
    expiry = datetime.datetime.fromtimestamp(int(expiry)).strftime('%Y-%m-%d %H:%M')
    #except:
        #expiry = 'Unkown Expiry Date'
    dialog.ok('[COLOR green]Thank You For Choosing Area 51 X[/COLOR]','User Name :: ' + str(serveruser)+ '\nSubscription Status :: ' + str(substatus) + '\nSubscription Exp Date :: ' + str(expiry))
    

myplatform = platform()

def sendtolistlive(self):

    #self.close
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
        Logo        = pyxbmct.Image(LOGO)

        self.placeControl(Background, -10, -1, 123, 52)
        self.placeControl(Logo, 2, 15, 16, 20)

        self.set_info_controls()

        self.set_active_controls()

        self.set_navigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        tick(self)
        self.connect(self.button1, lambda:checksub(self))
        self.connect(self.button7, lambda:apkinstall(self))
        self.connect(self.button2, lambda:sendtolistlive(self))
        self.connect(self.button4, lambda:sendtolistvod(self))
        self.connect(self.button3, lambda:_self_.openSettings())
        self.connect(self.button6, lambda:openpage(self))
        self.connect(self.button8, lambda:pvr(self))
        self.connect(self.button5, self.close)
        self.setFocus(self.button1)

    def set_info_controls(self):
        self.Hello = pyxbmct.Label('', textColor='0xFFF44248', font='font60', alignment=pyxbmct.ALIGN_CENTER)
        #self.TIME =  pyxbmct.Label('',textColor='0xFFFFFFFF', font='font14')
        self.DATE =  pyxbmct.Label('',textColor='0xFFFFFFFF', font='font18')
        self.placeControl(self.Hello, -4, 1, 1, 50)
        self.placeControl(self.DATE,  -9, 46, 12, 15)
        #self.placeControl(self.TIME,  -9, 46, 12, 15)
        

    def set_active_controls(self):
        #pass
        self.button1 = pyxbmct.Button('',   focusTexture=ButtonAccount,   noFocusTexture=ButtonAccountNF)
        self.placeControl(self.button1, 30, 6,  40, 8)
        
        self.button2 = pyxbmct.Button('',   focusTexture=ButtonLive,   noFocusTexture=ButtonLiveNF)
        self.placeControl(self.button2, 30, 16,  40, 8)
        
        self.button3 = pyxbmct.Button('',   focusTexture=ButtonSettings,   noFocusTexture=ButtonSettingsNF)
        self.placeControl(self.button3, 30, 26,  40, 8)
        
        self.button4 = pyxbmct.Button('',   focusTexture=ButtonVOD,   noFocusTexture=ButtonVODNF)
        self.placeControl(self.button4, 30, 36,  40, 8)
        
        self.button5 = pyxbmct.Button('',   focusTexture=ButtonExit,   noFocusTexture=ButtonExitNF)
        self.placeControl(self.button5, 86, 44,  25, 6)
        
        self.button6 = pyxbmct.Button('',   focusTexture=ButtonWebsite,   noFocusTexture=ButtonWebsiteNF)
        self.placeControl(self.button6, 90, 21,  10, 8)
        
        self.button7 = pyxbmct.Button('',   focusTexture=ButtonAPK,   noFocusTexture=ButtonAPKNF)
        self.placeControl(self.button7, 101, 21,  10, 8)
        
        self.button8 = pyxbmct.Button('',   focusTexture=ButtonPVR,   noFocusTexture=ButtonPVRNF)
        self.placeControl(self.button8, 86, 0,  25, 6)



    def set_navigation(self):
        #tick(self)
        self.button1.controlRight(self.button2)
        self.button2.controlRight(self.button3)
        self.button3.controlRight(self.button4)
        self.button4.controlRight(self.button1)
        
        self.button1.controlDown(self.button6)
        self.button2.controlDown(self.button6)
        self.button3.controlDown(self.button6)
        self.button4.controlDown(self.button6)
        
        self.button6.controlUp(self.button1)
        self.button6.controlDown(self.button7)
        self.button6.controlLeft(self.button8)
        self.button6.controlRight(self.button5)
        self.button5.controlLeft(self.button6)
        self.button8.controlRight(self.button6)
        self.button7.controlRight(self.button5)
        self.button7.controlLeft(self.button8)
        self.button7.controlUp(self.button6)
        
        self.button1.controlLeft(self.button4)
        self.button2.controlLeft(self.button1)
        self.button3.controlLeft(self.button2)
        self.button4.controlLeft(self.button3)
        # self.button5.controlDown(self.button1)
        
        # self.button1.controlUp(self.button5)
        # self.button2.controlUp(self.button1)
        # self.button3.controlUp(self.button2)
        # self.button4.controlUp(self.button3)
        # self.button5.controlUp(self.button4)
        
        # self.button5.controlRight(self.button6)
        # self.button6.controlLeft(self.button5)
        