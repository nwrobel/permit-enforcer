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
    logsDir = mypycommons.file.JoinPaths(currentDir, '~logs')

    if (not mypycommons.file.directoryExists(logsDir)):
        mypycommons.file.createDirectory(logsDir)
    
    return logsDir

if __name__ == '__main__':

    mypycommons.logger.initSharedLogger(logFilename='apply-permissions.log', logDir=getProjectLogsDir())
    mypycommons.logger.setSharedLoggerConsoleOutputLogLevel('info')
    logger = mypycommons.logger.getSharedLogger()

    thisDir = mypycommons.file.getThisScriptCurrentDirectory()
    configFilePath = mypycommons.file.JoinPaths(thisDir, 'permissions.csv')

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

        if (rule['applyToType'] == 'f'):
            applyToType = 'file'
        elif (rule['applyToType'] == 'd'):
            applyToType = 'directory'
        else:
            applyToType = ''

        logger.info("Applying permission rule #{}: {} ({}:{}, {}, DoOnlyForType={}, Recursive={})".format(currentLine, rule['path'], rule['owner'], rule['group'], rule['mask'], applyToType, useRecursive))
        mypycommons.file.applyPermissionToPath(rule['path'], rule['owner'], rule['group'], rule['mask'], onlyChildPathType=applyToType, recursive=useRecursive)

        currentLine += 1

    logger.info("All permission rules finished applying, script completed successfully")
       

