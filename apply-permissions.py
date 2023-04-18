'''
Main script for permissions application project.
'''

import os
import csv
import logging

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.file
import com.nwrobel.mypycommons.logger

def getProjectLogsDir():
    currentDir = mypycommons.file.getThisScriptCurrentDirectory()
    logsDir = mypycommons.file.joinPaths(currentDir, '~logs')

    if (not mypycommons.file.pathExists(logsDir)):
        mypycommons.file.createDirectory(logsDir)
    
    return logsDir

if __name__ == '__main__':

    configFilePath = '/datastore/nick/Development/Projects/permit-enforcer/config/permissions-zinc.csv'

    # Set up logger
    mypycommons.logger.configureLoggerWithBasicSettings(__name__, logFilename='apply-permissions.log', logDir=getProjectLogsDir())
    mypycommons.logger.setLoggerConsoleOutputLogLevel(__name__, mypycommons.logger.LogLevel.INFO)
    mypycommons.logger.setLoggerFileOutputLogLevel(__name__, mypycommons.logger.LogLevel.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting file permission application script")
    logger.info("Reading permission config file: {}".format(configFilePath))

    permissionRules = mypycommons.file.readCSVFile(configFilePath)
    currentLine = 1

    for rule in permissionRules:
        if (rule['recursive'] == '0'):
            useRecursive = False
        elif (rule['recursive'] == '1'):
            useRecursive = True
        else:
            raise "Invalid value for CSV column 'recursive': should be 0 or 1"

        logger.info("Applying permission rule #{}: {} ({}:{}, {}, Recursive={})".format(currentLine, rule['path'], rule['owner'], rule['group'], rule['mask'], useRecursive))

        mypycommons.file.applyPermissionToPath(rule['path'], rule['owner'], rule['group'], rule['mask'], recursive=useRecursive)
        currentLine += 1

    logger.info("All permission rules finished applying, script completed successfully")
       

