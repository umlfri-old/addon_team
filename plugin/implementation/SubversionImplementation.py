'''
Created on 30.3.2010

@author: Peterko
'''


from subprocess import Popen, PIPE
from imports.etree import etree
from teamExceptions import *
import os



class CSubversionImplementation(object):
    '''
    classdocs
    '''
    description = 'SVN'
    
    executable = 'svn'
    
    supported = ['checkin', 'checkout', 'diff', 'log', 'update', 'revert']
    

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
        
     
   
    
        
    def Update(self, revision=None):
        '''
        Run update, return new status of updated file
        '''
        print 'trying svn update to revision'
        if revision is None:
            rev = 'HEAD'
        else:
            rev = revision
        
        # run update    
        command = [self.executable, 'update', self.__fileName, '-r', rev, '--non-interactive']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (result, err) = p.communicate()
        
        
        return result
    
    
    def IsCompatible(self):
        command = [self.executable, 'propget', 'svn:mime-type', self.__fileName, '--xml']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        r = etree.XML(out)
        result = False
        for t in r:
            if t.tag == 'target':
                if os.path.normpath(t.get('path')) == os.path.normpath(self.__fileName):
                    for p in t:
                        if p.tag == 'property':
                            if p.get('name') == 'svn:mime-type':
                                if p.text == 'application/octet-stream':
                                    result = True
        return result
    
    def MakeCompatible(self):
        command = [self.executable, 'propset', 'svn:mime-type', 'application/octet-stream', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
    
    def IsInConflict(self):
        command2 = [self.executable, 'status', self.__fileName, '--xml']
        p2 = Popen(command2, stdout=PIPE, stderr=PIPE)
        (out, err2) = p2.communicate()
        
        
        r = etree.XML(out)
        wcStatus = r.find('.//wc-status')
        
        if wcStatus is not None:
            
            if wcStatus.get('item') == 'conflicted':
                return True
            
        return False
    
    def GetConflictingFiles(self):
        if self.IsInConflict():
            command3 = [self.executable, 'info', self.__fileName, '--xml']
            p3 = Popen(command3, stdout=PIPE, stderr=PIPE)
            (out, err2) = p3.communicate()
            r = etree.XML(out)
            baseFileName = r.find('.//prev-base-file').text
            newFileName = r.find('.//cur-base-file').text
             
            baseFile = os.path.join(os.path.dirname(self.__fileName), baseFileName)
            newFile = os.path.join(os.path.dirname(self.__fileName), newFileName)
            return {'mine':self.__fileName, 'base':baseFile, 'new':newFile}
        else:
            return None
            
    
    def Resolve(self):
        command = [self.executable, 'resolved', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (result, err) = p.communicate()
    
    
    
    def __SolveConflict(self):
        command = [self.executable, 'resolved', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.communicate()
    
        
    def Checkin(self, message='', username = None, password=None):
        print 'trynig svn commit'
        if username is None or password is None:
            command = [self.executable, 'commit', self.__fileName, '-m', message, '--non-interactive']
        else :
            command = [self.executable, 'commit', self.__fileName, '-m', message, '--non-interactive', '--username',username, '--password', password]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        
        if p.returncode == 0:
            # ak je vsetko v poriadku, vrat hlasku
            return out
        else:
            if err.lower().find('authorization') != -1:
                # ak je problem s autentifikaciou vyhod vynimnku
                raise AuthorizationError
            else:
                # inak vrat chybovu hlasku
                print 'returning err'
                return err
        
    def Revert(self):
        print 'trying svn revert'
        command = [self.executable, 'revert', self.__fileName]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.communicate()
    
    
    def Log(self):
        print 'trying svn log'
        command = [self.executable, 'log', self.__fileName, '--xml']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        # out ma teraz xml
        root = etree.XML(out)
        result = []
        for e in root:
            d = {}
            d['revision'] = e.get('revision')
            for sub in e:
                if sub.tag == 'author':
                    d['author'] = sub.text
                elif sub.tag == 'date':
                    d['date'] = sub.text
                elif sub.tag == 'msg':
                    d['message'] = sub.text
            result.append(d)
        
        return result
                    
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
        
        