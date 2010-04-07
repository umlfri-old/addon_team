'''
Created on 28.3.2010

@author: Peterko
'''
from zipfile import ZipFile, is_zipfile
from lib.Addons.Plugin.Client.Interface import CInterface

class CDummyImplementation(object):
    '''
    classdocs
    '''
    
    description = 'Dummy'

    def __init__(self, fileName):
        '''
        Constructor
        '''
        
        self.__fileName = fileName
        
        
    def IsProjectVersioned(self):
        return False
    
    def GetFileData(self, revision = None):
        prFile = self.__fileName
        if (is_zipfile(prFile)):
            file = ZipFile(prFile,'r')
            fileData = file.read('content.xml')
        else :
            file = open(prFile, 'r')
            fileData = file.read()
        return fileData
    
    def GetFileName(self):
        return self.__fileName
    
    
    def Update(self, revision = None):
        print 'Dummy implementation update'
        pass
    
    def Checkin(self, message = ''):
        print 'Dummy implementation commit'
        pass
    
    @classmethod
    def Checkout(self, url, directory, revision = None):
        print 'Dummy implementation checkout'
        pass
    
    def Revert(self):
        print 'Dummy implementation revert'
        pass
    
    def Log(self, revisionStart = None, revisionEnd = None):
        print 'Dummy implementation log'
        pass
    
    def Status(self):
        print 'Dummy implementation status'
        pass
    