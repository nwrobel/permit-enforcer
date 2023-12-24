import logging
import subprocess
import argparse
import sys
import pathlib
import os
from typing import Literal, List
from pathlib import Path
from glob import glob
from time import sleep
from tqdm import tqdm

from com.nwrobel import mypycommons
from com.nwrobel.mypycommons import (
    file,
    logger
)

def getPathParts(path):
    path = os.path.normpath(path)
    pathp = path.split(os.sep)
    return pathp

def getChildPathsDepth1(rootPath):
    return glob("{}/*".format(path), recursive=False)

def getListDupes(inputList):
    return set([x for x in inputList if inputList.count(x) > 1])

class PermitEnforcerConfigItem:
    def __init__(self, path, owner, group, mask, recursive):
        self.path = path
        self.owner = owner
        self.group = group
        self.mask = mask
        self.recursive = recursive

        pathParts = getPathParts(path)
        self.depth = len(pathParts) - 1 # adjust so root / has depth 0

class PermitEnforcerPath:
    def __init__(self, path, configItem):
        self.path = path
        self.owner = configItem.owner
        self.group = configItem.group
        self.mask = configItem.mask

class PermitEnforcerApp:
    def __init__(self, configFilename: str, loggerWrapper: mypycommons.logger.CommonLogger):
        if (not configFilename):
            raise TypeError("configFilename not passed")
        if (loggerWrapper is None):
            raise TypeError("commonLogger not passed")

        self._configFilepath = self._getConfigFilepath(configFilename)
        self._configItems = self._getConfigItems()
        self._permitEnforcerPaths = {} # dict: {'<path>': permitEnforcerPath}
        self._logger = loggerWrapper.getLogger()
        
        self._setPermitEnforcerPaths()

    def run(self):
        # Permit enforcer: make list of all file path items with the owner,group,mask,  so we can pass them directly to chown without recursive. 
        # (Apply the recursive rule logic in python - use non recursive rule over recursive if both exist for the same path) 
        # Then apply path rules deepest first.
        #
        self.applyPermitEnforcerPaths()

    def applyPermitEnforcerPaths(self):
        for pathKey in tqdm(self._permitEnforcerPaths):
            pep = self._permitEnforcerPaths[pathKey]

            #self._logger.debug("Applying permission to path: {} ({}:{}, {})".format(pep.path, pep.owner, pep.group, pep.mask))
            (chownResultTxt, chmodResultTxt) = mypycommons.file.applyPermissionToPath(pep.path, pep.owner, pep.group, pep.mask)
           
            if (chownResultTxt):
                self._logger.error("chown stderr: {}".format(chownResultTxt))
            if (chmodResultTxt):
                self._logger.error("chmod stderr: {}".format(chmodResultTxt))
            
    def _setPermitEnforcerPaths(self):
        groupedConfigItems = self._groupConfigItemsByDepth()

        for group in groupedConfigItems:
            depth = group[0]
            configItemsAtDepth = group[1]

            # handle duplicate path (apply recursive first, then non-recursive)
            dupePaths = self._getDupeConfigItemPaths(configItemsAtDepth)
            for path in dupePaths:
                configItemPair = [ci for ci in configItemsAtDepth if (ci.path == path)]
                configItemRecursive = [cip for cip in configItemPair if (cip.recursive)][0]
                configItemNonRecursive = [cip for cip in configItemPair if (not cip.recursive)][0]

                self._applyConfigItem(configItemRecursive)
                self._applyConfigItem(configItemNonRecursive)

                configItemsAtDepth.remove(configItemRecursive)
                configItemsAtDepth.remove(configItemNonRecursive)

            # handle rest
            for configItem in configItemsAtDepth:
                self._applyConfigItem(configItem)

    def _applyConfigItem(self, configItem):
        if (configItem.recursive):
            # get all files in the dir 
            # add the permitEnforcerPaths
            childPaths = mypycommons.file.getChildPathsRecursive(configItem.path)
            self._logger.info("recursive: found {} child paths".format(len(childPaths)))

            allPaths = childPaths + [configItem.path] # include the root dir itself
            for path in allPaths:
                self._updatePermitEnforcerPath(path, configItem)
        else:
            self._updatePermitEnforcerPath(configItem.path, configItem)        

    def _getDupeConfigItemPaths(self, configItemsAtDepth):
        configItemsPaths = [ci.path for ci in configItemsAtDepth]
        dupePaths = getListDupes(configItemsPaths)
        return dupePaths

    def _updatePermitEnforcerPath(self, path, configItem):
        try:
            matchingPep = self._permitEnforcerPaths[path]

            # update if there is this pep already
            matchingPep.owner = configItem.owner
            matchingPep.group = configItem.group
            matchingPep.mask = configItem.mask   
        except KeyError:
            # add
            self._permitEnforcerPaths[path] = PermitEnforcerPath(path, configItem)

    def _groupConfigItemsByDepth(self):
        self._configItems.sort(key=lambda x: x.depth)

        itemsGrouped = []
        depths = sorted(set(map(lambda x: x.depth, self._configItems)))

        for depth in depths:
            itemsAtDepth = [ci for ci in self._configItems if (ci.depth == depth)]
            itemsGrouped.append([depth, itemsAtDepth])

        return itemsGrouped

    def _getConfigItems(self):
        # Todo: validate config file input makes sense
            # path1Fmt = str(Path(path1))
            # path2Fmt = str(Path(path2))

        configData = mypycommons.file.readJsonFile(self._configFilepath)
        configItems = []
        for configItemJson in configData:
            configItems.append(
                PermitEnforcerConfigItem(
                    configItemJson['path'],
                    configItemJson['owner'],
                    configItemJson['group'],
                    configItemJson['mask'],
                    configItemJson['recursive']
                )
            )
        return configItems

    def _getConfigFilepath(self, configFilename):
        currentDir = mypycommons.file.getThisScriptCurrentDirectory()
        configDir = mypycommons.file.joinPaths(currentDir, '../config')

        return mypycommons.file.joinPaths(configDir, configFilename)
