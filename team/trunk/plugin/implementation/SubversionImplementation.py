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
    description = 'SVN'
    

    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.__client = pysvn.Client()
        self.__fileName = fileName
       
       
    def GetFileData(self, revision=None):
        if revision is None:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.base )
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
        
     
    


        
    def BeforeUpdate(self, revision=None):
        print 'before update'
        if revision is None:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.head )
        else:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.number, revision )
        mine = self.__client.cat(self.__fileName, pysvn.Revision(pysvn.opt_revision_kind.working))
        base = self.__client.cat(self.__fileName, pysvn.Revision(pysvn.opt_revision_kind.base))
        upd = self.__client.cat(self.__fileName, revnum)
        return mine, base, upd
    
        
    def Update(self, fileData, revision=None):
        print 'trying svn update'
        if revision is None:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.head )
        else:
            revnum = pysvn.Revision( pysvn.opt_revision_kind.number, revision )
        result = self.__client.update(self.__fileName, revnum)[0]
        
        status = self.__client.status(self.__fileName)[0]
        
        if status['text_status']==pysvn.wc_status_kind.conflicted:
        
        
            self.__SolveConflict()
        
        f = open(self.__fileName, 'w')
        f.write(fileData)
        f.close()
        
        
        
        return status.entry.revision.number
    
    def __SolveConflict(self):
        self.__client.resolved(self.__fileName)
    
        
    def Checkin(self, message=''):
        print 'trynig svn commit'
        try:
            self.__client.checkin(self.__fileName, message)
        except Exception, e:
            return 'error', e
        status = self.__client.status(self.__fileName)[0]
        return 'ok', status.entry.revision.number
        
    def Revert(self):
        print 'trying svn revert'
        print self.__client.revert(self.__fileName)
    
    
    
    
    
    @classmethod    
    def Checkout(self, url, directory, revision = None):
        print 'trying svn checkout'
        client = pysvn.Client()
        if revision is None:
            client.checkout(url,directory)
        else:
            client.checkout(url,directory, revision=pysvn.Revision(pysvn.opt_revision_kind.number, revision))
        