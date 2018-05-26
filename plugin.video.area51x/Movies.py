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
import json
import base64
import xml.etree.ElementTree as ET
import random
import Live
import datetime

import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon


#############################################################
#################### SET ADDON ID ###########################
_addon_id_	= 'plugin.video.area51x'
_self_		= xbmcaddon.Addon(id=_addon_id_)
addon		= Addon(_addon_id_, sys.argv)

#SET THE DEFAULT FOLDER FOR SKIN IMAGES
_images_	= '/resources/Red/'

#SET DIALOG TO = XBMCGUI DIALOG FUNCTION
Dialog = xbmcgui.Dialog()

#GET SOME NEEDED INFORMATION FROM ADDON SETTINGS

_BASE_ = 'http://'+ _self_.getSetting('Server')
_PORT_ = _self_.getSetting('Port')
_USERNAME_ = _self_.getSetting('Username')
_PASSWORD_ = _self_.getSetting('Password')
_TMDB_KEY_ = _self_.getSetting('Tmdb')
pvrsettings	= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))

#############################################################
#################### SET ADDON THEME IMAGES #################
Skin_Path = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_))
Icon			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_, 'Icon.png'))
FanArt			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_, 'Fanart.png'))
Background_Image	= xbmc.translatePath(os.path.join(Skin_Path, 'Background.png'))
Vert_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vertical.png'))
Hori_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'horizontal.png'))
Header_bg		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'header-back.png'))
Nav_bg			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'nav.png'))
Guide_img		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tv-guide.png'))
Guide_img_selected		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tv-guide-selected.png'))
Logo_img		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'logo-settings.png'))
Focused_Button	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'nav-selected.png'))
List_bg			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vod-list-bg.png'))
List_vod_bg			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-vod-bg.png'))
List_Focused	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected.png'))
List_vod_Focused	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-vod-selected.png'))
List_vod_no	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-vod.png'))
List_Focused_default	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected-default.png'))
Body_bg		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vod_bavkground.png'))
Body_bg_cats		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vod_bavkground_cats.png'))
Body_bg_all		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vod_bavkground_all.png'))
Arrow_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'arrow.png'))
tvshows		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tvshows.png'))
tvshows_un	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tvshows_un.png'))
movies		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'movies.png'))
movies_un	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'movies_un.png'))
catchup	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'catchup.png'))
catchup_un	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'catchup_un.png'))
search_bg	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'search_bg.png'))
Search_Button_Selected	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'Search_Button_Selected.png'))
Search_Button	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'Search_Button.png'))

DEFAULT_POSTER = xbmc.translatePath(os.path.join(Skin_Path, 'POSTER.jpg'))
PLAY_IMG = xbmc.translatePath(os.path.join(Skin_Path, 'play.png'))
PLAY_SEL = xbmc.translatePath(os.path.join(Skin_Path, 'play-sel.png'))
#############################################################
########## Function To Call That Starts The Window ##########
def MoviesWindow():
	
    window = Movies('area51x')
    window.doModal()
    del window

#####

def Get_Data(URL):

	# USE URLLIB2 FOR ALL WEB REQUESTS WITH THE MOZILLA USER AGENT
    req = urllib2.Request(URL)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
    response = urllib2.urlopen(req, timeout=30)
    data = response.read()
    response.close()

    return data
	
def open_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	req.add_header('Cookie', '__cfduid=dda1ead87c709cf4d3efd163fad9c9d131514228642; _ga=GA1.2.1262571518.1514228645; _gid=GA1.2.1997995054.1517178040; PHPSESSID=m1puvsf3mul1u9vmmpbsk7hlb1')
	response = urllib2.urlopen(req, timeout=10)
	link=response.read()
	response.close()
	link = link.replace('\n', '').replace('\r','').replace('\t','')
	return link
	
def find_single_match(text,pattern):

	# USE RE TO FIND THE PATTERN THAT IS A SINGLE MATCH TO OUR REGEX
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result
	
def find_multiple_matches(text,pattern):
    
	# USE RE TO FIND ALL PATTERNS THAT MATCH OUT REGEX
    matches = re.findall(pattern,text,re.DOTALL)

    return matches
	
def find_match_from(text, from_string, to_string, excluding=True):
    if excluding:
        try:
            r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
        except:
            r = ''
    else:
        try:
            r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
        except:
            r = ''
    return r


