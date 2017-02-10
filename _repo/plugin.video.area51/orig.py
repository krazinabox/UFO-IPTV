import urllib as OO0O00O00OOO0000O ,urllib2 as OOO0OO0OO0O0OOOOO ,sys as O00OO0OOOO0O00OO0 ,xbmcplugin as O00O0OOOOOOO00OO0 ,xbmcgui as O0OOOO00O0OO0OO00 ,xbmcaddon as OO0O00O0OOO0OOOOO ,xbmc as O0O00000OOO000O00 ,os as O0OOOOO0000000OO0 ,json as O000OOOOOO00O0OO0 ,re as O0000O0OOOOOO0000 #line:1
import common as O000000OO00OO0OO0 ,xbmcvfs as OOOOOO0OO0OO00O00 ,zipfile as O00000000000OOOO0 ,downloader as O00O0O0OO000O0OO0 ,extract as OOOO0O00O00OOO000 #line:2
import GoDev as OO0OOO000O000000O #line:3
from datetime import datetime as O0OO0OO0O0OO000O0 ,timedelta as O0O00O000OOOOOOO0 #line:4
import base64 as OO00OO0O0O00000OO ,time as OOO0OO00O000OO00O #line:5
AddonID ='plugin.video.area51'#line:6
Addon =OO0O00O0OOO0OOOOO .Addon (AddonID )#line:7
ADDON =OO0O00O0OOO0OOOOO .Addon (id ='plugin.video.area51')#line:8
Username =O00O0OOOOOOO00OO0 .getSetting (int (O00OO0OOOO0O00OO0 .argv [1 ]),'Username')#line:10
Password =O00O0OOOOOOO00OO0 .getSetting (int (O00OO0OOOO0O00OO0 .argv [1 ]),'Password')#line:11
ServerURL ="http://iptv-reseller.xyz/get.php?username=%s&password=%s&type=m3u&output=hls"%(Username ,Password ,)#line:12
AccLink ="http://iptv-reseller.xyz/panel_api.php?username=%s&password=%s"%(Username ,Password ,)#line:13
addonDir =Addon .getAddonInfo ('path').decode ("utf-8")#line:14
Images =O0O00000OOO000O00 .translatePath (O0OOOOO0000000OO0 .path .join ('special://home','addons',AddonID ,'resources/'));#line:15
addon_data_dir =O0OOOOO0000000OO0 .path .join (O0O00000OOO000O00 .translatePath ("special://userdata/addon_data").decode ("utf-8"),AddonID )#line:16
if not O0OOOOO0000000OO0 .path .exists (addon_data_dir ):#line:17
    O0OOOOO0000000OO0 .makedirs (addon_data_dir )#line:18
def OPEN_URL (OO0O00000O0O00O00 ):#line:19
    OOO00OO0OOO000O0O =OOO0OO0OO0O0OOOOO .Request (OO0O00000O0O00O00 )#line:20
    OOO00OO0OOO000O0O .add_header ('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')#line:21
    OOOOO00O00O0OOO0O =OOO0OO0OO0O0OOOOO .urlopen (OOO00OO0OOO000O0O )#line:22
    OO000O0O0O0OOOO0O =OOOOO00O00O0OOO0O .read ()#line:23
    OOOOO00O00O0OOO0O .close ()#line:24
    return OO000O0O0O0OOOO0O #line:25
def Open_URL (OOO00OO0000OO000O ):#line:26
        O0OOO0O0O0O00OO0O =OOO0OO0OO0O0OOOOO .Request (url )#line:27
        O0OOO0O0O0O00OO0O .add_header ('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')#line:29
        OO0OOOO0OO0OOO0OO =OOO0OO0OO0O0OOOOO .urlopen (O0OOO0O0O0O00OO0O )#line:30
        OO0OOO00O000O00OO =OO0OOOO0OO0OOO0OO .read ()#line:31
        OO0OOOO0OO0OOO0OO .close ()#line:32
        return OO0OOO00O000O00OO #line:33
