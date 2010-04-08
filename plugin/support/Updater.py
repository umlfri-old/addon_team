'''
Created on 6.4.2010

@author: Peterko
'''
from Conflicter import CConflicter
from structure import *
from DiffActions import EDiffActions




class CUpdater(object):
    '''
    classdocs
    '''


    def __init__(self, mine, base, upd, fileName):
        '''
        Constructor
        '''
        self.__mineProject = CProject(None, mine)
        self.__baseProject = CProject(None, base)
        self.__updProject  = CProject(None, upd)
        self.__fileName = fileName
        self.__newXml = None
        self.__conflictFileName = None
        self.__TryUpdate()
        
        
        
        
    def GetNewXml(self):
        return self.__newXml
    
    def GetConflictFileName(self):
        return self.__conflictFileName
        
    def __TryUpdate(self):
        
        
        conflicter = CConflicter(self.__updProject, self.__baseProject, self.__mineProject)
        if len(conflicter.conflicting) == 0:
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
        for diff in conflicter.merging:
            self.__MergeDiff(diff)
            
        self.__mineProject.UpdateCounters(self.__updProject.GetCounters())
        self.__newXml = self.__mineProject.GetSaveXml()
        
        
    def __MergeDiff(self, diff):
        
        print 'merging',diff
        element = diff.GetElement()
        
        if diff.GetAction() == EDiffActions.INSERT:
            
            if isinstance(element, CBase):
                print 'adding object'
                self.__mineProject.AddObject(element)
            
            elif isinstance(element, CProjectTreeNode):
                print 'adding project tree node'
                self.__mineProject.AddProjectTreeNode(element)
            elif isinstance(element, CBaseView):
                print 'adding view'
                self.__mineProject.AddView(element)
            
        
        elif diff.GetAction() == EDiffActions.DELETE:
            if isinstance(element, CBase):
                print 'deleting object'
                self.__mineProject.DeleteObject(element)
            
            
            elif isinstance(element, CProjectTreeNode):
                print 'deleting project tree node'
                self.__mineProject.DeleteProjectTreeNode(element)
                
            elif isinstance(element, CBaseView):
                print 'deleting view'
                self.__mineProject.DeleteView(element) 
            
            
        
        elif diff.GetAction() == EDiffActions.MODIFY:
            if isinstance(element, CBase):
                print 'modifying object data'
                self.__mineProject.ModifyObjectData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
            elif isinstance(element, CBaseView):
                print 'modyfing view data'
                self.__mineProject.ModifyViewData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
                
        elif diff.GetAction() == EDiffActions.MOVE:
            print 'moving project tree node'
            self.__mineProject.MoveProjectTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
        
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            if isinstance(element, CProjectTreeNode):
                print 'changing order project tree node'
                self.__mineProject.ChangeOrderTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
            elif isinstance(element, CBaseView):
                print 'changing order view'
                self.__mineProject.ChangeOrderView(element, diff.GetPreviousState(), diff.GetNewState())
        
        