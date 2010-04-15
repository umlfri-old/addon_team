'''
Created on 10.4.2010

@author: Peterko
'''
from DiffActions import EDiffActions

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
        
        self.__unresolvedConflicts = conflicts
        self.__resolvedConflicts = []
        self.__merger = merger
        
    def GetMerger(self):
        return self.__merger
        
    def GetUnresolvedConflicts(self):
        return self.__unresolvedConflicts
    
    def GetResolvedConflicts(self):
        return self.__resolvedConflicts
    
        
    def ResolveConflict(self, conflict, resolution):
        # pokus sa vyriesit konflikt a pozor na zavisle konflikty
        if conflict not in self.__resolvedConflicts:
        
            relatedConflicts = self.__FindRelatedConflicts(conflict)
            print 'found related conflicts'
            for r in relatedConflicts:
                print r
            
            if resolution == CConflictSolver.NO_CHANGE:
                self.__MoveResolvedConflicts(relatedConflicts)
                
            elif resolution == CConflictSolver.ACCEPT_MINE:
                print 'accepting mine'
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs(list(set([conflict.GetBaseWorkDiff() for conflict in relatedConflicts])))
                
            elif resolution == CConflictSolver.ACCEPT_THEIRS:
                self.__MoveResolvedConflicts(relatedConflicts)
                self.__merger.MergeDiffs(list(set([conflict.GetBaseNewDiff() for conflict in relatedConflicts])))
        
         
    def __MoveResolvedConflicts(self, conflicts):
        for conflict in conflicts:
            self.__unresolvedConflicts.remove(conflict)
            self.__resolvedConflicts.append(conflict)
    
        
    def __FindRelatedConflicts(self, conflict):
        #najdi vsetky zavisle konflikty
        result = [conflict]
        print 'finding related for', conflict
        baseWorkDiff = conflict.GetBaseWorkDiff()
        baseNewDiff = conflict.GetBaseNewDiff()
        print 'base work diff', baseWorkDiff
        print 'base new diff', baseNewDiff
        if baseWorkDiff.GetAction() == EDiffActions.DELETE or baseNewDiff.GetAction() == EDiffActions.DELETE:
            for c in self.__unresolvedConflicts:
                if c not in result:
                    if c.GetBaseWorkDiff() == baseWorkDiff:
                        result.append(c)
                        print 'found', c
                        
                    elif c.GetBaseNewDiff() == baseNewDiff:
                        result.append(c)
                        print 'found', c
                        
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