def find_all_matches(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	
def Get_Catchup(self):
	
	HIDE_RAND(self)
	
	global vod_ids
	global vod_cats

	vod_cats	= []
	vod_ids		= []
	
	self.LIST.reset()
	self.Body.setImage(Body_bg_cats)
	
	epg_url = _BASE_ + ':' + _PORT_ + '/panel_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_
	epg_channels = Get_Data(epg_url)
	
	all = regex_get_all(epg_channels, '{"num', 'direct')
	for a in all:
		if '"tv_archive":1' in a:

			NAME = regex_from_to(a, '"name":"', '"')
			EPG_ID = regex_from_to(a, '"epg_channel_id":"', '"')
			IDS = regex_from_to(a, 'stream_id":"', '"')
			
			vod_ids.append('CTV:' + IDS)
			vod_cats.append(NAME)
			self.LIST.addItem(NAME)
		
	self.setFocus(self.LIST)
	
def Get_Shows(self, option):

	HIDE_RAND(self)
	
	global vod_ids
	global vod_cats

	vod_cats	= []
	vod_ids		= []
	
	self.LIST.reset()
	self.Body.setImage(Body_bg_cats)
	shows_url = _BASE_ + ':' + _PORT_ + '/enigma2.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&type=get_series&cat_id=0'
	link = Get_Data(shows_url)
	tree = ET.ElementTree(ET.fromstring(link))
	root = tree.getroot()
	for channel in root.findall('channel'):
		title = channel.find('title').text
		title = base64.b64decode(title)
		link = channel.find('playlist_url').text
		vod_cats.append(title)
		vod_ids.append('SVOD:' + str(link))
		self.LIST.addItem(title)
		
	self.setFocus(self.LIST)
	
def Get_Vod(self, Option):

	HIDE_RAND(self)

	global vod_ids
	global vod_cats
	
	self.LIST.reset()
	self.Body.setImage(Body_bg_cats)
	
	vod_ids = []
	vod_cats = []
	VOD_ITEMS = []

	try:
		if Option == 'movies':
			vod_url = _BASE_ + ':' + _PORT_ + '/enigma2.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&type=get_vod_categories'
			Vod_Categories = Get_Data(vod_url)
			
			XML_TREE = ET.ElementTree(ET.fromstring(Vod_Categories))
			XML_ROOT = XML_TREE.getroot()

			for ELEMENT in XML_ROOT.findall('channel'):

				VOD_NAME = base64.b64decode(ELEMENT.find('title').text.encode('utf-8').strip().replace('', ''))
				VOD_ID = ELEMENT.find('category_id').text

				if any(re.findall(r'TV|All|Demand', VOD_NAME, re.IGNORECASE)):
					pass
				else:
					VOD_NAME = VOD_NAME.replace('Movies|', '').replace('VOD|', '')

					if VOD_NAME in VOD_ITEMS:
						pass
					else:
						vod_ids.append(VOD_ID)
						vod_cats.append(VOD_NAME)
						self.LIST.addItem(VOD_NAME)
	
		elif Option == 'shows':
			vod_url = _BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_vod_categories'
			
			Regex = '{"category_id":"([\d]+)","category_name":"(.*?)","parent_id":"85"}'
			
			Vod_Categories = Get_Data(vod_url)
			Categories = find_multiple_matches(Vod_Categories,Regex)
	
			for Category in Categories:
				if any(re.findall(r'}', Category[1], re.IGNORECASE)):
					pass
				else:
					Vod_id = Category[0]
					Vod_cat = Category[1].replace('TV|', '').replace('Tv|', '').replace('tv|', '')
					vod_ids.append(Vod_id)
					vod_cats.append(Vod_cat)
					self.LIST.addItem(Vod_cat)
		else:
			pass
	except:
		pass
		
	self.setFocus(self.LIST)

def Load_Vod(self):

	global Movie_ids
	global Movie_posters
	global Movie_dates
	global Movie_titles
	global Movie_types
	global Json_data
	
	self.VOD_LIST.reset()
	self.VOD_LIST.setVisible(True)
	self.Body.setImage(Body_bg_all)
	
	Movie_ids		=	[]
	Movie_types		=	[]
	Movie_titles	=	[]
	Movie_posters	=	[]
	Movie_dates		=	[]
	
	try:
		#IF THE MAIN LIST IF FOCUSEDRUN THE FOLLOWING CODE
		if self.getFocus() == self.LIST:
			Position	=	self.LIST.getSelectedPosition()
			Category	=	vod_ids[Position]
			
			if 'CTV:' in Category:

				MOVIES_URL = _BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_  + '&action=get_simple_data_table&stream_id=' + Category.replace('CTV:','') + '&limit=1000'
				VOD_Data = Get_Data(MOVIES_URL)
				Json_data = json.loads(VOD_Data)
				data2 = Json_data['epg_listings']
				for i in data2:
					Vod_Name	=	str(base64.b64decode(i['title']))
					Vod_ID		=	str(Category)
					Vod_Added	=	str(i['start'])
					Vod_Type	=	str(base64.b64decode(i['description']))
					CTV_Date 	= Vod_Added.replace(' ',':')
					
					Movie_ids.append(Vod_ID)
					Movie_titles.append(Vod_Name)
					Movie_types.append(Vod_Type)
					Movie_dates.append(CTV_Date)
					self.VOD_LIST.addItem(Vod_Name)
					
			elif 'SVOD:' in Category:
				Category = Category.replace('SVOD:','')
				link = Get_Data(Category)
				tree = ET.ElementTree(ET.fromstring(link))
				root = tree.getroot()
				for channel in root.findall('channel'):
					title = channel.find('title').text
					title = base64.b64decode(title)
					link = channel.find('playlist_url').text
					Movie_titles.append(title)
					Movie_types.append('')
					Movie_dates.append('')
					Movie_ids.append('TVVOD:' + link)
					self.VOD_LIST.addItem(title)
			
			else:
				MOVIES_URL = _BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_vod_streams&category_id=' + Category

				VOD_Data = Get_Data(MOVIES_URL)
				Json_data = json.loads(VOD_Data)
				
				for i in Json_data:
					Vod_Name	=	str(i['name'])
					Vod_Poster	=	str(i['stream_icon'])
					Vod_ID		=	str(i['stream_id'])
					Vod_Added	=	str(i['added'])
					Vod_Type	=	str(i['container_extension'])
					
					Movie_ids.append(Vod_ID)
					Movie_titles.append(Vod_Name)
					Movie_posters.append(Vod_Poster)
					Movie_types.append(Vod_Type)
					self.VOD_LIST.addItem(Vod_Name)
					
	except (RuntimeError, SystemError):
		pass
		
def Load_Episodes(self, option):
	
	global Movie_ids
	global Movie_posters
	global Movie_dates
	global Movie_titles
	global Movie_types
	global Json_data
	
	self.VOD_LIST.reset()
	self.VOD_LIST.setVisible(True)
	self.Body.setImage(Body_bg_all)
	
	Movie_ids		=	[]
	Movie_types		=	[]
	Movie_titles	=	[]
	Movie_posters	=	[]
	Movie_dates		=	[]
	
	EPISODES_URL = option.replace('TVVOD:','')
	VOD_Data = Get_Data(EPISODES_URL)
	tree = ET.ElementTree(ET.fromstring(VOD_Data))
	root = tree.getroot()
	for channel in root.findall('channel'):
		title = channel.find('title').text
		title = base64.b64decode(title)
		image = channel.find('desc_image').text
		link = channel.find('stream_url').text
		Movie_titles.append(title)
		Movie_types.append('')
		Movie_dates.append('')
		Movie_posters.append(image)
		Movie_ids.append('PLAY:' + link)
		self.VOD_LIST.addItem(title)
	
		
def Play(self):

	position = 	self.VOD_LIST.getSelectedPosition()
	option = Movie_ids[position]

	if 'TVVOD:' in option:
	
		Load_Episodes(self, option)
		
	else:

		Link_name	=	MOVIE_INFO_NAME
		Link_Type	=	MOVIE_INFO_TYPE
		Link_Image  =	VOD_MOVIE_POSTER
		Link_ID		=	MOVIE_INFO_ID
		Link_DATE	=	MOVIE_INFO_DATE
		
		if 'CTV:' in Link_ID:
			Link_ID = Link_ID.replace('CTV:','')
			Link = _BASE_ + ':' + _PORT_ + '/streaming/timeshift.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&stream=' + Link_ID + '&start=' + Link_DATE + '&duration=540'
			Show_List	=	xbmcgui.ListItem(Link_name, iconImage=Link_Image,thumbnailImage=Link_Image)
			xbmc.Player().play(Link, Show_List, False)
		
		elif 'PLAY:' in Link_ID:
			Link = Link_ID.replace('PLAY:','')
			Show_List	=	xbmcgui.ListItem(Link_name, iconImage=Link_Image,thumbnailImage=Link_Image)
			xbmc.Player().play(Link, Show_List, False)
			
			
		else:
			Link = _BASE_ + ':' + _PORT_ + '/movie/' + _USERNAME_ + '/' + _PASSWORD_ + '/' + str(MOVIE_INFO_ID) + '.' + MOVIE_INFO_TYPE
			Show_List	=	xbmcgui.ListItem(Link_name, iconImage=Link_Image,thumbnailImage=Link_Image)
			xbmc.Player().play(Link, Show_List, False)
	
def Vod_Search(self):

	HIDE_RAND(self)

	global Movie_ids
	global Movie_posters
	global Movie_dates
	global Movie_titles
	global Movie_types

	self.VOD_LIST.reset()
	self.VOD_LIST.setVisible(True)
	self.Body.setImage(Body_bg_all)
			
	Movie_ids		=	[]
	Movie_types		=	[]
	Movie_titles	=	[]
	Movie_posters	=	[]
	Search_Keywords	=	[]
	voddata = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_, 'voddata.xml'))

	Search_String = self.SEARCH.getText().lower()
	
	Keywords = Search_String.split()
	Search_Keywords.append(Keywords)

	Search_URL	= _BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_vod_streams'
	Search_Request = open_url(Search_URL)
	
	Search_Data = json.loads(Search_Request)
	
	for i in Search_Data:
		Search_Name = i['name'].lower()
		Search_ID	= i['stream_id']
		Search_Icon = i['stream_icon']
		Search_Type = i['container_extension']
		
		for key in Search_Keywords:
			if key[0] in Search_Name:
				Movie_titles.append(Search_Name)
				Movie_ids.append(Search_ID)
				Movie_posters.append(Search_Icon)
				Movie_types.append(Search_Type)
				self.VOD_LIST.addItem(Search_Name)
				self.setFocus(self.VOD_LIST)
				
				
