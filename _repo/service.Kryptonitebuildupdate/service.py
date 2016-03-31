import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import urllib2, urllib

path = xbmc.translatePath('special://home/addons/service.Kryptonitebuildupdate')

installed = xbmc.translatePath("special://home/addons/service.Kryptonitebuildupdate/installed_version.txt")
latest = xbmc.translatePath("special://home/addons/service.Kryptonitebuildupdate/latest_version.txt")

def path():
	if not os.path.exists(path):
		os.mkdir(path)

url = 'https://archive.org/download/kryptonite_20160224/latest_version.txt'
urllib.urlretrieve(url, latest)


file_i = open(installed)
file_i.close()

file_l = open(latest, 'r')
checksum_latest = file_l.read()
file_l.close()

def check(checksum):
	datafile = file(installed)
	updated = False
	for line in datafile:
		if checksum in line:
			updated = True
			break
	return updated

def wizard():
	choice = xbmcgui.Dialog().yesno('Kryptonite Build Updater for KRYPTONITE BUILD ONLY', 'Update available for Kryptonite Build', 'Select OK to start updating', nolabel='Cancel',yeslabel='OK')
	if choice == 0:
		return
	elif choice == 1:
		#xbmc.executebuiltin("RunAddon(plugin.video.UFOBuilds)")
		xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.UFOBuilds/?url=https://archive.org/download/kryptonite_20160224/Update.zip&mode=1&name=UPDATE&iconimage=https://archive.org/download/krazinabox_gmail_Icon_201601/icon.png)')
		file_i = open(installed, "w")
		file_i.write(checksum_latest)
		file_i.close()
		file_i = open(installed)
		checksum_updated = file_i.read()
		file_i.close()

if check(checksum_latest):
	xbmc.sleep(1000)
else:
	wizard()
