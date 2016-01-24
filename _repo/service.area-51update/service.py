import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import urllib2, urllib

path = xbmc.translatePath('special://home/addons/service.area-51update')

installed = xbmc.translatePath("special://home/addons/service.area-51update/installed_version.txt")
latest = xbmc.translatePath("special://home/addons/service.area-51update/latest_version.txt")

def path():
	if not os.path.exists(path):
		os.mkdir(path)

url = 'https://archive.org/download/latest_version_20160123/latest_version.txt'
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
	choice = xbmcgui.Dialog().yesno('Area-51 Updater for Area-51 Build', 'Update available for Area-51 BUILD', 'Select OK to start updating', nolabel='Cancel',yeslabel='OK')
	if choice == 0:
		return
	elif choice == 1:
		#xbmc.executebuiltin("RunAddon(plugin.program.area-51wizard)")
		xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.ufowizard/?url=https://archive.org/download/area-51update/area-51update.zip&mode=1&name=UPDATE&iconimage=https://archive.org/download/newicon_201601/newicon.png)')
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
