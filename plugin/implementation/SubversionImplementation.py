'''
Created on 30.3.2010

@author: Peterko
'''

#import pysvn
import os
from subprocess import Popen, PIPE




class CSubversionImplementation(object):
    '''
    classdocs
    '''
    description = 'SVN'
    
    executable = 'svn'
    

    def __init__(self, fileName):
        '''
        Constructor
        '''
        #self.__client = pysvn.Client()
        self.__fileName = fileName
        
       
       
    def GetFileData(self, revision=None):
        if revision is None:
            rev = 'BASE'
        else:
            rev = revision
        command = [self.executable, 'cat', self.__fileName, '-r', rev]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if p.returncode == 0:
            return out
        else:
            raise Exception(p.communicate()[1])
    
    def GetFileName(self):
        return self.__fileName
        
    # zisti, ci je projekt pod tymto verzovacim systemom    
    def IsProjectVersioned(self):
        
        command = [self.executable, 'status', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        return p.communicate()[1] == ''
        
     
    


        
    def BeforeUpdate(self, revision=None):
        '''
        Returns contents of mine, base and updated files
        '''
        print 'before update'
        if revision is None:
            rev = 'HEAD'
        else:
            rev = revision
        mine = open(self.__fileName).read()
        base = self.GetFileData()
        upd = self.GetFileData(rev)
        return mine, base, upd
    
        
    def Update(self, fileData, revision=None):
        '''
        Run update and then rewrite file with contents in fileData
        Solve conflicts on implementation level
        '''
        print 'trying svn update to revision'
        if revision is None:
            rev = 'HEAD'
        else:
            rev = revision
            
        command = [self.executable, 'update', self.__fileName, '-r', rev, '--non-interactive']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (result, err) = p.communicate()
        
        command2 = [self.executable, 'status', self.__fileName]
        p2 = Popen(command2, stdout=PIPE, stderr=PIPE)
        (out, err2) = p2.communicate()
        
        if len(out) > 0:
            if out[0] == 'C':
                # ak je v konflikte
                # vyries konflikt na urovni svn, aby tam potom nestrasili tie subory
                self.__SolveConflict()
        

        f = open(self.__fileName, 'w')
        f.write(fileData)
        f.close()
        
        
        
        return result
    
    def __SolveConflict(self):
        command = [self.executable, 'resolved', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.communicate()
    
        
    def Checkin(self, message=''):
        print 'trynig svn commit'
        command = [self.executable, 'commit', self.__fileName, '-m', message]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if p.returncode == 0:
            return out
        else:
            return err
        
    def Revert(self):
        print 'trying svn revert'
        command = [self.executable, 'revert', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.communicate()
    
    
    
    
    
    @classmethod    
    def Checkout(self, url, directory, revision = None):
        print 'trying svn checkout'
        if revision is None:
            rev = 'HEAD'
        else:
            rev = revision
        command = [self.executable, 'checkout', url, directory, '-r', rev]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if p.returncode == 0:
            return out
        else:
            return err
        
        