'''
Created on 6.4.2010

@author: Peterko
'''
from Conflicter import CConflicter
from structure import *
from DiffActions import EDiffActions
from Merger import CMerger




class CUpdater(object):
    '''
    classdocs
    '''


    def __init__(self, mine, base, upd, fileName):
        '''
        Constructor
        '''
        
        self.__baseProject = CProject(None, base)
        self.__updProject  = CProject(None, upd)
        self.__mineProject = CProject(None, mine)
        self.__fileName = fileName
        self.__newXml = None
        self.__conflictFileName = None
        self.__TryUpdate()
        self.__conflicter = None
        
        
        
        
    def GetNewXml(self):
        self.__newXml = self.__baseProject.GetSaveXml()
        return self.__newXml
    
    def GetConflictFileName(self):
        return self.__conflictFileName
    
    def GetConflicter(self):
        return self.__conflicter
        
    def __TryUpdate(self):
        
        
        self.__conflicter = CConflicter(self.__updProject, self.__baseProject, self.__mineProject)
        if len(self.__conflicter.conflicting) == 0:
            print 'no conflicts'
        else:
            # vytvor 3 subory v adresari s projektom, aby som vedel, ze je v konflikte
            fmine = open(self.__fileName+'.friwork', 'w')
            fmine.write(self.__mineProject.GetSaveXml())
            fmine.close()
            fold = open(self.__fileName+'.fribase', 'w')
            fold.write(self.__baseProject.GetSaveXml())
            fold.close()
            fnew = open(self.__fileName+'.frinew', 'w')
            fnew.write(self.__updProject.GetSaveXml())
            fnew.close()
            self.__conflictFileName = self.__fileName
            
        merger = CMerger(self.__baseProject)
        merger.MergeDiffs(self.__conflicter.merging)
            
        self.__baseProject.UpdateCounters(self.__mineProject.GetCounters())
        self.__baseProject.UpdateCounters(self.__updProject.GetCounters())
        
        
    
        