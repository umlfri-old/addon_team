'''
Created on 10.4.2010

@author: Peterko
'''
from DiffActions import EDiffActions

class CConflictSolver(object):
    '''
    Class that manages conflicts resolving
    '''
    
    # resolutions
    ACCEPT_MINE = 'ACCEPT MINE'
    ACCEPT_THEIRS = 'ACCEPT THEIRS'
    NO_CHANGE = 'NO CHANGE'


    def __init__(self, conflicts, merger):
        '''
        Constructor
        @type conflicts: list
        @param conflicts: Conflicts to be possibly solved
        @type merger: CMerger
        @param merger: Merger instance, provides merging of diffs
        '''
        
        self.__unresolvedConflicts = conflicts
        self.__resolvedConflicts = []
        self.__merger = merger
        
    def GetMerger(self):
        '''
        Getter for merger
        @rtype: CMerger
        @return: merger
        '''
        return self.__merger
        
    def GetUnresolvedConflicts(self):
        '''
        Getter for unresolved conflicts
        @rtype: list
        @return: unresolved conflicts
        '''
        return self.__unresolvedConflicts
    
    def GetResolvedConflicts(self):
        '''
        Getter for resolved conflicts
        @rtype: list
        @return: resolved conflicts
        '''
        return self.__resolvedConflicts
    
        
    def ResolveConflict(self, conflict, resolution):
        '''
        Resolves conflict (and all related conflicts) with desired resolution
        @type conflict: CConflict
        @param conflict: Conflict to be solved
        @type resolution: CConflictSolver.resolutions
        @param resolution: Desired resolution
        '''
        # pokus sa vyriesit konflikt a pozor na zavisle konflikty
        if conflict not in self.__resolvedConflicts:
        
            relatedConflicts = self.FindRelatedConflicts(conflict)
            
            for r in relatedConflicts:
                print r
            
            if resolution == CConflictSolver.NO_CHANGE:
                self.__MoveResolvedConflicts(relatedConflicts)
                
            elif resolution == CConflictSolver.ACCEPT_MINE:
                
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs(list(set([conflict.GetBaseWorkDiff() for conflict in relatedConflicts])))
                
            elif resolution == CConflictSolver.ACCEPT_THEIRS:
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs(list(set([conflict.GetBaseNewDiff() for conflict in relatedConflicts])))
        
         
    def __MoveResolvedConflicts(self, conflicts):
        '''
        Moves conflicts from unresolved to resolved
        @type conflicts: list
        @param conflicts: resolved conflicts 
        '''
        for conflict in conflicts:
            self.__unresolvedConflicts.remove(conflict)
            self.__resolvedConflicts.append(conflict)
    
        
    def FindRelatedConflicts(self, conflict):
        '''
        Finds related conflict for given conflict
        @type conflict: CConflict
        @param conflict: Base conflict
        '''
        #najdi vsetky zavisle konflikty
        result = [conflict]
        
        baseWorkDiff = conflict.GetBaseWorkDiff()
        baseNewDiff = conflict.GetBaseNewDiff()
        if baseWorkDiff.GetAction() == EDiffActions.DELETE or baseNewDiff.GetAction() == EDiffActions.DELETE:
            for c in self.__unresolvedConflicts:
                if c not in result:
                    if c.GetBaseWorkDiff() == baseWorkDiff:
                        result.append(c)
                        
                        
                    elif c.GetBaseNewDiff() == baseNewDiff:
                        result.append(c)
                        
                        
            for c in self.__unresolvedConflicts:
                if c not in result:
                    if c.GetBaseWorkDiff() in [r.GetBaseWorkDiff() for r in result]:
                        result.append(c)
                    elif c.GetBaseNewDiff() in [r.GetBaseNewDiff() for r in result]:
                        result.append(c)
                        
            for c in self.__unresolvedConflicts:
                if c not in result:
                    if len(set.intersection(set(c.GetRelatedObjects()), set([r.GetBaseWorkDiff().GetElement() for r in result]))) > 0:
                        result.append(c)
                        
                    elif len(set.intersection(set(c.GetRelatedObjects()), set([r.GetBaseNewDiff().GetElement() for r in result]))) > 0:
                        result.append(c)
        else:
            for c in self.__unresolvedConflicts:
                if c not in result:
                    if c.GetBaseWorkDiff() == baseWorkDiff:
                        result.append(c)
                        
                    elif c.GetBaseNewDiff() == baseNewDiff:
                        result.append(c)
        return list(set(result))