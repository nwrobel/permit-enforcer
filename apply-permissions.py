'''
Main script for permissions application project.
'''

import os
import csv
import logging

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.file

if __name__ == '__main__':

    thisDir = mypycommons.file.getThisScriptCurrentDirectory() 
    configFilePath = mypycommons.file.JoinPaths(thisDir, 'permissions.csv')
    logFilePath = '/var/log/permit-enforcer.log'

    logging.basicConfig(filename=logFilePath, level=logging.INFO)

    logging.info("Starting file permission application script")
    logging.info("Reading permission config file: {}".format(configFilePath))

    permissionRules = mypycommons.file.readCSVFile(configFilePath)
    currentLine = 1

    for rule in permissionRules:
        logging.info("Applying permission rule #{}: {} ({}:{} {})".format(currentLine, rule['path'], rule['owner'], rule['group'], rule['mask']))
        mypycommons.file.applyPermissionToPath(rule['path'], rule['owner'], rule['group'], rule['mask'])

        currentLine += 1

    logging.info("All permission rules finished applying, script completed successfully")
       