def VOD_Random(self):
	
	global RAND_NAMES
	global RAND_IMAGES
	global RAND_IDS
	global RAND_TYPES
	global RAND_NUMBERS
	
	RAND_NAMES	= []
	RAND_IMAGES = []
	RAND_IDS = []
	RAND_TYPES = []
	RAND_NUMBERS = []
	
	RAND_URL	= _BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_vod_streams'
	VOD_DATA = Get_Data(RAND_URL)
	VOD_JSON = json.loads(VOD_DATA)
	
	for i in VOD_JSON:

		RAND_NAME	= str(i['name'].encode('utf-8').strip())
		RAND_ID		= str(i['stream_id'])
		RAND_IMAGE = str(i['stream_icon'])#.encode('utf-8').strip())
			#RAND_IMAGE	= str('http://via.placeholder.com/350/d82a2a/ffffff?text='+RAND_NAME.replace(' ','%20'))
		RAND_TYPE	= str(i['container_extension'])

		if '- S' in RAND_NAME:
			pass
		else:
			if RAND_IMAGE =="":
				pass
			else:
				RAND_IDS.append(RAND_ID)
				RAND_NAMES.append(RAND_NAME)
				RAND_IMAGES.append(RAND_IMAGE)
				RAND_TYPES.append(RAND_TYPE)
	
	Count = len(RAND_IMAGES)
	
	for x in range (1, Count):
		num = random.randint(1, Count)
		while num in RAND_NUMBERS:
			num = random.randint(1, Count)
		RAND_NUMBERS.append(num)
	
	self.RAND_ONE.setImage(RAND_IMAGES[RAND_NUMBERS[0]])
	self.RAND_TWO.setImage(RAND_IMAGES[RAND_NUMBERS[1]])
	self.RAND_THREE.setImage(RAND_IMAGES[RAND_NUMBERS[2]])
	self.RAND_FOUR.setImage(RAND_IMAGES[RAND_NUMBERS[3]])
	self.RAND_FIVE.setImage(RAND_IMAGES[RAND_NUMBERS[4]])
	self.RAND_SIX.setImage(RAND_IMAGES[RAND_NUMBERS[5]])
	self.RAND_SEVEN.setImage(RAND_IMAGES[RAND_NUMBERS[6]])
	self.RAND_EIGHT.setImage(RAND_IMAGES[RAND_NUMBERS[7]])
	self.RAND_NINE.setImage(RAND_IMAGES[RAND_NUMBERS[8]])
	self.RAND_TEN.setImage(RAND_IMAGES[RAND_NUMBERS[9]])
	
