import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[COLOR lightgreen]UFOBuilds[/COLOR]'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'http://theuforepo.us/wizard/autobuilds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 3
# Text File with apk info in it.
APKFILE        = 'http://theuforepo.us/wizard/apk.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
# Leave as http:// for default icon
ICONBUILDS     = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONMAINT      = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONAPK        = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONADDONS     = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONYOUTUBE    = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONSAVE       = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONTRAKT      = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONREAL       = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONLOGIN      = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONCONTACT    = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
ICONSETTINGS   = 'https://archive.org/download/krazinabox_gmail_Icon/icon.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'limegreen'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']UFOBuilds[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing UFOBuilds Wizard.\r\n\r\nContact us on Facebook at https://www.facebook.com/groups/363073830770143/'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://firestickplusmancomlu.com/backgrounds/Area-51/icon.png'
CONTACTFANART  = 'http://firestickplusmancomlu.com/backgrounds/Area-51/fanart.jpg'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = 'http://theuforepo.us/wizard/autobuilds.txt'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.ufo-repo'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.github.com/krazinabox/UFO-IPTV/master/_repo/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'http://theuforepo.us/repo/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'http://theuforepo.us/wizard/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = ''
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = 'http://firestickplusmancomlu.com/backgrounds/Area-51/fanart.jpg'
#########################################################