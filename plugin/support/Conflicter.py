'''
Created on 2.4.2010

@author: Peterko
'''
from Differ import CDiffer
from DiffActions import EDiffActions
import itertools
from structure import CProjectTreeNode

class CConflicter(object):
    '''
    classdocs
    '''


    def __init__(self, newProject, oldProject, workProject):
        '''
        Constructor
        '''
        self.__new = newProject
        self.__old = oldProject
        self.__work= workProject
        
        self.__oldNewDiffer = CDiffer(self.__old, self.__new)
        self.__oldWorkDiffer = CDiffer(self.__old, self.__work)
        
        self.__TryConflictSolve()
        
    def __TryConflictSolve(self):
        # pokus sa zakomponovat zmeny z new do worku
        # ak to nepojde vyhlas to za konflikt a ponukni pouzivatelovi riesenie
        
        # najskor projektovy strom
        
        
        for diff in self.__oldNewDiffer.projectTreeDiff:
            if self.__PossibleToMergeProjectTreeDiff(diff):
                self.__MergeProjectTreeDiff(diff)
            else:
                self.__ProjectTreeConflict(diff)
        
        # potom vizualny diff
        
        for diff in self.__oldNewDiffer.visualDiff:
            if self.__PossibleToMergeVisualDiff(diff):
                self.__MergeVisualDiff(diff)
            else:
                self.__VisualConflict(diff)
            
        
        # nakoniec diff datovych zloziek
        for diff in self.__oldNewDiffer.dataDiff:
            if self.__PossibleToMergeDataDiff(diff):
                self.__MergeDataDiff(diff)
            else:
                self.__DataConflict(diff)
        
    
    
    
    
    def __PossibleToMergeProjectTreeDiff(self, diff):
        if diff.GetAction() == EDiffActions.INSERT:
            if diff.GetElement().GetParent() in [d.GetElement() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, [])]:
                print 'insert project tree node under deleted element'
                print diff
                return False
            else:
                return True
            
        elif diff.GetAction() == EDiffActions.DELETE:
            if diff.GetElement().GetObject() in [d.GetElement() for d in self.__oldWorkDiffer.dataDiff]:
                print 'delete modified element'
                print diff
                return False
            elif diff.GetElement() in [d.GetElement().GetParent() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.INSERT, [])]:
                print 'delete new parent project tree'
                print diff
                return False
            else:
                return True
            
        elif diff.GetAction() == EDiffActions.MOVE:
            if diff.GetElement().GetParent() in [d.GetElement() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, [])]:
                print 'move project tree node under deleted element'
                print diff
                return False
            elif diff.GetElement() in [d.GetElement() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.MOVE, [])]:
                parentNew = diff.GetElement().GetParent()
                parentOld = self.__oldWorkDiffer.GetProjectTreeDiff()[EDiffActions.MOVE][self.__oldWorkDiffer.GetProjectTreeDiff()[EDiffActions.MOVE].index(diff)].GetElement().GetParent()
                if parentNew != parentOld:
                    print 'moving project tree node under different parents'
                    print diff
                    return False
                else:
                    return True
                    
            else:
                return True
        
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            if diff.GetElement().GetParent() in [d.GetElement() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, [])]:
                print 'changing child order under deleted element'
                print diff
                return False
            else:
                return True
       
       
       
    def __MergeProjectTreeDiff(self, diff):
        print 'merging possible project tree diff'
        print diff
    
    def __ProjectTreeConflict(self, diff):
        print 'project tree conflict'
        print diff
    
    def __PossibleToMergeVisualDiff(self, diff):
        if diff.GetAction() == EDiffActions.INSERT:
            if diff.GetElement().GetParentDiagram() in [d.GetElement().GetObject() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE,[])]:
                print 'insert view in deleted diagram'
                print diff
                return False
            else:
                return True
            
        elif diff.GetAction() == EDiffActions.DELETE:
            if diff.GetElement() in [d.GetElement() for d in self.__oldWorkDiffer.GetVisualDiff().get(EDiffActions.MODIFY,[])]:
                print 'delete modified visual element'
                print diff
                return False
            else:
                return True
            
        elif diff.GetAction() == EDiffActions.MODIFY:
            if diff.GetElement() in [d.GetElement() for d in self.__oldWorkDiffer.GetVisualDiff().get(EDiffActions.DELETE,[])]:
                print 'modify deleted visual element'
                print diff
                return False
            elif diff.GetDataPath() in [d.GetDataPath() for d in self.__oldWorkDiffer.GetVisualDiff().get(EDiffActions.MODIFY,[])]:
                print 'modyfing same visual data of elements'
                print diff
            else:
                return True
    
    
    
    def __MergeVisualDiff(self, diff):
        print 'merging possible visual diff'
        print diff
    
    def __VisualConflict(self, diff):
        print 'visual conflict'
        print diff
        
        
        
    def __PossibleToMergeDataDiff(self, diff):
        if diff.GetAction() == EDiffActions.MODIFY:
            if diff.GetElement() in [d.GetElement().GetObject() for d in self.__oldWorkDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE,[])]:
                print 'modifying data of deleted element'
                print diff
                return False
            elif diff.GetDataPath() in [d.GetDataPath() for d in self.__oldWorkDiffer.GetDataDiff().get(EDiffActions.MODIFY,[])]:
                print 'modyfing same data of elements'
                print diff
                return False
            else:
                return True
    
    
    def __MergeDataDiff(self, diff):
        print 'merging possible data diff'
        print diff
    
    def __DataConflict(self, diff):
        print 'data conflict'
        print diff
        
        
        
    def __str__(self):
        return 'new: '+str(self.__new.GetProjectTreeRoot()) \
            + 'old: '+str(self.__old.GetProjectTreeRoot()) \
            + 'work: '+str(self.__work.GetProjectTreeRoot())