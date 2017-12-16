import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os,json,base64,plugintools
import GoDev
import orig
import common,xbmcvfs,zipfile,downloader,extract
import xml.etree.ElementTree as ElementTree
reload(sys)
sys.setdefaultencoding('utf8')
SKIN_VIEW_FOR_MOVIES="515"
addonDir = plugintools.get_runtime_path()
global kontroll
background = "YmFja2dyb3VuZC5wbmc=" #background.png
defaultlogo = "bG9nby5wbmc=" #defaultlogo.png
hometheater = "aG9tZXRoZWF0ZXIuanBn"
noposter = "bm9wb3N0ZXIuanBn"
theater = "dGhlYXRlci5qcGc="
addonxml = "YWRkb24ueG1s"
addonpy = "ZGVmYXVsdC5weQ=="
icon = "aWNvbi5wbmc="
fanart = "ZmFuYXJ0LmpwZw=="
message = "VU5BVVRIT1JJWkVEIEVESVQgT0YgQURET04h"
def run():
    global pnimi
    global televisioonilink
    global filmilink
    global andmelink
    global uuenduslink
    global lehekylg
    global LOAD_LIVE
    global uuendused
    global vanemalukk
    global version
    global showxxx
    version = int(get_live("MQ=="))
    kasutajanimi=plugintools.get_setting("Username")
    salasona=plugintools.get_setting("Password")
    if not kasutajanimi:
        kasutajanimi = "NONE"
        salasona="NONE"
    lehekylg="http://iptv-area-51.tv"
    pordinumber="2095"
    uuendused=plugintools.get_setting(sync_data("dXVlbmR1c2Vk"))
    vanemalukk=plugintools.get_setting(sync_data("dmFuZW1hbHVraw=="))
    showxxx=plugintools.get_setting("showxxx")
    pnimi = get_live("T25lIFZpZXc=")
    LOAD_LIVE = os.path.join( plugintools.get_runtime_path() , "resources" , "art" )
    plugintools.log(pnimi+get_live("U3RhcnRpbmcgdXA="))
    televisioonilink = get_live("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfbGl2ZV9jYXRlZ29yaWVz")%(lehekylg,pordinumber,kasutajanimi,salasona)
    filmilink = vod_channels("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfdm9kX2NhdGVnb3JpZXM=")%(lehekylg,pordinumber,kasutajanimi,salasona)
    andmelink = vod_channels("JXM6JXMvcGFuZWxfYXBpLnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcw==")%(lehekylg,pordinumber,kasutajanimi,salasona)
    uuenduslink = get_live("aHR0cHM6Ly93d3cuZHJvcGJveC5jb20vcy83ZW0yNHdkMXBkZGlkcW8vdmVyc2lvbi50eHQ/ZGw9MQ==")
    #if get_live("T25lIFZpZXc=") not in open(addonDir+"/"+sync_data("YWRkb24ueG1s")).read():
       #check_user()
    params = plugintools.get_params()
    
    if params.get("action") is None:
        peamenyy(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()

def peamenyy(params):
    plugintools.log(pnimi+vod_channels("TWFpbiBNZW51")+repr(params))
    load_channels()
    if not lehekylg:
       plugintools.open_settings_dialog()
    if uuendused == "true":
       kontrolli_uuendusi()
    channels = kontroll()
    if channels == 1 and orig.mode != 5:
       plugintools.log(pnimi+vod_channels("TG9naW4gU3VjY2Vzcw=="))
       plugintools.add_item( action=vod_channels("c2VjdXJpdHlfY2hlY2s="),  title="live TV" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
       plugintools.add_item( action=vod_channels("ZGV0ZWN0X21vZGlmaWNhdGlvbg=="),   title="VOD" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("dm9kLnBuZw==")) , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
       plugintools.addItem('Launch PVR','pvr',12,orig.Images + 'extras.png',orig.Images + 'background.png')
       orig.AddDir('Clear Cache','Clear Cache',7,orig.Images + 'clear.png')
       plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjaw=="), title="[COLOR yellow][B][I]Settings[/I][/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bG9nby5wbmc=")) , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")), folder=False )
       plugintools.addItem('[COLOR yellow][B][I]Click to Setup PVR SIMPLE CLIENT[/I][/B][/COLOR]','pvr',11,orig.Images + 'extras.png',orig.Images + 'background.png')
	   
    elif orig.mode != 5:
       plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjaw=="),  title="[COLOR yellow][B]Click here to enter login[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bG9nby5wbmc=")) , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )

       orig.AddDir('[COLOR yellow][B]Click here to refresh after login details have been entered[/B][/COLOR]','Clear Cache',7,orig.Images + 'logo.png')
    if plugintools.get_setting("improve")=="true":
        tseaded = xbmc.translatePath(sync_data("c3BlY2lhbDovL3VzZXJkYXRhL2FkdmFuY2Vkc2V0dGluZ3MueG1s"))
        if not os.path.exists(tseaded):
            file = open( os.path.join(plugintools.get_runtime_path(),vod_channels("cmVzb3VyY2Vz"),sync_data("YWR2YW5jZWRzZXR0aW5ncy54bWw=")) )
            data = file.read()
            file.close()
            file = open(tseaded,"w")
            file.write(data)
            file.close()
            plugintools.message(pnimi, get_live("TmV3IGFkdmFuY2VkIHN0cmVhbWluZyBzZXR0aW5ncyBhZGRlZC4="))



def license_check(params):
    plugintools.log(pnimi+get_live("U2V0dGluZ3MgbWVudQ==")+repr(params))
    plugintools.open_settings_dialog()
def security_check(params):
    plugintools.log(pnimi+sync_data("TGl2ZSBNZW51")+repr(params))
    request = urllib2.Request(televisioonilink, headers={"Accept" : "application/xml"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        kanalinimi = channel.find(get_live("dGl0bGU=")).text
        kanalinimi = base64.b64decode(kanalinimi)
        a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx', '18+'
        if showxxx == "false":
          if any(s in kanalinimi for s in a):
            return
        kategoorialink = channel.find(vod_channels("cGxheWxpc3RfdXJs")).text
        plugintools.add_item( action=get_live("c3RyZWFtX3ZpZGVv"), title="[COLOR red][B][I]"+kanalinimi+"[/I][/B][/COLOR]" , url=kategoorialink , thumbnail=os.path.join(LOAD_LIVE,sync_data("bG9nby5wbmc=")) , fanart="" , folder=True )
    plugintools.set_view( plugintools.LIST )
def detect_modification(params):
    plugintools.log(pnimi+vod_channels("Vk9EIE1lbnUg")+repr(params))        
    request = urllib2.Request(filmilink, headers={"Accept" : "application/xml"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        filminimi = channel.find(get_live("dGl0bGU=")).text
        filminimi = base64.b64decode(filminimi)
        kategoorialink = channel.find(vod_channels("cGxheWxpc3RfdXJs")).text
        plugintools.add_item( action=vod_channels("Z2V0X215YWNjb3VudA=="), title=filminimi , url=kategoorialink , thumbnail = "" , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=True )
    plugintools.set_view( plugintools.LIST )
def stream_video(params):
    alreadyinput = False
    plugintools.log(pnimi+sync_data("TGl2ZSBDaGFubmVscyBNZW51IA==")+repr(params))
    #if get_live("T25lIFZpZXc=") not in open(addonDir+"/"+sync_data("YWRkb24ueG1s")).read():
       #check_user()
    #if vanemalukk == "true":
     #  pealkiri = params.get(sync_data("dGl0bGU="))
      # vanema_lukk(pealkiri)
    url = params.get(get_live("dXJs"))
    request = urllib2.Request(url, headers={"Accept" : "application/xml"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        kanalinimi = channel.find(get_live("dGl0bGU=")).text
        kanalinimi = base64.b64decode(kanalinimi)
        kanalinimi = kanalinimi.partition("[")
        striimilink = channel.find(get_live("c3RyZWFtX3VybA==")).text
        pilt = channel.find(vod_channels("ZGVzY19pbWFnZQ==")).text
        kava = kanalinimi[1]+kanalinimi[2]
        kava = kava.partition("]")
        kava = kava[2]
        kava = kava.partition("   ")
        kava = kava[2]
        shou = get_live("W0NPTE9SIHN0ZWVsYmx1ZV0lcyBbL0NPTE9SXQ==")%(kanalinimi[0])+"- [COLOR gold]" + kava + "[/COLOR]"
        kirjeldus = channel.find(sync_data("ZGVzY3JpcHRpb24=")).text
        if kirjeldus:
           kirjeldus = base64.b64decode(kirjeldus)
           nyyd = kirjeldus.partition("(")
           nyyd = sync_data("Tk9XOiA=") +nyyd[0]
           jargmine = kirjeldus.partition(")\n")
           jargmine = jargmine[2].partition("(")
           jargmine = sync_data("TkVYVDog") +jargmine[0]
           kokku = nyyd+jargmine
        else:
           kokku = ""
        a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx', '18+'
        if vanemalukk == "true":
          if alreadyinput != True:
            if any(s in shou for s in a):
                xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock Enabled!", "Channels may contain adult content", 2000)'))
                dialog = xbmcgui.Dialog()
                text = dialog.input(get_live('UGFyZW50YWwtTG9jazogUGxlYXNlIGVudGVyIHlvdXIgUGFyZW50YWwgQ29kZQ=='), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                if text!=plugintools.get_setting(sync_data("dmFuZW1ha29vZA==")):
                    xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock Error!", "Incorrect code!", 3000)'))
                    return
                else:
                    alreadyinput = True
        if pilt:
           plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=striimilink, thumbnail=pilt, plot=kokku, fanart=os.path.join(LOAD_LIVE,vod_channels("aG9tZXRoZWF0ZXIuanBn")), extra="", isPlayable=True, folder=False )
        else:
           plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,sync_data("bG9nby5wbmc=")) , plot=kokku, fanart=os.path.join(LOAD_LIVE,sync_data("aG9tZXRoZWF0ZXIuanBn")) , extra="", isPlayable=True, folder=False )
    if sync_data('Y2F0X2lkPTM=') in url:
      plugintools.set_view( plugintools.EPISODES )
    else:
      plugintools.set_view( plugintools.EPISODES )
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
def get_myaccount(params):
        plugintools.log(pnimi+get_live("Vk9EIGNoYW5uZWxzIG1lbnUg")+repr(params))
        #if vanemalukk == "true":
           #pealkiri = params.get(sync_data("dGl0bGU="))
           #vanema_lukk(pealkiri)
        purl = params.get(get_live("dXJs"))
        request = urllib2.Request(purl, headers={"Accept" : "application/xml"})
        u = urllib2.urlopen(request)
        tree = ElementTree.parse(u)
        rootElem = tree.getroot()
        for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
            pealkiri = channel.find(get_live("dGl0bGU=")).text
            pealkiri = base64.b64decode(pealkiri)
            pealkiri = pealkiri.encode("utf-8")
            striimilink = channel.find(sync_data("c3RyZWFtX3VybA==")).text
            pilt = channel.find(sync_data("ZGVzY19pbWFnZQ==")).text
            kirjeldus = channel.find(vod_channels("ZGVzY3JpcHRpb24=")).text
            if kirjeldus:
               kirjeldus = base64.b64decode(kirjeldus) 
            if pilt:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=pilt, plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,"theater.jpg") , extra="", isPlayable=True, folder=False )
            else:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,"noposter.jpg"), plot=kirjeldus, fanart="" , extra="", isPlayable=True, folder=False )
        plugintools.set_view( plugintools.MOVIES )
        xbmc.executebuiltin('Container.SetViewMode(515)')


def run_cronjob(params):
    extend=plugintools.get_setting(vod_channels("ZXh0ZW5k"))
    plugintools.log(pnimi+sync_data("UExBWV9MSVZF")+repr(params))
    #if vanemalukk == "true":
       #pealkiri = params.get(sync_data("dGl0bGU="))
       #vanema_lukk(pealkiri)
    lopplink = params.get(vod_channels("dXJs"))
    lopplink = lopplink.replace('.ts','.%s'%extend)
    plugintools.play_resolved_url( lopplink )
	
def run_cronjobxxx(params):
    kasutajanimi=plugintools.get_setting("Username")
    salasona=plugintools.get_setting("Password")
    lopplink = params.get("url")
    if "http://"  not in lopplink: 
        lopplink = get_live("aHR0cDovL290dHR2LmdhOjIwOTUvbGl2ZS8lcy8lcy8lcw==")%(kasutajanimi,salasona,lopplink)
        lopplink = lopplink[:-2]
        lopplink = lopplink + "m3u8"
    listitem = xbmcgui.ListItem(path=lopplink)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)




