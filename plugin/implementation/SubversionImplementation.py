'''
Created on 30.3.2010

@author: Peterko
'''

import pysvn
import os

class CSubversionImplementation(object):
    '''
    classdocs
    '''


    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.__client = pysvn.Client()
        self.__fileName = fileName
       
       
    def GetFileData(self, revision=None):
        if revision is None:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.head )
        else:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.number, revision )
        return self.__client.cat(self.__fileName, revnum)
    
    def GetFileName(self):
        return self.__fileName
        
    # zisti, ci je projekt pod tymto verzovacim systemom    
    def IsProjectVersioned(self):
        try:
            return self.__client.status(self.__fileName)[0]['is_versioned'] == 1
        except:
            return False
        
     
    def GetConflictTriple(self):
        status = self.__client.status(self.__fileName)[0]
        
        if status['text_status']==pysvn.wc_status_kind.conflicted:
            # conflict
            conflictNewFileName = self.__fileName[0:self.__fileName.rfind(os.sep)+1]+status['entry']['conflict_new']
            conflictOldFileName = self.__fileName[0:self.__fileName.rfind(os.sep)+1]+status['entry']['conflict_old']
            conflictWorkFileName = self.__fileName[0:self.__fileName.rfind(os.sep)+1]+status['entry']['conflict_work']
            result = (open(conflictNewFileName).read(), open(conflictOldFileName).read(), open(conflictWorkFileName).read())
            return result
        else:
            return None
        
        
    def Update(self, revision=None):
        print 'trying svn update'
        if revision is None:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.head )
        else:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.number, revision )
        result = self.__client.update(self.__fileName, revnum)[0]
        
        if self.GetConflictTriple() is not None:
            return self.GetConflictTriple()
        else:
            # malo by byt ok
            return result.number
        
    def Checkin(self, message=''):
        print 'trynig svn commit'
        print self.__client.checkin(self.__fileName, message)
        
    def Revert(self):
        print 'trying svn revert'
        print self.__client.revert(self.__fileName)
        
    def Checkout(self, url, directory, revision = None):
        print 'trying svn checkout'
        if revision is None:
            print self.__client.checkout(url,directory)
        else:
            print self.__client.checkout(url,directory, revision=pysvn.Revision(pysvn.opt_revision_kind.number, revision))
        