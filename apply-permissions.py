'''
Main script for permissions application project.
'''
import subprocess
import os
import csv
import logging
logger = logging.getLogger()

def applyPermissionToPath(path, owner, group, mask):

    # Set ownership and permissions using by calling the linux chown and chmod commands
    # If the path is a dir, specify the recursive option
    ownerGroup = "{}:{}".format(owner, group)
    if (os.path.isdir(path)):    
        subprocess.call(['sudo', 'chown', ownerGroup, '-R', path])
        subprocess.call(['sudo', 'chmod', mask, '-R', path])
    else:
        subprocess.call(['sudo', 'chown', ownerGroup, path])
        subprocess.call(['sudo', 'chmod', mask, path])


if __name__ == '__main__':

    permitConfigFilePath = '/datastore/nick/permissions.csv'
    logger.info("Starting file permission application script")

    with open(permitConfigFilePath, mode='r') as permitConfigFile:
        logger.info("Reading file permission config file {}".format(permitConfigFile))
        permitCsv = csv.DictReader(permitConfigFile)
        currentLine = 0

        for permitRule in permitCsv:
            if (currentLine != 0):
                logger.info("Processing permission rule #{}: {} ({}:{} {})".format(currentLine, permitRule['path'], permitRule['owner'], permitRule['group'], permitRule['mask']))
                applyPermissionToPath(permitRule['path'], permitRule['owner'], permitRule['group'], permitRule['mask'])

            currentLine += 1

        logger.info("All permission rules finished applying, script complete")
       