def RAND_PLAY(self,position):
	
	RAND_POSITION = int(position)
	
	RAND_PLAY_NAME	=	RAND_NAMES[RAND_NUMBERS[RAND_POSITION]]
	RAND_PLAY_TYPE	=	RAND_TYPES[RAND_NUMBERS[RAND_POSITION]]
	RAND_PLAY_IMAGE	=	RAND_IMAGES[RAND_NUMBERS[RAND_POSITION]]
	RAND_PLAY_ID	=	RAND_IDS[RAND_NUMBERS[RAND_POSITION]]

	RAND_PLAY_URL = _BASE_ + ':' + _PORT_ + '/movie/' + _USERNAME_ + '/' + _PASSWORD_ + '/' + str(RAND_PLAY_ID) + '.' + RAND_PLAY_TYPE
	
	RAND_LIST	=	xbmcgui.ListItem(RAND_PLAY_NAME, iconImage=RAND_PLAY_IMAGE,thumbnailImage=RAND_PLAY_IMAGE)
	xbmc.Player().play(RAND_PLAY_URL, RAND_LIST, False)
	
def HIDE_RAND(self):

	self.RAND_ONE.setVisible(False)
	self.RAND_TWO.setVisible(False)
	self.RAND_THREE.setVisible(False)
	self.RAND_FOUR.setVisible(False)
	self.RAND_FIVE.setVisible(False)
	self.RAND_SIX.setVisible(False)
	self.RAND_SEVEN.setVisible(False)
	self.RAND_EIGHT.setVisible(False)
	self.RAND_NINE.setVisible(False)
	self.RAND_TEN.setVisible(False)
	self.RAND_BUTTON_ONE.setVisible(False)
	self.RAND_BUTTON_TWO.setVisible(False)
	self.RAND_BUTTON_THREE.setVisible(False)
	self.RAND_BUTTON_FOUR.setVisible(False)
	self.RAND_BUTTON_FIVE.setVisible(False)
	self.RAND_BUTTON_SIX.setVisible(False)
	self.RAND_BUTTON_SEVEN.setVisible(False)
	self.RAND_BUTTON_EIGHT.setVisible(False)
	self.RAND_BUTTON_NINE.setVisible(False)
	self.RAND_BUTTON_TEN.setVisible(False)
	
def SHOW_RAND(self):

	self.RAND_ONE.setVisible(True)
	self.RAND_TWO.setVisible(True)
	self.RAND_THREE.setVisible(True)
	self.RAND_FOUR.setVisible(True)
	self.RAND_FIVE.setVisible(True)
	self.RAND_SIX.setVisible(True)
	self.RAND_SEVEN.setVisible(True)
	self.RAND_EIGHT.setVisible(True)
	self.RAND_NINE.setVisible(True)
	self.RAND_TEN.setVisible(True)
	self.RAND_BUTTON_ONE.setVisible(True)
	self.RAND_BUTTON_TWO.setVisible(True)
	self.RAND_BUTTON_THREE.setVisible(True)
	self.RAND_BUTTON_FOUR.setVisible(True)
	self.RAND_BUTTON_FIVE.setVisible(True)
	self.RAND_BUTTON_SIX.setVisible(True)
	self.RAND_BUTTON_SEVEN.setVisible(True)
	self.RAND_BUTTON_EIGHT.setVisible(True)
	self.RAND_BUTTON_NINE.setVisible(True)
	self.RAND_BUTTON_TEN.setVisible(True)
	
