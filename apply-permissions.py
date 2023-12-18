'''
Main script for permissions application project.
'''

import os
import csv
import logging
import argparse

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.file
import com.nwrobel.mypycommons.logger

def getProjectLogsDir():
    currentDir = mypycommons.file.getThisScriptCurrentDirectory()
    logsDir = mypycommons.file.joinPaths(currentDir, '~logs')

    if (not mypycommons.file.pathExists(logsDir)):
        mypycommons.file.createDirectory(logsDir)
    
    return logsDir

def getConfigFilepath(configFilename):
    currentDir = mypycommons.file.getThisScriptCurrentDirectory()
    configDir = mypycommons.file.joinPaths(currentDir, 'config')

    return mypycommons.file.joinPaths(configDir, configFilename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", 
        help="permissions config file name in config/",
        default="permissions.csv",
        type=str,
        dest='configFile'
    )
    args = parser.parse_args()

    # Set up logger
    loggerWrapper = mypycommons.logger.CommonLogger(
        loggerName="apply-permissions-logger", 
        logDir=getProjectLogsDir(), 
        logFilename="apply-permissions.py.log"
    )
    logger = loggerWrapper.getLogger()

    configFilePath = getConfigFilepath(args.configFile)
    logger.info("Starting permit-enforcer: Reading permission config file: {}".format(configFilePath))

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
       

