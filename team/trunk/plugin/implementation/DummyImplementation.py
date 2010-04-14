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


    supported = ['diff']
    
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
    
    def BeforeUpdate(self, revision=None):
        
        raise Exception('Not implemented in dummy implementation')
    
    
    def Update(self, fileData, revision=None):
        
        raise Exception('Not implemented in dummy implementation')
    
    def Checkin(self, message='', username = None, password=None):
        
        raise Exception('Not implemented in dummy implementation')
    
    @classmethod
    def Checkout(self, url, directory, revision = None):
        
        raise Exception('Not implemented in dummy implementation')
    
    def Revert(self):
        
        raise Exception('Not implemented in dummy implementation')
    
    def Log(self):
        
        raise Exception('Not implemented in dummy implementation')
    
    
    