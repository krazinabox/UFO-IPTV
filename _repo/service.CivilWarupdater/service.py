import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import urllib2, urllib

path = xbmc.translatePath('special://home/addons/service.CivilWarupdater')

installed = xbmc.translatePath("special://home/addons/service.CivilWarupdater/installed_version.txt")
latest = xbmc.translatePath("special://home/addons/service.CivilWarupdater/latest_version.txt")

def path():
	if not os.path.exists(path):
		os.mkdir(path)

url = 'https://archive.org/download/CivilWar_201604/latest_version.txt'
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
	choice = xbmcgui.Dialog().yesno('Updater for CivilWar Build', 'Update available for CivilWar BUILD', 'Select OK to start updating', nolabel='Cancel',yeslabel='OK')
	if choice == 0:
		return
	elif choice == 1:
		#xbmc.executebuiltin("RunAddon(plugin.video.UFOBuilds)")
		xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.UFOBuilds/?url=https://archive.org/download/CivilWar_201604/update.zip&mode=1&name=UPDATE&iconimage=https://archive.org/download/CivilWar_201604/civil-war.jpg)')
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