def MainMenu ():#line:34
        AddDir ('My Account',AccLink ,1 ,Images +'MyAcc.png')#line:35
        AddDir ('Live TV','url',2 ,Images +'Live TV.png')#line:36
        AddDir ('Movies (Coming Soon)','Movies',8 ,Images +'movies.png')#line:37
        AddDir ('TVShows (Coming Soon)','TVshows',9 ,Images +'tvshows.png')#line:38
        AddDir ('Extras','Extras',5 ,Images +'extras.png')#line:39
        AddDir ('Clear Cache','Clear Cache',7 ,Images +'cache.png')#line:40
        AddDir ('Settings','settings',4 ,Images +'settings.png')#line:41
def LiveTv (O000OO0O00O0OO00O ):#line:42
    O00O0O00OOOOO0OO0 =O000000OO00OO0OO0 .m3u2list (ServerURL )#line:43
    for O0OO0O0O00O0O00O0 in O00O0O00OOOOO0OO0 :#line:44
        O0000O0OO0O0OO0OO =O000000OO00OO0OO0 .GetEncodeString (O0OO0O0O00O0O00O0 ["display_name"])#line:45
        AddDir (O0000O0OO0O0OO0OO ,O0OO0O0O00O0O00O0 ["url"],3 ,iconimage ,isFolder =False )#line:46
