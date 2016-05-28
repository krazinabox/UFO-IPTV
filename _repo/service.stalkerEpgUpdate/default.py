import resources.lib.utils as utils
from service import epgUpdater

#run the program
utils.log("Update Library Service starting...")
epgUpdater().setup()
