import xbmcplugin,xbmcaddon
import time
import datetime
import xbmc
import random
import os
import urllib2
import zipfile, json, hashlib
import resources.lib.utils as utils
from resources.lib.croniter import croniter
import traceback

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
offset1hr = __addon__.getSetting("offset1hr")
pvrStalkerUsername =  __addon__.getSetting("donation")
pvrStalkerMac =  __addon__.getSetting("mac")
configureSimple = __addon__.getSetting("configureSimple")
configureStalker = __addon__.getSetting("configureStalker")

class epgUpdater:

    def __init__(self):
        self.monitor = UpdateMonitor(update_method = self.settingsChanged)
        self.enabled = utils.getSetting("enable_scheduler")
        self.next_run = 0
        self.schedule_time = __addon__.getSetting("schedule_time")
        self.unzipPath = __addon__.getSetting("downloadPath")
        if 'special://' in self.unzipPath:
            self.realUnzipPath =  xbmc.translatePath(self.unzipPath)
        else:
            self.realUnzipPath =  self.unzipPath


        if configureSimple != 'false' :
            utils.log(configureSimple)
            self.cycleAddon('pvr.iptvsimple')
            self.cycleAddon('plugin.video.stalker')

            try:
              self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
            except:
              utils.log("Failed to find pvr.iptvsimple addon")
              self.pvriptvsimple_addon = None

            try:
              self.videostalker = xbmcaddon.Addon('plugin.video.stalker')
            except:
              utils.log("Failed to find plugin.video.stalker addon")
              self.pvriptvsimple_addon = None

        if configureStalker != 'false' :
            try:
              self.cycleAddon('pvr.stalker')
              self.pvrstalker_addon = xbmcaddon.Addon('pvr.stalker')
            except:
              utils.log("Failed to find pvr.stalker addon")
              self.pvrstalker_addon = None


        self.updateEpg()
        self.setup()

    def cycleAddon(self, addonName):
        #disable - crashes kodi right now...
        return
        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":false},"id":1}' % addonName
        result = xbmc.executeJSONRPC(json)
        xbmc.sleep(1000)
        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true},"id":1}' % addonName
        result = xbmc.executeJSONRPC(json)

    def getRandomTime(self):
        hour = random.randrange(2,5)
        hourStr = str(hour).zfill(2)
        minute = random.randrange(1,59)
        minuteStr = str(minute).zfill(2)
        time = hourStr + ':' + minuteStr
        return time

    def setup(self):
        #scheduler was turned on, find next run time
        if self.schedule_time == '02:00':
            newTime = self.getRandomTime()
            self.schedule_time = newTime
            utils.log(newTime)
            __addon__.setSetting('schedule_time', newTime)

        utils.log("StalkerSettings::scheduler enabled, finding next run time")
        if configureSimple != 'false' :
            utils.log("Configuring IPTV Simple")

            if self.pvriptvsimple_addon != None and self.videostalker != None:
                self.pvriptvsimple_addon.setSetting("epgCache", "false")
                self.pvriptvsimple_addon.setSetting("epgPathType", "0")
                self.pvriptvsimple_addon.setSetting("epgPath", 'https://github.com/psyc0n/epgninja/raw/master/guide.xml.gz')
                self.pvriptvsimple_addon.setSetting("m3uPathType", "0")
                self.pvriptvsimple_addon.setSetting("m3uPath", "http://localhost:8899/channels-1.m3u")
                self.cycleAddon('pvr.iptvsimple')
            else:
                utils.log('Addon not found')

        if configureStalker != 'false' :
            utils.log("Configuring PVR Stalker")
            if self.pvrstalker_addon != None:
                checkSetting =  self.pvrstalker_addon.getSetting('server_0')
                utils.log(checkSetting)

                portalEndpoint  =  __addon__.getSetting("portalEndpoint")

                if portalEndpoint == '0' :
                    portalUrl = "http://portal1.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '1' :
                    portalUrl = "http://portal2.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '2' :
                    portalUrl = "http://portal3.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '3' :
                    portalUrl = "http://portal4.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '4' :
                    portalUrl = "http://portal5.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '5' :
                    portalUrl = "http://portal6.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '6' :
                    portalUrl = "http://portal7.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '7' :
                    portalUrl = "http://portal8.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '8' :
                    portalUrl = 'http://portal.iptvrocket.tv/stalker_portal/c/index.html'
                if portalEndpoint == '9' :
                    portalUrl = 'http://portal1.iptvrocket.tv/stalker_portal/c/index.html'
                if portalEndpoint == '10' :
                    portalUrl = 'http://portal2.iptvrocket.tv/stalker_portal/c/index.html'
                if portalEndpoint == '11' :
                    portalUrl = 'http://mw1.iptv66.tv/stalker_portal/c/index.html'
                if portalEndpoint == '12' :
                    portalUrl = 'http://mw2.iptv66.tv/stalker_portal/c/index.html'




                if portalEndpoint == '0' :
                    portalUrl = "http://portal1.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '1' :
                    portalUrl = "http://portal2.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '2' :
                    portalUrl = "http://portal3.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '3' :
                    portalUrl = "http://portal4.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '4' :
                    portalUrl = "http://portal5.iptvprivateserver.tv/stalker_portal/c/index.html"
                if portalEndpoint == '5' :
                    portalUrl = 'http://portal.iptvrocket.tv/stalker_portal/c/index.html'
                if portalEndpoint == '6' :
                    portalUrl = 'http://mw1.iptv66.tv/stalker_portal/c/index.html'


                if pvrStalkerUsername != "":


                    sn = hashlib.md5(pvrStalkerMac).hexdigest().upper()[13:];
                    device_id = hashlib.sha256(sn).hexdigest().upper();
                    device_id2 = hashlib.sha256(pvrStalkerMac).hexdigest().upper();
                    signature = hashlib.sha256(sn + pvrStalkerMac).hexdigest().upper();

                    self.pvrstalker_addon.setSetting('login_0', pvrStalkerUsername )
                    self.pvrstalker_addon.setSetting('server_0', portalUrl )
                    self.pvrstalker_addon.setSetting('password_0', pvrStalkerUsername )
                    self.pvrstalker_addon.setSetting('guide_cache_0', 'false' )
                    self.pvrstalker_addon.setSetting('guide_preference_0', '3' )
                    self.pvrstalker_addon.setSetting('xmltv_path_0', self.realUnzipPath+'epg_xmltv.xml' )
                    self.pvrstalker_addon.setSetting('xmltv_scope_0', '1' )
                    self.pvrstalker_addon.setSetting('device_id_0', device_id )
                    self.pvrstalker_addon.setSetting('device_id2_0', device_id2 )
                    self.pvrstalker_addon.setSetting('signature_0', signature)
                    self.pvrstalker_addon.setSetting('serial_number_0', sn )


                if pvrStalkerMac != "":
                    self.pvrstalker_addon.setSetting('mac_0', pvrStalkerMac )
                # self.cycleAddon('pvr.stalker')



        self.findNextRun(time.time())
        while(not xbmc.abortRequested):
            # Sleep/wait for abort for 10 seconds
            now = time.time()
            if(self.next_run <= now):
                if self.enabled:
                    self.updateEpg()
                    self.findNextRun(now)


            else:
                self.findNextRun(now)




            xbmc.sleep(500)
        # del self.monitor


    def settingsChanged(self):
        utils.log("Settings changed - update")
        current_enabled = utils.getSetting("enable_scheduler")
        offset1hr = __addon__.getSetting("offset1hr")
        pvrStalkerUsername =  __addon__.getSetting("username")
        pvrStalkerMac =  __addon__.getSetting("donation")
        configureSimple = __addon__.getSetting("configureSimple")
        self.schedule_time = __addon__.getSetting("schedule_time")
        configureStalker = __addon__.getSetting("configureStalker")

        if(current_enabled == "true" and self.enabled == "false"):
            #scheduler was just turned on

            self.enabled = current_enabled
            self.setup()
        elif (current_enabled == "false" and self.enabled == "true"):
            #schedule was turn off
            self.enabled = current_enabled

        if(self.enabled == "true"):
            #always recheck the next run time after an update
            utils.log('recalculate start time , after settings update')
            self.findNextRun(time.time())


    def parseSchedule(self):
        schedule_type = int(utils.getSetting("schedule_interval"))
        cron_exp = utils.getSetting("cron_schedule")
        if self.schedule_time:
            hour, minute = self.schedule_time.split(':')
            hour = int(hour)
            minute = int(minute)

            cron_exp = str(minute) + ' ' + str(hour)  + ' * * *'
            return cron_exp


    def findNextRun(self,now):
        #find the cron expression and get the next run time
        cron_exp = self.parseSchedule()
        cron_ob = croniter(cron_exp,datetime.datetime.fromtimestamp(now))
        new_run_time = cron_ob.get_next(float)
        # utils.log('new run time' +  str(new_run_time))
        # utils.log('next run time' + str(self.next_run))
        if(new_run_time != self.next_run):
            self.next_run = new_run_time
            utils.showNotification('EPG Updater', 'Next Update: ' + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M'))
            utils.log("scheduler will run again on " + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M'))




    def updateEpg(self):
        utils.log('StalkerSettings:: updateEpg')
        if offset1hr == 'true':
            epgFileName = 'guide2.zip'
        else:
            epgFileName = 'guide.zip'

        epgFile = None


        userdataPath = xbmc.translatePath('special://userdata')
        tempPath =  xbmc.translatePath('special://temp')



        epgDownloadPath = os.path.join(tempPath, epgFileName)
        unzipPath = os.path.join(userdataPath,'addon_data/pvr.stalker')

        try:
            response = urllib2.urlopen('https://github.com/psyc0n/epgninja/raw/master/'+epgFileName)
            epgFile = response.read()
        except Exception as e:
            utils.log('StalkerSettings: Main guide download failed.')
            utils.log('{0}\n{1}'.format(e, traceback.format_exc()))

        if epgFile is None:
          try:
              response = urllib2.urlopen('http://162.253.251.2/'+epgFileName)
              epgFile = response.read()
          except Exception as e:
              utils.log('StalkerSettings: Backup download failed.')
              utils.log('{0}\n{1}'.format(e, traceback.format_exc()))

        if epgFile:
            utils.log('StalkerSettings:: ' + epgDownloadPath)
            epgFH = open(epgDownloadPath, "w+b")
            epgFH.write(epgFile)
            epgFH.close()

            zfobj = zipfile.ZipFile(epgDownloadPath)

            for name in zfobj.namelist():
                outputFileName = self.realUnzipPath+'epg_xmltv.xml'
                uncompressed = zfobj.read(name)
                utils.log("StalkerSettings::Saving extracted file to " + str(outputFileName))
                output = open(outputFileName,'wb')
                output.write(uncompressed)
                output.close()

class UpdateMonitor(xbmc.Monitor):
    update_method = None

    def __init__(self,*args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.update_method = kwargs['update_method']

    def onSettingsChanged(self):
        self.update_method()
