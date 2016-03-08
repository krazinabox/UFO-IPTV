import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import urllib2, urllib

path = xbmc.translatePath('special://home/addons/service.kingbuildupdate')

installed = xbmc.translatePath("special://home/addons/service.kingbuildupdate/installed_version.txt")
latest = xbmc.translatePath("special://home/addons/service.kingbuildupdate/latest_version.txt")

def path():
	if not os.path.exists(path):
		os.mkdir(path)

url = 'https://ia601507.us.archive.org/24/items/latest_version/latest_version.txt'
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
	choice = xbmcgui.Dialog().yesno('King Build Updater for Nebula King Build', 'Update available for Nebula King BUILD', 'Select OK to start updating', nolabel='Cancel',yeslabel='OK')
	if choice == 0:
		return
	elif choice == 1:
		#xbmc.executebuiltin("RunAddon(plugin.program.kodikingbuildwizard)")
		xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.mykodibuildwizard/?url=https%3A%2F%2Farchive.org%2Fdownload%2Fkingbuild_update_201601%2Fkingbuild_update.zip&mode=1&name=UPDATE&iconimage=https%3A%2F%2Farchive.org%2Fdownload%2Fevansataz_msn_Icon_201512%2Ficon.png)')
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