def MyAccDetails (O0O00OO000OO00000 ):#line:47
        O0OO0OOO00OO0OOO0 =Open_URL (O0O00OO000OO00000 )#line:48
        OOOO0O0O00O0000O0 =O0000O0OOOOOO0000 .compile ('"username":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:49
        OOO00OO00O0OOO000 =O0000O0OOOOOO0000 .compile ('"status":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:50
        OO000OO00OOO0OO00 =O0000O0OOOOOO0000 .compile ('"exp_date":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:51
        O00O000O0OO0OO000 =O0000O0OOOOOO0000 .compile ('"active_cons":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:52
        O0OOOOOOO0O0O000O =O0000O0OOOOOO0000 .compile ('"created_at":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:53
        O000OOO0O0OOO000O =O0000O0OOOOOO0000 .compile ('"max_connections":"(.+?)"').findall (O0OO0OOO00OO0OOO0 )#line:54
        O0OOOOO0O0O00O0OO =O0000O0OOOOOO0000 .compile ('"is_trial":"1"').findall (O0OO0OOO00OO0OOO0 )#line:55
        for O0O00OO000OO00000 in OOOO0O0O00O0000O0 :#line:56
                AddAccInfo ('My Account Information','','',Images +'MyAcc.png')#line:57
                AddAccInfo ('Username:  %s'%(O0O00OO000OO00000 ),'','',Images +'MyAcc.png')#line:58
        for O0O00OO000OO00000 in OOO00OO00O0OOO000 :#line:59
                AddAccInfo ('Status:  %s'%(O0O00OO000OO00000 ),'','',Images +'MyAcc.png')#line:60
        for O0O00OO000OO00000 in O0OOOOOOO0O0O000O :#line:61
                O00O00000OO00OOO0 =O0OO0OO0O0OO000O0 .fromtimestamp (float (O0OOOOOOO0O0O000O [0 ]))#line:62
                O00O00000OO00OOO0 .strftime ('%Y-%m-%d %H:%M:%S')#line:63
                AddAccInfo ('Created:  %s'%(O00O00000OO00OOO0 ),'','',Images +'MyAcc.png')#line:64
        for O0O00OO000OO00000 in OO000OO00OOO0OO00 :#line:65
                O00O00000OO00OOO0 =O0OO0OO0O0OO000O0 .fromtimestamp (float (OO000OO00OOO0OO00 [0 ]))#line:66
                O00O00000OO00OOO0 .strftime ('%Y-%m-%d %H:%M:%S')#line:67
                AddAccInfo ('Expires:  %s'%(O00O00000OO00OOO0 ),'','',Images +'MyAcc.png')#line:68
        for O0O00OO000OO00000 in O00O000O0OO0OO000 :#line:69
                AddAccInfo ('Active Connection:  %s'%(O0O00OO000OO00000 ),'','',Images +'MyAcc.png')#line:70
        for O0O00OO000OO00000 in O000OOO0O0OOO000O :#line:71
                AddAccInfo ('Max Connection:  %s'%(O0O00OO000OO00000 ),'','',Images +'MyAcc.png')#line:72
        for O0O00OO000OO00000 in O0OOOOO0O0O00O0OO :#line:73
                AddAccInfo ('Trial: Yes','','',Images +'MyAcc.png')#line:74
def PlayUrl (OOOO0O0O0O0O0OO00 ,OO000OO0OO00O00OO ,iconimage =None ):#line:76
        _O00OO0O0OO00000O0 =OOOO0O0O0O0O0OO00 #line:77
        O0OO00OOOO00O00O0 =O000000OO00OO0OO0 .m3u2list (ServerURL )#line:78
        for O0OO0O00000OO0O00 in O0OO00OOOO00O00O0 :#line:79
            OOOO0O0O0O0O0OO00 =O000000OO00OO0OO0 .GetEncodeString (O0OO0O00000OO0O00 ["display_name"])#line:80
            OOO0O0OOO0O0OO00O =O0OO0O00000OO0O00 ["url"]#line:81
            if _O00OO0O0OO00000O0 in OOOO0O0O0O0O0OO00 :#line:82
                OOO0OOOOO000OO0OO =O0OOOO00O0OO0OO00 .ListItem (path =OOO0O0OOO0O0OO00O ,thumbnailImage =iconimage )#line:83
                OOO0OOOOO000OO0OO .setInfo (type ="Video",infoLabels ={"Title":OOOO0O0O0O0O0OO00 })#line:84
                O00O0OOOOOOO00OO0 .setResolvedUrl (int (O00OO0OOOO0O00OO0 .argv [1 ]),True ,OOO0OOOOO000OO0OO )#line:85
def AddAccInfo (O000O0O0O0OO000O0 ,OO00OO00OO00O0O00 ,OO00O0000O00OOO0O ,O00O0000OO0O0OO0O ):#line:86
        OOOOO0000O000O000 =O00OO0OOOO0O00OO0 .argv [0 ]+"?url="+OO0O00O00OOO0000O .quote_plus (OO00OO00OO00O0O00 )+"&mode="+str (OO00O0000O00OOO0O )+"&name="+OO0O00O00OOO0000O .quote_plus (O000O0O0O0OO000O0 )#line:87
        O0OO0O000OOOO0OO0 =True #line:88
        OO0OOOO0O0OOOOO0O =O0OOOO00O0OO0OO00 .ListItem (O000O0O0O0OO000O0 ,iconImage ="DefaultFolder.png",thumbnailImage =O00O0000OO0O0OO0O )#line:89
        OO0OOOO0O0OOOOO0O .setInfo (type ="Video",infoLabels ={"Title":O000O0O0O0OO000O0 })#line:90
        O0OO0O000OOOO0OO0 =O00O0OOOOOOO00OO0 .addDirectoryItem (handle =int (O00OO0OOOO0O00OO0 .argv [1 ]),url =OOOOO0000O000O000 ,listitem =OO0OOOO0O0OOOOO0O ,isFolder =False )#line:91
def AddDir (OO0O00OO000O00OOO ,OOOOO00OO0OOO0000 ,O0OO00OO0O0OOOOO0 ,O0O0O000OO0OO0O00 ,description ="",isFolder =True ,background =None ):#line:92
    O000O00OO000OO000 =O00OO0OOOO0O00OO0 .argv [0 ]+"?url="+OO0O00O00OOO0000O .quote_plus (OOOOO00OO0OOO0000 )+"&mode="+str (O0OO00OO0O0OOOOO0 )+"&name="+OO0O00O00OOO0000O .quote_plus (OO0O00OO000O00OOO )+"&iconimage="+OO0O00O00OOO0000O .quote_plus (O0O0O000OO0OO0O00 )+"&description="+OO0O00O00OOO0000O .quote_plus (description )#line:93
    OO0OO0000O000O00O =O00OO0OOOO0O00OO0 .argv [0 ]+"?url=None&mode="+str (O0OO00OO0O0OOOOO0 )+"&name="+OO0O00O00OOO0000O .quote_plus (OO0O00OO000O00OOO )+"&iconimage="+OO0O00O00OOO0000O .quote_plus (O0O0O000OO0OO0O00 )+"&description="+OO0O00O00OOO0000O .quote_plus (description )#line:94
    OOOO0OO00O0000O00 =O0OOOO00O0OO0OO00 .ListItem (OO0O00OO000O00OOO ,iconImage =O0O0O000OO0OO0O00 ,thumbnailImage =O0O0O000OO0OO0O00 )#line:96
    OOOO0OO00O0000O00 .setInfo (type ="Video",infoLabels ={"Title":OO0O00OO000O00OOO ,"Plot":description })#line:97
    OOOO0OO00O0000O00 .setProperty ('IsPlayable','true')#line:98
    O00O0OOOOOOO00OO0 .addDirectoryItem (handle =int (O00OO0OOOO0O00OO0 .argv [1 ]),url =O000O00OO000OO000 ,listitem =OOOO0OO00O0000O00 ,isFolder =isFolder )#line:99
def Get_Params ():#line:100
    O0O0OO0OO0O0OO00O =[]#line:101
    O0O00000OO00O0O00 =O00OO0OOOO0O00OO0 .argv [2 ]#line:102
    if len (O0O00000OO00O0O00 )>=2 :#line:103
        OOOO0O0O0OO0O0OO0 =O00OO0OOOO0O00OO0 .argv [2 ]#line:104
        O0OO0OOOOOOOOO000 =OOOO0O0O0OO0O0OO0 .replace ('?','')#line:105
        if (OOOO0O0O0OO0O0OO0 [len (OOOO0O0O0OO0O0OO0 )-1 ]=='/'):#line:106
            OOOO0O0O0OO0O0OO0 =OOOO0O0O0OO0O0OO0 [0 :len (OOOO0O0O0OO0O0OO0 )-2 ]#line:107
        OO0O00O00O0O0OOOO =O0OO0OOOOOOOOO000 .split ('&')#line:108
        O0O0OO0OO0O0OO00O ={}#line:109
        for OO0O00O0OO0OO0O0O in range (len (OO0O00O00O0O0OOOO )):#line:110
            O00OO0O00O0OO00O0 ={}#line:111
            O00OO0O00O0OO00O0 =OO0O00O00O0O0OOOO [OO0O00O0OO0OO0O0O ].split ('=')#line:112
            if (len (O00OO0O00O0OO00O0 ))==2 :#line:113
                O0O0OO0OO0O0OO00O [O00OO0O00O0OO00O0 [0 ].lower ()]=O00OO0O00O0OO00O0 [1 ]#line:114
    return O0O0OO0OO0O0OO00O #line:115
def correctPVR ():#line:117
	OOOO00O0O00OOOO0O =OO0O00O0OOO0OOOOO .Addon ('plugin.video.area51')#line:119
	O0000OO0OO0O00O0O =OOOO00O0O00OOOO0O .getSetting (id ='Username')#line:120
	O00O0OO0O000O0O0O =OOOO00O0O00OOOO0O .getSetting (id ='Password')#line:121
	O000O00OOO000O00O ='{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'#line:122
	OO0OOO00OO00O0O0O ='{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'#line:123
	OO0OOOOO00000O0OO ='{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'#line:124
	OOOOO0O00O00OO000 ="http://iptv-reseller.xyz:2095/get.php?username="+O0000OO0OO0O00O0O +"&password="+O00O0OO0O000O0O0O +"&type=m3u_plus&output=ts"#line:125
	O00OOOO0OO000OO0O ="http://iptv-reseller.xyz:2095/xmltv.php?username="+O0000OO0OO0O00O0O +"&password="+O00O0OO0O000O0O0O +"&type=m3u_plus&output=ts"#line:126
	O0O00000OOO000O00 .executeJSONRPC (O000O00OOO000O00O )#line:128
	O0O00000OOO000O00 .executeJSONRPC (OO0OOO00OO00O0O0O )#line:129
	O0O00000OOO000O00 .executeJSONRPC (OO0OOOOO00000O0OO )#line:130
	OO00OO0O0O0OOOOOO =OO0O00O0OOO0OOOOO .Addon ('pvr.iptvsimple')#line:132
	OO00OO0O0O0OOOOOO .setSetting (id ='m3uUrl',value =OOOOO0O00O00OO000 )#line:133
	OO00OO0O0O0OOOOOO .setSetting (id ='epgUrl',value =O00OOOO0OO000OO0O )#line:134
	OO00OO0O0O0OOOOOO .setSetting (id ='m3uCache',value ="false")#line:135
	OO00OO0O0O0OOOOOO .setSetting (id ='epgCache',value ="false")#line:136
	OO0OO000O0O00O000 =O0OOOO00O0OO0OO00 .Dialog ().ok ("[COLOR white]PVR SETUP DONE[/COLOR]",'[COLOR white]We\'ve copied your AREA 51 to the PVR Guide[/COLOR]',' ','[COLOR white]This includes the EPG please allow time to populate now click launch PVR[/COLOR]')#line:137
def LaunchPVR ():#line:140
	O0O00000OOO000O00 .executebuiltin ('ActivateWindow(TVGuide)')#line:141
def OpenSettings ():#line:143
    ADDON .openSettings ()#line:144
    MainMenu ()#line:145
def Clear_Cache ():#line:146
    OOO00000OO0OOO0OO =O0OOOO00O0OO0OO00 .Dialog ().yesno ('Clear your Cache?','If you still cant see your account after ok button is clicked your details are incorrect',nolabel ='Cancel',yeslabel ='OK')#line:147
    if OOO00000OO0OOO0OO ==1 :#line:148
        OO0OOO000O000000O .Wipe_Cache ()#line:149
def wizard2 ():#line:151
    O0000000OOOOOOOO0 =gettextdata ('http://fix4u.tech/ottserver/update.txt')#line:152
    O0O0O0O0OO0O0O000 =O0OOOO00O0OO0OO00 .Dialog ()#line:153
    O0O0O0O0OO0O0O000 .ok ("Sporting Info",O0000000OOOOOOOO0 ,"","")#line:154
def wizard3 ():#line:156
	OO0OO0000OO00O00O =O0OOOO00O0OO0OO00 .Dialog ()#line:157
	OOOOOOOO0OOOOOOOO =O0O00000OOO000O00 .translatePath ('special://home/addons')#line:158
	O0OO00OO0O0O000OO =O0OOOOO0000000OO0 .listdir (OOOOOOOO0OOOOOOOO )#line:159
	if 'plugin.video.testpiece'in O0OO00OO0O0O000OO :#line:160
		O0O00000OOO000O00 .executebuiltin ('RunAddon(plugin.video.testpiece)')#line:161
	else :#line:162
		OO0OO0000OO00O00O .ok ('Not Installed','You need ivue guide in order to use this')#line:163
def addXMLMenu (O00OO000OO0O0O000 ,O0OO00O0OO0000OO0 ,OO000OOO0O0OO000O ,OO0OOO000OO0OOOO0 ,OO000O0O0OOOO0000 ,O0O00OO0000O0OOOO ):#line:165
        O000000O0OO0OO000 =O00OO0OOOO0O00OO0 .argv [0 ]+"?url="+OO0O00O00OOO0000O .quote_plus (O0OO00O0OO0000OO0 )+"&mode="+str (OO000OOO0O0OO000O )+"&name="+OO0O00O00OOO0000O .quote_plus (O00OO000OO0O0O000 )+"&iconimage="+OO0O00O00OOO0000O .quote_plus (OO0OOO000OO0OOOO0 )+"&fanart="+OO0O00O00OOO0000O .quote_plus (OO000O0O0OOOO0000 )+"&description="+OO0O00O00OOO0000O .quote_plus (O0O00OO0000O0OOOO )#line:166
        O000000OOOO00OO00 =True #line:167
        O0OOOOO00OO00O0OO =O0OOOO00O0OO0OO00 .ListItem (O00OO000OO0O0O000 ,iconImage ="DefaultFolder.png",thumbnailImage =OO0OOO000OO0OOOO0 )#line:168
        O0OOOOO00OO00O0OO .setInfo (type ="Video",infoLabels ={"Title":O00OO000OO0O0O000 ,"Plot":O0O00OO0000O0OOOO })#line:169
        O0OOOOO00OO00O0OO .setProperty ("Fanart_Image",OO000O0O0OOOO0000 )#line:170
        O000000OOOO00OO00 =O00O0OOOOOOO00OO0 .addDirectoryItem (handle =int (O00OO0OOOO0O00OO0 .argv [1 ]),url =O000000O0OO0OO000 ,listitem =O0OOOOO00OO00O0OO ,isFolder =False )#line:171
        return O000000OOOO00OO00 #line:172
def ExtraMenu ():#line:173
    O00OOOOO0O000OOO0 =OPEN_URL ('http://46.105.35.189/development/xml/toolboxextras.xml').replace ('\n','').replace ('\r','')#line:174
    OO00O0O0000O0OOOO =O0000O0OOOOOO0000 .compile ('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall (O00OOOOO0O000OOO0 )#line:175
    for O0OOOOO0O0OOOO0OO ,OOOOOO0000OO0O00O ,OOO00O00OO0O00OO0 ,O000O00OOOOOOO00O ,OO00O0O0O0OO00O00 in OO00O0O0000O0OOOO :#line:176
        addXMLMenu (O0OOOOO0O0OOOO0OO ,OOOOOO0000OO0O00O ,6 ,OOO00O00OO0O00OO0 ,O000O00OOOOOOO00O ,OO00O0O0O0OO00O00 )#line:177
def Movies ():#line:178
	OOO0O0O0OOOO0O0OO =O0OOOO00O0OO0OO00 .Dialog ()#line:179
	OOOOO0000OO000O00 =O0O00000OOO000O00 .translatePath ('special://home/addons')#line:180
	O0OOO000OOO00O0OO =O0OOOOO0000000OO0 .listdir (OOOOO0000OO000O00 )#line:181
	if 'plugin.program.fixtures'in O0OOO000OOO00O0OO :#line:182
		O0O00000OOO000O00 .executebuiltin ('RunAddon(plugin.program.fixtures)')#line:183
	else :#line:184
		OOO0O0O0OOOO0O0OO .ok ('Not Installed','You need extended info to use this')#line:185
def TVShows ():#line:187
	O0O0O00O0OO0O0O0O =O0OOOO00O0OO0OO00 .Dialog ()#line:188
	OO000000OOOOOOO00 =O0O00000OOO000O00 .translatePath ('special://home/addons')#line:189
	OO00000OO0000000O =O0OOOOO0000000OO0 .listdir (OO000000OOOOOOO00 )#line:190
	if 'plugin.program.mtvguidepro'in OO00000OO0000000O :#line:191
		O0O00000OOO000O00 .executebuiltin ('RunAddon(plugin.program.mtvguidepro)')#line:192
	else :#line:193
		O0O0O00O0OO0O0O0O .ok ('Not Installed','You need mayfair pro guide in order to use this you can get it from here http://mayfairguides.com/pro')#line:194
def gettextdata (OO0O0OO00000O00O0 ):#line:196
    mayfair_show_busy_dialog ()#line:197
    try :#line:198
        O00OOO00OO0O0OOO0 =OOO0OO0OO0O0OOOOO .Request (OO0O0OO00000O00O0 )#line:199
        OOOO00OOO0O000O0O =OOO0OO0OO0O0OOOOO .urlopen (O00OOO00OO0O0OOO0 )#line:200
        O00O00OOO00OOO00O =OOOO00OOO0O000O0O .read ()#line:201
        OOOO00OOO0O000O0O .close ()#line:202
        mayfair_hide_busy_dialog ()#line:203
        if O00O00OOO00OOO00O =='':#line:204
            O00O00OOO00OOO00O ='No message to display, please check back later!'#line:205
        return O00O00OOO00OOO00O #line:206
    except :#line:207
        import sys as O000O000O000000OO #line:208
        import traceback as O0O0OO0OOOOOO000O #line:209
        (O0O0OOOOOO0O00OO0 ,OO00OOO00OOO0O0O0 ,OOOO0O00O0OOO000O )=O000O000O000000OO .exc_info ()#line:210
        O0O0OO0OOOOOO000O .print_exception (O0O0OOOOOO0O00OO0 ,OO00OOO00OOO0O0O0 ,OOOO0O00O0OOO000O )#line:211
        mayfair_hide_busy_dialog ()#line:212
        OO0O00OOO0O0O0O0O =O0OOOO00O0OO0OO00 .Dialog ()#line:213
        OO0O00OOO0O0O0O0O .ok ("Error!","Error connecting to server!","","Please try again later.")#line:214
def mayfair_show_busy_dialog ():#line:216
    O0O00000OOO000O00 .executebuiltin ('ActivateWindow(10138)')#line:217
def mayfair_hide_busy_dialog ():#line:219
    O0O00000OOO000O00 .executebuiltin ('Dialog.Close(10138)')#line:220
    while O0O00000OOO000O00 .getCondVisibility ('Window.IsActive(10138)'):#line:221
        O0O00000OOO000O00 .sleep (100 )#line:222
params =Get_Params ()#line:227
url =None #line:228
name =None #line:229
mode =None #line:230
iconimage =None #line:231
description =None #line:232
try :url =OO0O00O00OOO0000O .unquote_plus (params ["url"])#line:234
except :pass #line:235
try :name =OO0O00O00OOO0000O .unquote_plus (params ["name"])#line:236
except :pass #line:237
try :iconimage =OO0O00O00OOO0000O .unquote_plus (params ["iconimage"])#line:238
except :pass #line:239
try :mode =int (params ["mode"])#line:240
except :pass #line:241
try :description =OO0O00O00OOO0000O .unquote_plus (params ["description"])#line:242
except :pass #line:243
if mode ==7 :#line:245
	Clear_Cache ()#line:246
elif mode ==8 :#line:247
	Movies ()#line:248
elif mode ==9 :#line:249
	TVShows ()#line:250
elif mode ==1 :#line:251
    MyAccDetails (url )#line:252
elif mode ==2 :#line:253
    LiveTv (url )#line:254
elif mode ==3 :#line:255
    PlayUrl (name ,url ,iconimage )#line:256
elif mode ==4 :#line:257
	OpenSettings ()#line:258
elif mode ==5 :#line:259
	ExtraMenu ()#line:260
elif mode ==6 :#line:261
	wizard2 ()#line:262
elif mode ==10 :#line:263
	wizard3 ()#line:264
elif mode ==11 :#line:265
	correctPVR ()#line:266
elif mode ==12 :#line:267
	LaunchPVR ()
#e9015584e6a44b14988f13e2298bcbf9