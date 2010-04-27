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
    Class provides updating capabilites. Checks for conflicts
    '''


    def __init__(self, mine, base, upd):
        '''
        Constructor
        @type mine: string
        @param mine: Working copy project string xml
        @type base: string
        @param base: Base revision project string xml
        @type upd: string
        @param upd: New project string xml
        '''
        
        self.__baseProject = CProject(None, base)
        self.__updProject  = CProject(None, upd)
        self.__mineProject = CProject(None, mine)
        
        self.__newXml = None
        self.__isInConflict = False
        self.__conflicter = None
        self.__merger = None
        
        
        self.__TryUpdate()
        
        
        
        
        
    def GetNewXml(self):
        '''
        Returns xml of merged project
        @rtype: string
        @return: Xml of merged project 
        '''
        self.__newXml = self.__baseProject.GetSaveXml()
        return self.__newXml
    
    def IsInConflict(self):
        '''
        Returns boolean if update ended with conflicts
        @rtype: bool
        @return: True if update ended with conflicts, False otherwise
        '''
        return self.__isInConflict
    
    def GetConflicter(self):
        '''
        Returns conflicter instance
        @rtype: CConflicter
        @return: Conflicter instance
        '''
        return self.__conflicter
    
    def GetMerger(self):
        '''
        Returns merger instance
        @rtype: CMerger
        @return: Merger instance
        '''
        return self.__merger
        
    def __TryUpdate(self):
        '''
        Tries update (apply diffs from new and work to base)
        '''
        
        
        self.__conflicter = CConflicter(self.__updProject, self.__baseProject, self.__mineProject)
        if len(self.__conflicter.GetConflicting()) == 0:
            # ok nechaj vsetko tak
            pass
        else:
            self.__isInConflict = True
            
        self.__merger = CMerger(self.__baseProject)
        self.__merger.MergeDiffs(self.__conflicter.merging)
            
        
        self.__baseProject.UpdateCounters(self.__mineProject.GetCounters())
        
        self.__baseProject.UpdateCounters(self.__updProject.GetCounters())
        
        
        
    
        