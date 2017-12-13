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
import Main
import urlresolver


import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon

dialog = xbmcgui.Dialog()



#############################################################
#################### SET ADDON ID ###########################
_addon_id_	= 'plugin.video.guit'
_self_			= xbmcaddon.Addon(id=_addon_id_)

#############################################################
#################### SET ADDON THEME DIRECTORY ##############
_theme_			= _self_.getSetting('Theme')
_images_		= '/resources/' + _theme_	

#############################################################
#################### SET ADDON THEME IMAGES #################
Background_Image	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'background.png'))
Logo_Image = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'logo.png'))
Addon_Image = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'addon.png'))
Listbg = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'listbg.png'))
ButtonbF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'b2.gif'))
ButtonbNF = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'b1.gif'))

########## Function To Call That Starts The Window ##########
def nflwindow(ta):
    global data
    global List
    
    data = ta
    
    window = nfl_window('guit')
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

def passed(self, title):

    global Item_Title
    global Item_Link
    global Item_Desc
    global Item_Icon

    Item_Title =  []
    Item_Link  =  []
    Item_Desc  =  []
    Item_Icon  =  []
    
    title = title.upper()
    Item_Title.append('[COLOR red]Main ' + title + ' List[/COLOR]')
    Item_Link.append('')
    Item_Desc.append('Welcome')
    Item_Icon.append(Addon_Image)
    self.List.addItem('[COLOR red]Main ' + title + ' List[/COLOR]')
    self.textbox.setText('Welcome')
    self.Show_Logo.setImage(Addon_Image)
    
    regex = ("<item>\s+<title>(.*?)<\/title>\s+<link>(.*?)<\/link>\s+<description>(.*?)<\/description>\s+<icon>(.*?)<\/icon>\s+<\/item>")
    
    
    if 'NFL' in title:
        List_Data = Get_Data('https://www.dropbox.com/s/nmq8n8ew52ujm8u/dstest.xml?dl=1')
    elif 'nba' in title:
        pass
    elif 'MLB' in title:
        List_Data = Get_Data('https://pastebin.com/raw/pYQHDYTP')
    elif 'boxing' in title:
        pass
    elif 'footie' in title:
        pass
    elif 'nascar' in title:
        pass
    elif 'ufc' in title:
        pass
    elif 'wwe' in title:
        pass
    
    
    List_Items = re.findall(regex, List_Data ,re.DOTALL)
    
    for Item in List_Items:
        Item_Title.append(Item[0])
        Item_Link.append(Item[1])
        Item_Desc.append(Item[2])
        Item_Icon.append(Item[3])
        self.List.addItem(Item[0])
        
def List_Selected(self):

    Show_List  =  xbmcgui.ListItem(Media_Title, iconImage=Media_Icon,thumbnailImage=Media_Icon)
    xbmc.Player().play(Media_Link, Show_List, False)



#############################################################
######### Class Containing the GUi Code / Controls ##########
class nfl_window(pyxbmct.AddonFullWindow):

    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='guit'):
        super(nfl_window, self).__init__(title)

        self.setGeometry(1280, 720, 100, 50)

        Background  = pyxbmct.Image(Background_Image)

        self.placeControl(Background, -10, -1, 123, 52)
        
        Logo  = pyxbmct.Image(Logo_Image)

        self.placeControl(Logo, -1, 4, 10, 20)

        self.set_info_controls()

        self.set_active_controls()

        self.set_navigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.List, lambda:List_Selected(self))
        
        passed(self, data)
        self.setFocus(self.List)

    def set_info_controls(self):
        self.Hello = pyxbmct.Label('', textColor='0xFFF44248', font='font60', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.Hello, -4, 1, 1, 50)

        self.textbox = pyxbmct.TextBox(textColor='0xFFFFFFFF')
        self.placeControl(self.textbox, 70, 33, 30, 13)

        self.Show_Logo = pyxbmct.Image('')
        #self.placeControl(self.Show_Logo, 15, 32, 50, 14)
        self.placeControl(self.Show_Logo, 14, 33, 50, 12)

    def set_active_controls(self):
        self.List =	pyxbmct.List(buttonFocusTexture=Listbg,_space=9,_itemTextYOffset=-7,textColor='0xFF3E4349')
        self.placeControl(self.List, 15, 3, 91, 23)
        
        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.List_update)


    def set_navigation(self):
        pass
    
    def List_update(self):
        global Media_Title
        global Media_Link
        global Media_Desc
        global Media_Icon

        try:
            if self.getFocus() == self.List:
            
                position = self.List.getSelectedPosition()
                
                Media_Title = Item_Title[position]
                Media_Link  = Item_Link[position]
                Media_Desc = Item_Desc[position]
                
                self.textbox.setText(Media_Desc)
                self.textbox.autoScroll(1000, 1000, 1000)
                
                if Item_Icon[position] is not None:
                    Media_Icon = Item_Icon[position]
                    self.Show_Logo.setImage(Media_Icon)
                else:
                    Media_Icon = 'http://via.placeholder.com/300x220/13b7ff/FFFFFF?text=' + Media_Title
                    self.Show_Logo.setImage(Media_Icon)
                    
        except (RuntimeError, SystemError):
            pass