def sync_data(channel):
    video = base64.b64decode(channel)
    return video


def restart_service(params):
    lopplink = params.get(vod_channels("dXJs"))
    plugintools.play_resolved_url( lopplink )



def grab_epg():
    req = urllib2.Request(andmelink)
    req.add_header(sync_data("VXNlci1BZ2VudA==") , vod_channels("S29kaSBwbHVnaW4gYnkgTWlra00="))
    response = urllib2.urlopen(req)
    link=response.read()
    jdata = json.loads(link.decode('utf8'))
    response.close()
    if jdata:
       plugintools.log(pnimi+sync_data("amRhdGEgbG9hZGVkIA=="))
       return jdata
def kontroll():
    randomstring = grab_epg()
    kasutajainfo = randomstring[sync_data("dXNlcl9pbmZv")]
    kontroll = kasutajainfo[get_live("YXV0aA==")]
    return kontroll
def get_live(channel):
    video = base64.b64decode(channel)
    return video
def execute_ainfo(params):
    plugintools.log(pnimi+get_live("TXkgYWNjb3VudCBNZW51IA==")+repr(params))
    andmed = grab_epg()
    kasutajaAndmed = andmed[sync_data("dXNlcl9pbmZv")]
    seis = kasutajaAndmed[get_live("c3RhdHVz")]
    aegub = kasutajaAndmed[sync_data("ZXhwX2RhdGU=")]
    if aegub:
       aegub = datetime.datetime.fromtimestamp(int(aegub)).strftime('%d/%m/%Y %H:%M')
    else:
       aegub = vod_channels("TmV2ZXI=")
    leavemealone = kasutajaAndmed[get_live("bWF4X2Nvbm5lY3Rpb25z")]
    polarbears = kasutajaAndmed[sync_data("dXNlcm5hbWU=")]
    plugintools.add_item( action="",   title=sync_data("W0NPTE9SID0gd2hpdGVdVXNlcjogWy9DT0xPUl0=")+polarbears , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
    plugintools.add_item( action="",   title=sync_data("W0NPTE9SID0gd2hpdGVdU3RhdHVzOiBbL0NPTE9SXQ==")+seis , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
    plugintools.add_item( action="",   title=get_live("W0NPTE9SID0gd2hpdGVdRXhwaXJlczogWy9DT0xPUl0=")+aegub , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
    plugintools.add_item( action="",   title=vod_channels("W0NPTE9SID0gd2hpdGVdTWF4IGNvbm5lY3Rpb25zOiBbL0NPTE9SXQ==")+leavemealone , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
    plugintools.add_item( action="",   title=vod_channels("U2lnbiB1cCBhdCBGdXR1cmVTdHJlYW1zLnRr") , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	
    plugintools.set_view( plugintools.LIST )
def vanema_lukk(name):
        plugintools.log(pnimi+sync_data("UGFyZW50YWwgbG9jayA="))
        a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx', '18+'
        if any(s in name for s in a):
           xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock", "Channels may contain adult content", 2000)'))
           text = plugintools.keyboard_input(default_text="", title=get_live("UGFyZW50YWwtTG9jazogUGxlYXNlIGVudGVyIHlvdXIgUGFyZW50YWwgQ29kZQ=="))
           if text==plugintools.get_setting(sync_data("dmFuZW1ha29vZA==")):
              return
           else:
              exit()
        else:
           name = ""
def kontrolli_uuendusi():
        req = urllib2.Request(uuenduslink)
        req.add_header(vod_channels("VXNlci1BZ2VudA==") , sync_data("S29kaSBwbHVnaW4gYnkgTWlra00="))
        response = urllib2.urlopen(req)
        repoversion=response.read()
        repoversion = repoversion.partition("\n")
        iversion = repoversion[1]
        global dlink
        dlink = repoversion[2]
        response.close()
        if iversion <> version:
           update = " "
        else:
           if plugintools.message_yes_no(pnimi,sync_data("TmV3IHVwZGF0ZSBpcyBhdmFpbGFibGUh"),get_live("RG8geW91IHdhbnQgdG8gdXBkYXRlIHBsdWdpbiBub3c/")):
              plugintools.log( pnimi+vod_channels("VHJ5aW5nIHRvIHVwZGF0ZSBwbHVnaW4uLi4="))
              try:
                  destpathname = xbmc.translatePath(os.path.join(sync_data("c3BlY2lhbDovLw=="),sync_data("aG9tZS9hZGRvbnMv")))
                  local_file_name = os.path.join( plugintools.get_runtime_path() , get_live("dXBkYXRlLnppcA==") )
                  plugintools.log(pnimi+local_file_name)
                  urllib.urlretrieve(dlink, local_file_name )
                  DownloaderClass(dlink,local_file_name)
                  plugintools.log(pnimi+sync_data("RXh0cmFjdGluZyB1cGRhdGUuLi4="))
                  import ziptools
                  unzipper = ziptools.ziptools()
                  #destpathname = xbmc.translatePath(os.path.join('special://','home'))
                  plugintools.log(pnimi+destpathname)
                  unzipper.extract( local_file_name , destpathname )
                  os.remove(local_file_name)
                  xbmc.executebuiltin((u'XBMC.Notification("Updated", "The add-on has been updated", 2000)'))
                  #import updater
                  xbmc.executebuiltin( "Container.Refresh" )
                  plugintools.log(pnimi+get_live("VXBkYXRlIHN1Y2Nlc3M="))
              except:
                  plugintools.log(pnimi+get_live("VXBkYXRlIGZhaWxlZA=="))
                  xbmc.executebuiltin((u'XBMC.Notification("Not updated", "An error causes the update to fail", 2000)'))
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create(sync_data("R2V0dGluZyB1cGRhdGU="),get_live("RG93bmxvYWRpbmc="))
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
def check_user():
    plugintools.message(get_live("RVJST1I="),vod_channels("VU5BVVRIT1JJWkVEIEVESVQgT0YgQURET04h"))
    sys.exit()
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()
def load_channels():
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("YmFja2dyb3VuZC5wbmc="))

def vod_channels(channel):
    video = base64.b64decode(channel)
    return video
run()