def SET_LIVE(self,LIVE_CATEGORY):

	_self_.setSetting('LIVE_CAT', LIVE_CATEGORY)
	Live.LiveWindow()
	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        try:
            r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
        except:
            r = ''
    else:
        try:
            r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
        except:
            r = ''
    return r


def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	
				
#############################################################
######### Class Containing the GUi Code / Controls ##########
class Movies(pyxbmct.AddonFullWindow):

	#CLOSE THE BUSY SPINNER THAT ALL WAYS APPEARS USING PYXBMCT
	xbmc.executebuiltin("Dialog.Close(busydialog)")

	def __init__(self, title='area51x'):
		super(Movies, self).__init__(title)
		
		#set the location and size of your window in kodi
		self.setGeometry(1280, 720, 111, 52)
		
		## SET THE ADDON BACKGROUND IMAGE AND HEADER AND NAV WITH PYXBMCT.IMAGE
		Background = pyxbmct.Image(Background_Image)
		Header = pyxbmct.Image(Header_bg)
		Nav = pyxbmct.Image(Nav_bg)
		self.Body = pyxbmct.Image(Body_bg)
		
		## PLACE THE IMAGES ON SCREEN USING (X, Y, H, W)
		self.placeControl(Background, -9, -1, 140, 56)
		self.placeControl(Header, -11, -1, 12, 56)
		self.placeControl(Nav, -1, -1, 12, 56)
		self.placeControl(self.Body, 9, -1, 128, 54)
		
		## function to set information controls none interactive
		self.set_info_controls()
		
		## function to set active controls that users interact with 
		self.set_active_controls()
		
		## function to set what happens when users press left,right,up,down on your active controls
		self.set_navigation()
		
		# SET THE LOGO FOR THE ADDON THIS IS PLACED HERSO ITS ABOVE THE BACKGROUND IMAGE
		Logo = pyxbmct.Image(Logo_img)
		self.placeControl(Logo, -11, -1, 12, 15)
		
		## connect the back button to pyx to close window
		self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		self.connect(self.VOD_MOVIES, lambda:Get_Vod(self, 'movies'))
		self.connect(self.VOD_SHOWS, lambda:Get_Shows(self, 'shows'))
		self.connect(self.CATCHUP_TV, lambda:Get_Catchup(self))
		self.connect(self.LIST, lambda:Load_Vod(self))
		self.connect(self.VOD_LIST,lambda:Play(self))
		self.connect(self.SearchButton, lambda:Vod_Search(self))
		
		self.connect(self.RAND_BUTTON_ONE, lambda:RAND_PLAY(self,'0'))
		self.connect(self.RAND_BUTTON_TWO, lambda:RAND_PLAY(self,'1'))
		self.connect(self.RAND_BUTTON_THREE, lambda:RAND_PLAY(self,'2'))
		self.connect(self.RAND_BUTTON_FOUR, lambda:RAND_PLAY(self,'3'))
		self.connect(self.RAND_BUTTON_FIVE, lambda:RAND_PLAY(self,'4'))
		self.connect(self.RAND_BUTTON_SIX, lambda:RAND_PLAY(self,'5'))
		self.connect(self.RAND_BUTTON_SEVEN, lambda:RAND_PLAY(self,'6'))
		self.connect(self.RAND_BUTTON_EIGHT, lambda:RAND_PLAY(self,'7'))
		self.connect(self.RAND_BUTTON_NINE, lambda:RAND_PLAY(self,'8'))
		self.connect(self.RAND_BUTTON_TEN, lambda:RAND_PLAY(self,'9'))
		
		self.setFocus(self.VOD_MOVIES)
		VOD_Random(self)
		

	def set_info_controls(self):
		self.POSTER			=	pyxbmct.Image('')
		self.DESCRIPTION	=	pyxbmct.TextBox()
		self.SEARCH			=	pyxbmct.Edit('Search...', textColor='#000000', focusTexture=search_bg, noFocusTexture=search_bg, isPassword=False)
		
		
		self.placeControl(self.POSTER, 23, 38, 69, 10)
		self.placeControl(self.DESCRIPTION, 97, 35, 30, 17)
		self.placeControl(self.SEARCH, 11, 19, 9, 10)
		

	def set_active_controls(self):
	
		##SET THE PYXBMCT BUTTONS THAT USERS INTERACT WITH
		
		self.EVENTS	=	pyxbmct.Button(' EVENTS ',	focusTexture=Focused_Button, noFocusTexture="", textColor='0xFF3E4349', focusedColor='0xFF3E4349')
		self.SearchButton	=	pyxbmct.Button('',	focusTexture=Search_Button_Selected, noFocusTexture=Search_Button)
		self.GUIDE		=	pyxbmct.Button('',	focusTexture=Guide_img_selected, noFocusTexture=Guide_img)
		self.VOD_MOVIES	=	pyxbmct.Button('',	focusTexture=movies, noFocusTexture=movies_un)
		self.VOD_SHOWS	=	pyxbmct.Button('',	focusTexture=tvshows, noFocusTexture=tvshows_un)
		self.CATCHUP_TV	=	pyxbmct.Button('',	focusTexture=catchup, noFocusTexture=catchup_un)
		self.VOD_LIST	=	pyxbmct.List(buttonFocusTexture=List_vod_no, buttonTexture='', _imageWidth=20, _imageHeight=20, _space=-1, _itemHeight=71,  _itemTextXOffset=4, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
		self.LIST		=	pyxbmct.List(buttonFocusTexture=List_vod_Focused, buttonTexture='', _imageWidth=20, _imageHeight=20, _space=-1, _itemHeight=71,  _itemTextXOffset=4, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
		
		self.RAND_ONE		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_TWO		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_THREE		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_FOUR		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_FIVE		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_SIX		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_SEVEN		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_EIGHT		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_NINE		=	pyxbmct.Image(DEFAULT_POSTER)
		self.RAND_TEN		=	pyxbmct.Image(DEFAULT_POSTER)
		
		self.RAND_BUTTON_ONE	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_TWO	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_THREE	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_FOUR	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_FIVE	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_SIX	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_SEVEN	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_EIGHT	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_NINE	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)
		self.RAND_BUTTON_TEN	=	pyxbmct.Button('',	focusTexture=PLAY_SEL, noFocusTexture=PLAY_IMG)


		self.placeControl(self.RAND_ONE, 27, 12, 45, 6)
		self.placeControl(self.RAND_TWO, 27, 20, 45, 6)
		self.placeControl(self.RAND_THREE, 27, 28, 45, 6)
		self.placeControl(self.RAND_FOUR, 27, 36, 45, 6)
		self.placeControl(self.RAND_FIVE, 27, 44, 45, 6)
		self.placeControl(self.RAND_SIX, 78, 12, 45, 6)
		self.placeControl(self.RAND_SEVEN, 78, 20, 45, 6)
		self.placeControl(self.RAND_EIGHT, 78, 28, 45, 6)
		self.placeControl(self.RAND_NINE, 78, 36, 45, 6)
		self.placeControl(self.RAND_TEN, 78, 44, 45, 6)
		
		self.placeControl(self.RAND_BUTTON_ONE, 27, 12, 45, 6)
		self.placeControl(self.RAND_BUTTON_TWO, 27, 20, 45, 6)
		self.placeControl(self.RAND_BUTTON_THREE, 27, 28, 45, 6)
		self.placeControl(self.RAND_BUTTON_FOUR, 27, 36, 45, 6)
		self.placeControl(self.RAND_BUTTON_FIVE, 27, 44, 45, 6)
		self.placeControl(self.RAND_BUTTON_SIX, 78, 12, 45, 6)
		self.placeControl(self.RAND_BUTTON_SEVEN, 78, 20, 45, 6)
		self.placeControl(self.RAND_BUTTON_EIGHT, 78, 28, 45, 6)
		self.placeControl(self.RAND_BUTTON_NINE, 78, 36, 45, 6)
		self.placeControl(self.RAND_BUTTON_TEN, 78, 44, 45, 6)
		
		self.placeControl(self.SearchButton, 11, 27, 9, 7)
		self.placeControl(self.VOD_LIST, 20, 17, 122, 17)		
		self.placeControl(self.LIST, 20, 8, 122, 11)
		self.placeControl(self.GUIDE, -11, 12, 12, 9)
		self.placeControl(self.VOD_MOVIES, 30, -1, 12, 10)
		self.placeControl(self.VOD_SHOWS, 40, -1, 12, 10)
		self.placeControl(self.CATCHUP_TV, 50, -1, 12, 10)
		
		#SET UP THE CONTROL LISTENER FOR MOUSE AND BUTTON CLICKS TO UPDATE LISTS
		self.connectEventList(
			[pyxbmct.ACTION_MOVE_DOWN,
			pyxbmct.ACTION_MOVE_UP,
			pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
			pyxbmct.ACTION_MOUSE_WHEEL_UP,
			pyxbmct.ACTION_MOUSE_MOVE],
			self.list_update)
		
	def set_navigation(self):
		self.VOD_MOVIES.controlRight(self.RAND_BUTTON_ONE)
		self.VOD_SHOWS.controlRight(self.RAND_BUTTON_SIX)
		self.SEARCH.controlRight(self.SearchButton)
		self.SEARCH.controlUp(self.GUIDE)
		self.SearchButton.controlLeft(self.SEARCH)
		self.SEARCH.controlDown(self.VOD_MOVIES)
		self.SearchButton.controlDown(self.VOD_MOVIES)
		self.VOD_MOVIES.controlUp(self.SEARCH)
		self.VOD_SHOWS.controlUp(self.VOD_MOVIES)
		self.VOD_MOVIES.controlDown(self.VOD_SHOWS)
		self.VOD_SHOWS.controlDown(self.CATCHUP_TV)
		self.CATCHUP_TV.controlUp(self.VOD_SHOWS)
		self.CATCHUP_TV.controlDown(self.VOD_MOVIES)
		self.LIST.controlUp(self.GUIDE)
		self.LIST.controlLeft(self.VOD_MOVIES)
		self.LIST.controlRight(self.VOD_LIST)
		self.VOD_LIST.controlLeft(self.LIST)
		self.GUIDE.controlDown(self.VOD_MOVIES)
		

		self.RAND_BUTTON_ONE.controlDown(self.RAND_BUTTON_SIX)
		self.RAND_BUTTON_ONE.controlRight(self.RAND_BUTTON_TWO)
		self.RAND_BUTTON_ONE.controlLeft(self.VOD_MOVIES)
		self.RAND_BUTTON_TWO.controlDown(self.RAND_BUTTON_SEVEN)
		self.RAND_BUTTON_TWO.controlRight(self.RAND_BUTTON_THREE)
		self.RAND_BUTTON_TWO.controlLeft(self.RAND_BUTTON_ONE)
		self.RAND_BUTTON_THREE.controlDown(self.RAND_BUTTON_EIGHT)
		self.RAND_BUTTON_THREE.controlRight(self.RAND_BUTTON_FOUR)
		self.RAND_BUTTON_THREE.controlLeft(self.RAND_BUTTON_TWO)
		self.RAND_BUTTON_FOUR.controlDown(self.RAND_BUTTON_NINE)
		self.RAND_BUTTON_FOUR.controlRight(self.RAND_BUTTON_FIVE)
		self.RAND_BUTTON_FOUR.controlLeft(self.RAND_BUTTON_THREE)
		self.RAND_BUTTON_FIVE.controlDown(self.RAND_BUTTON_TEN)
		self.RAND_BUTTON_FIVE.controlRight(self.RAND_BUTTON_ONE)
		self.RAND_BUTTON_FIVE.controlLeft(self.RAND_BUTTON_FOUR)
		self.RAND_BUTTON_SIX.controlUp(self.RAND_BUTTON_ONE)
		self.RAND_BUTTON_SIX.controlRight(self.RAND_BUTTON_SEVEN)
		self.RAND_BUTTON_SIX.controlLeft(self.VOD_SHOWS)
		self.RAND_BUTTON_SEVEN.controlUp(self.RAND_BUTTON_TWO)
		self.RAND_BUTTON_SEVEN.controlRight(self.RAND_BUTTON_EIGHT)
		self.RAND_BUTTON_SEVEN.controlLeft(self.RAND_BUTTON_SIX)
		self.RAND_BUTTON_EIGHT.controlUp(self.RAND_BUTTON_THREE)
		self.RAND_BUTTON_EIGHT.controlRight(self.RAND_BUTTON_NINE)
		self.RAND_BUTTON_EIGHT.controlLeft(self.RAND_BUTTON_SEVEN)
		self.RAND_BUTTON_NINE.controlUp(self.RAND_BUTTON_FOUR)
		self.RAND_BUTTON_NINE.controlRight(self.RAND_BUTTON_TEN)
		self.RAND_BUTTON_NINE.controlLeft(self.RAND_BUTTON_EIGHT)
		self.RAND_BUTTON_TEN.controlUp(self.RAND_BUTTON_FIVE)
		self.RAND_BUTTON_TEN.controlRight(self.RAND_BUTTON_SIX)
		self.RAND_BUTTON_TEN.controlLeft(self.RAND_BUTTON_NINE)
        
	def list_update(self):
	
		global MOVIE_INFO_ID
		global VOD_MOVIE_POSTER
		global MOVIE_INFO_TYPE
		global MOVIE_INFO_NAME
		global MOVIE_INFO_DATE
		global Vod_Info_Json
		try:
			#IF THE MAIN LIST IF FOCUSEDRUN THE FOLLOWING CODE
			if self.getFocus() == self.VOD_LIST:
			
				self.DESCRIPTION.setVisible(True)
				self.POSTER.setVisible(True)
				
				VOD_Position =	self.VOD_LIST.getSelectedPosition()
				
				ID_CHECK = Movie_ids[VOD_Position]
				if 'CTV:' in ID_CHECK:
				
					CTV_ID = ID_CHECK.replace('CTV:','')
					MOVIE_INFO_ID		=	ID_CHECK
					MOVIE_INFO_TYPE 	=	Movie_types[VOD_Position]
					MOVIE_INFO_NAME 	=	Movie_titles[VOD_Position]
					MOVIE_INFO_DATE 	=	Movie_dates[VOD_Position]
					
					
					TMDB_SEARCH_TERM	= Movie_titles[VOD_Position]
	
					if _TMDB_KEY_ == '':
						_TMDB_API_KEY_ = '45937b7d04244a92494fea9c5e1f145a'
						
					else:
						_TMDB_API_KEY_  = _TMDB_KEY_
						
					TMDB_REQUEST		= Get_Data('https://api.themoviedb.org/3/search/tv?api_key=' + _TMDB_API_KEY_  + '&query=' + TMDB_SEARCH_TERM.replace(' ','+'))
					TMDB_REGEX			= '"results":\[{"original_name":"(.*?)","id":(.*?),"name":"(.*?)","vote_count":(.*?),"vote_average":(.*?),"poster_path":"(.*?)","first_air_date":"(.*?)","popularity":(.*?),"genre_ids":\[(.*?)\],"original_language":"(.*?)","backdrop_path":"(.*?)","overview":"(.*?)","origin_country":\[(.*?)\]}'
					TMDB_DATA			= find_single_match(TMDB_REQUEST,TMDB_REGEX)
					
					if TMDB_DATA == '':
						VOD_MOVIE_POSTER		= xbmc.translatePath(os.path.join(Skin_Path, 'POSTER.jpg'))
						TMDB_DESCRIPTION	= 'No Information On Catchup Show Found!'
					else:
						TMDB_DESCRIPTION	= TMDB_DATA[11] 
						VOD_MOVIE_POSTER		= 'https://image.tmdb.org/t/p/w500/' + TMDB_DATA[5].replace('\/', '/')
						
					COMBINED = '[COLOR white][B]' + MOVIE_INFO_NAME + '[/COLOR][/B]\n\n' + '[COLOR silver][B]Release Date[/B] : ' + MOVIE_INFO_DATE + '[/COLOR]\n\n' + '[COLOR silver][B]Description[/B] : ' + MOVIE_INFO_TYPE + '[/COLOR]'
					
					self.POSTER.setImage(VOD_MOVIE_POSTER)
					
					self.DESCRIPTION.setText(COMBINED)
					self.DESCRIPTION.autoScroll(1000, 1000, 1000)
				elif 'PLAY' in ID_CHECK:	
				
					VOD_MOVIE_POSTER	=	Movie_posters[VOD_Position].replace('\/','/')
					self.POSTER.setImage(VOD_MOVIE_POSTER)
					
					MOVIE_INFO_ID		=	Movie_ids[VOD_Position]
					MOVIE_INFO_TYPE 	=	Movie_types[VOD_Position]
					MOVIE_INFO_NAME 	=	Movie_titles[VOD_Position]
					MOVIE_INFO_DATE		=	'Unknown'

					COMBINED = '[COLOR white][B]' + MOVIE_INFO_NAME.title() + '[/COLOR][/B]\n\n We hope You Enjoy This Show!' 
					
					self.DESCRIPTION.setText(COMBINED)
					self.DESCRIPTION.autoScroll(1000, 1000, 1000)
					
				else:
				
					VOD_MOVIE_POSTER	=	Movie_posters[VOD_Position].replace('\/','/')
					self.POSTER.setImage(VOD_MOVIE_POSTER)
					
					MOVIE_INFO_ID		=	Movie_ids[VOD_Position]
					MOVIE_INFO_TYPE 	=	Movie_types[VOD_Position]
					MOVIE_INFO_NAME 	=	Movie_titles[VOD_Position]
					
					MOVIE_INFO_URL		=	_BASE_ + ':' + _PORT_ + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_vod_info&vod_id=' + str(MOVIE_INFO_ID)
					MOVIE_INFO_DATA		=	Get_Data(MOVIE_INFO_URL)

					Vod_Info_Json = json.loads(MOVIE_INFO_DATA)
				
					#for item in Vod_Info_Json:

					MOVIE_INFO_GENRES	=	Vod_Info_Json['info']['genre']
					MOVIE_INFO_PLOT		=	Vod_Info_Json['info']['plot'].replace('\/', '/')
					MOVIE_INFO_CAST		=	Vod_Info_Json['info']['cast']
					MOVIE_INFO_RATING	=	Vod_Info_Json['info']['rating']
					MOVIE_INFO_DIRECTOR	=	Vod_Info_Json['info']['director']
					MOVIE_INFO_DATE		=	Vod_Info_Json['info']['releasedate']
					MOVIE_INFO_DURATION	=	Vod_Info_Json['info']['duration']
					COMBINED = '[COLOR white][B]' + MOVIE_INFO_NAME.title() + '[/COLOR][/B]\n\n' + '[COLOR silver][B]Release Date[/B] : ' + MOVIE_INFO_DATE + '\n\n[B]Movie Length[/B] : ' + MOVIE_INFO_DURATION + '\n\n[COLOR silver][B]Cast[/B] : ' + MOVIE_INFO_CAST + '\n\n[COLOR silver]'   + MOVIE_INFO_PLOT + '[/COLOR]'
					
					self.DESCRIPTION.setText(COMBINED)
					self.DESCRIPTION.autoScroll(1000, 1000, 1000)
					
			elif self.getFocus() == self.LIST:
				self.Body.setImage(Body_bg_cats)
				self.DESCRIPTION.setVisible(False)
				self.POSTER.setVisible(False)
				self.VOD_LIST.reset()
			elif self.getFocus() == self.GUIDE or self.VOD_MOVIES:
				self.Body.setImage(Body_bg)
				self.DESCRIPTION.setVisible(False)
				self.POSTER.setVisible(False)
				self.VOD_LIST.setVisible(False)
				self.LIST.reset()
				self.VOD_LIST.reset()
				SHOW_RAND(self)
				
				
				
		except (RuntimeError, SystemError):
			pass