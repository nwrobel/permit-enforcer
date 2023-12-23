import os
import sys
import unittest

# Add project root to PYTHONPATH so MLU modules can be imported
scriptPath = os.path.dirname(os.path.realpath(__file__))
projectRoot = os.path.abspath(os.path.join(scriptPath ,".."))
sys.path.insert(0, projectRoot)

from com.nwrobel import mypycommons
from com.nwrobel.mypycommons import (
    file,
    time,
    logger,
    system,
    archive
)

from src.permit_enforcer import PermitEnforcerApp, PermitEnforcerPath


def getProjectLogsDir():
    currentDir = mypycommons.file.getThisScriptCurrentDirectory()
    logsDir = mypycommons.file.joinPaths(currentDir, '../~logs')

    if (not mypycommons.file.pathExists(logsDir)):
        mypycommons.file.createDirectory(logsDir)
    
    return logsDir

class PermitEnforcer_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        '''
        super(PermitEnforcer_ModuleTest, self).setUpClass

        thisDirectory = mypycommons.file.getThisScriptCurrentDirectory()
        self.testDataDir = mypycommons.file.joinPaths(thisDirectory, 'data')



    # @classmethod
    # def tearDownClass(self):  
    #     super(Archive_ModuleTest, self).tearDownClass      
    #     mypycommons.file.deletePath(self.tempDir)

    def test(self):
        '''
        '''
        loggerWrapper = mypycommons.logger.CommonLogger(
            loggerName="permit-enforcer-logger-test", 
            logDir=getProjectLogsDir(), 
            logFilename="apply-permissions-test.py.log"
        )
        app = PermitEnforcerApp('permissions.unittest.json', loggerWrapper)
        app.run()
        
        configItemPaths = [ci.path for ci in app._configItems]
        expectedPathItemResults = [
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test',
                'owner': 'root',
                'group': 'root',
                'mask': '777'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\1',
                'owner': 'root',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir2',
                'owner': 'root',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir2\\1',
                'owner': 'root',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir2\\subdir',
                'owner': 'root',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir2\\subdir\\1',
                'owner': 'root',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1',
                'owner': 'git',
                'group': 'git',
                'mask': '777'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\1',
                'owner': 'git',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects',
                'owner': 'object',
                'group': 'object',
                'mask': '777'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\1',
                'owner': 'object',
                'group': 'allppl',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\0c',
                'owner': 'see',
                'group': 'object',
                'mask': '770'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\0c\\1',
                'owner': 'see',
                'group': 'object',
                'mask': '750'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\0c\\2',
                'owner': 'datad',
                'group': 'datad',
                'mask': '600'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\0c\\test',
                'owner': 'test',
                'group': 'test',
                'mask': '400'
            },
            {
                'path': 'C:\\nick-local-data\\local-dev-my\\test\\dir1\\objects\\0c\\test\\1',
                'owner': 'test',
                'group': 'test',
                'mask': '400'
            }
            # {
            #     'path': '',
            #     'owner': '',
            #     'group': '',
            #     'mask': ''
            # },
        ]
        for resultPep in app._permitEnforcerPaths:
            actualPathItemResult = {
                'path': resultPep.path,
                'owner': resultPep.owner,
                'group': resultPep.group,
                'mask': resultPep.mask
            }

            self.assertIn(actualPathItemResult, expectedPathItemResults)



if __name__ == '__main__':
    unittest.main()
