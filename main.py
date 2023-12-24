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

from src.permit_enforcer import PermitEnforcerApp



def getProjectLogsDir():
    currentDir = mypycommons.file.getThisScriptCurrentDirectory()
    logsDir = mypycommons.file.joinPaths(currentDir, '~logs')

    if (not mypycommons.file.pathExists(logsDir)):
        mypycommons.file.createDirectory(logsDir)
    
    return logsDir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", 
        help="permissions config file name in config/",
        default="permissions.json",
        type=str,
        dest='configFilename'
    )
    args = parser.parse_args()

    # Set up logger
    loggerWrapper = mypycommons.logger.CommonLogger(
        loggerName="permit-enforcer-logger", 
        logDir=getProjectLogsDir(), 
        logFilename="apply-permissions.py.log"
    )
    app = PermitEnforcerApp(args.configFilename, loggerWrapper)

    app.run()
    



       

