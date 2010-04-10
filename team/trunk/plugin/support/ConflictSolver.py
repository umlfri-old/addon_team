'''
Created on 10.4.2010

@author: Peterko
'''

class CConflictSolver(object):
    '''
    classdocs
    '''
    
    # resolutions
    ACCEPT_MINE = 'ACCEPT MINE'
    ACCEPT_THEIRS = 'ACCEPT THEIRS'
    NO_CHANGE = 'NO CHANGE'


    def __init__(self, conflicts, merger):
        '''
        Constructor
        '''
        
        self.__unresolvedConflicts = self.__conflicts
        self.__resolvedConflicts = []
        self.__merger = merger
        
        
    def GetUnresolvedConflicts(self):
        return self.__unresolvedConflicts
    
    def GetResolvedConflicts(self):
        return self.__resolvedConflicts
    
        
    def ResolveConflict(self, conflict, resolution):
        # pokus sa vyriesit konflikt a pozor na zavisle konflikty
        if conflict not in self.__resolvedConflicts:
        
            relatedConflicts = self.__FindRelatedConflicts(conflict)
            
            
            if resolution == CConflictSolver.NO_CHANGE:
                self.__MoveResolvedConflicts(relatedConflicts)
                
            elif resolution == CConflictSolver.ACCEPT_MINE:
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs([conflict.GetBaseWorkDiff() for conflict in relatedConflicts])
                
            elif resolution == CConflictSolver.ACCEPT_THEIRS:
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs([conflict.GetBaseNewDiff() for conflict in relatedConflicts])
        
         
    def __MoveResolvedConflicts(self, conflicts):
        for conflict in conflicts:
            self.__unresolvedConflicts.remove(conflict)
            self.__resolvedConflicts.append(conflict)
    
        
    def __FindRelatedConflicts(self, conflict):
        #najdi vsetky zavisle konflikty
        result = []
        
        return result