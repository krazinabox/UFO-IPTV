import sys
import os
import json
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import load_channels
import hashlib
import re
import random
import base64
import urllib2
import server

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('profile') ) 
addonset	= ['4d4441364d5545364e7a6b364f5445364d4441364d44413d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMDNhMzAzMDNhMzAzMw=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5441364d4441364d44593d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMDNhMzAzMDNhMzUzOA=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5441364d4441364e7a413d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMDNhMzAzMDNhMzczMw=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5441364d4441364f44633d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMjNhMzMzNDNhMzczOQ=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d4467364d4467364d44673d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMDNhMzAzMDNhMzIzMA=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5463364d5463364d54633d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzkzODNhMzczNjNhMzUzNA=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d4445364d5445364d6a493d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczOTNhMzIzMzNhMzIzMzNhMzIzMw=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5449364d7a51364f546b3d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzIzMzNhMzIzMzNhMzIzMw=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d6a51364e7a6b364e44493d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzYzNjNhMzYzNjNhMzUzMg=='.decode('base64').decode('hex'), '4d4441364d5545364e7a6b364d4441364d5441364e54413d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczOTNhMzEzMjNhMzMzNDNhMzkzOQ=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5445364d6a49364e6a4d3d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMjNhMzMzNDNhMzYzOA=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5449364d7a51364e7a413d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMjNhMzMzNDNhMzYzMg=='.decode('base64').decode('hex'), '4d4441364d5545364e7a67364d5449364d7a51364e6a513d'.decode('hex').decode('base64'), 'MzAzMDNhMzE0MTNhMzczODNhMzEzMjNhMzMzNDNhMzYzNw=='.decode('base64').decode('hex')]
eternal		= (random.choice(addonset))
current     = os.getcwd()

def portalConfig(number):

	portal = {};
	
	portal['parental'] = addon.getSetting("parental");
	portal['password'] = addon.getSetting("password");
	
	portal['name'] = addon.getSetting("portal_name_" + number);
	portal['url'] = addon.getSetting("portal_url_" + number);
	portal['mac'] = configMac(number);
	portal['serial'] = configSerialNumber(number);
		
	return portal;


def configMac(number):
	global go;
	import urllib2

	custom_mac = ('Y3VzdG9tX21hY18x'.decode('base64'));
	portal_mac = ('cG9ydGFsX21hY18x'.decode('base64'));
	
	if custom_mac != 'true':
		portal_mac = (eternal);
		
	elif not (custom_mac == 'true' and re.match("WzAtOWEtZl17Mn0oWy06XSlbMC05YS1mXXsyfShcXDFbMC05YS1mXXsyfSl7NH0k".decode('base64'), portal_mac.lower()) != None):
		xbmcgui.Dialog().notification(addonname, 'Custom Mac ' + number + ' is Invalid.', xbmcgui.NOTIFICATION_ERROR );
		portal_mac = '';
		go=False;
		
	return portal_mac;
	
	
def configSerialNumber(number):
	global go;
	
	send_serial = addon.getSetting('send_serial_' + number);
	custom_serial = addon.getSetting('custom_serial_' + number);
	serial_number = addon.getSetting('serial_number_' + number);
	device_id = addon.getSetting('device_id_' + number);
	device_id2 = addon.getSetting('device_id2_' + number);
	signature = addon.getSetting('signature_' + number);

	
	if send_serial != 'true':
		return None;
	
	elif send_serial == 'true' and custom_serial == 'false':
		return {'custom' : False};
		
	elif send_serial == 'true' and custom_serial == 'true':
	
		if serial_number == '' or device_id == '' or device_id2 == '' or signature == '':
			xbmcgui.Dialog().notification(addonname, 'Serial information is invalid.', xbmcgui.NOTIFICATION_ERROR );
			go=False;
			return None;
	
		return {'custom' : True, 'sn' : serial_number, 'device_id' : device_id, 'device_id2' : device_id2, 'signature' : signature};
		
	return None;