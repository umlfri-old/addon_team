'''
Created on 2.4.2010

@author: Peterko
'''
from Differ import CDiffer
from DiffActions import EDiffActions
import itertools
from structure import *
from Conflict import CConflict
from DiffResult import CDiffResult

class CConflicter(object):
    '''
    Class that checks for conflicts between base, new and work project
    '''


    def __init__(self, newProject, baseProject, workProject):
        '''
        Constructor
        @type newProject: CProject
        @param newProject: new project
        @type baseProject: CProject
        @param baseProject: base project
        @type workProject: CProject
        @param workProject: work project
        '''
        self.__new = newProject
        self.__base = baseProject
        self.__work= workProject
        
        
        self.__baseWorkDiffer = CDiffer(self.__base, self.__work)
        
        self.__baseNewDiffer = CDiffer(self.__base, self.__new)
        
        
        self.merging = []
        
        self.conflicting = []
        
        self.__TryMerge()
        
    def GetConflicting(self):
        '''
        Getter for all conflicts
        @rtype: list
        @return: list of conflicts
        '''
        return self.conflicting
        
    
    def GetMerging(self):
        '''
        Getter for diffs that are possible to merge
        @rtype: list
        @return: list of all diffs that are possible to merge
        '''
        return self.merging
    
    def GetBaseWorkDiffer(self):
        '''
        Getter for base to work differ
        @rtype: CDiffer
        @return: base to work differ
        '''
        return self.__baseWorkDiffer
    
    def GetBaseNewDiffer(self):
        '''
        Getter for base to new differ
        @rtype: CDiffer
        @return: base to new differ
        '''
        return self.__baseNewDiffer
        
    def __TryMerge(self):
        '''
        Method tries to merge all diffs from new and work project to base project,
        if it is not possible adds new conflict 
        '''
        # pokus sa zakomponovat zmeny z new a worku do base
        # ak to nepojde vyhlas to za konflikt a ponukni pouzivatelovi riesenie
        
        for diff in self.__baseWorkDiffer.dataDiff:
            # prejdi data diffy z base do work
            result = self.__FindConflictsForDataDiff(diff, self.__baseNewDiffer, self.__work)
            for c in result:
                self.__DataConflict(diff, c)
                
        for diff in self.__baseWorkDiffer.projectTreeDiff:
            # prejdi project tree diffy z base do work
            result = self.__FindConflictsForProjectTreeDiff(diff, self.__baseNewDiffer, self.__work)
            for c in result:
                self.__ProjectTreeConflict(diff, c)
                
        for diff in self.__baseWorkDiffer.visualDiff:
            # prejdi visual diffy z base do work
            result = self.__FindConflictsForVisualDiff(diff, self.__baseNewDiffer, self.__work)
            for c in result:
                self.__VisualConflict(diff, c)
        
        
        
        for diff in self.__baseNewDiffer.dataDiff:
            # prejdi data diffy z base do new
            result = self.__FindConflictsForDataDiff(diff, self.__baseWorkDiffer, self.__new)
            for c in result:
                self.__DataConflict(c, diff)
                
        for diff in self.__baseNewDiffer.projectTreeDiff:
            # prejdi project tree diffy z base do new
            result = self.__FindConflictsForProjectTreeDiff(diff, self.__baseWorkDiffer, self.__new)
            for c in result:
                self.__ProjectTreeConflict(c, diff)
                
        for diff in self.__baseNewDiffer.visualDiff:
            # prejdi visual diffy z base do new
            result = self.__FindConflictsForVisualDiff(diff, self.__baseWorkDiffer, self.__new)
            for c in result:
                self.__VisualConflict(c, diff)
            
        
        for diff in self.__baseWorkDiffer.dataDiff:
            
            if diff not in [c.GetBaseWorkDiff() for c in self.conflicting]:
                relatedElements = self.__RelatedElements(diff, self.__base, self.__work)
                intersection = set.intersection(set(relatedElements),set([c.GetBaseWorkDiff().GetElement() for c in self.conflicting if c.GetBaseWorkDiff().GetAction() == EDiffActions.DELETE]))
                if len(intersection) == 0:
                    self.__MergeDataDiff(diff)
                else:
                    self.__DataConflict(diff, CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), list(intersection))
        
        for diff in self.__baseWorkDiffer.projectTreeDiff:
            if diff not in [c.GetBaseWorkDiff() for c in self.conflicting]:
                if diff.GetElement().GetParent() not in [c.GetBaseWorkDiff().GetElement() for c in self.conflicting if c.GetBaseWorkDiff().GetAction() == EDiffActions.DELETE]:
                    self.__MergeProjectTreeDiff(diff)
                else:
                    self.__ProjectTreeConflict(diff, CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), [diff.GetElement().GetParent()])
     
        for diff in self.__baseWorkDiffer.visualDiff:
            if diff not in [c.GetBaseWorkDiff() for c in self.conflicting]:
                
                relatedElements = self.__RelatedElements(diff, self.__base, self.__work)
                
                intersection = set.intersection(set(relatedElements),set([c.GetBaseWorkDiff().GetElement() for c in self.conflicting if c.GetBaseWorkDiff().GetAction() == EDiffActions.DELETE])) 
                if len(intersection) == 0:
                    self.__MergeDataDiff(diff)
                else:
                    self.__VisualConflict(diff, CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), list(intersection))
                
        for diff in self.__baseNewDiffer.dataDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                
                relatedElements = self.__RelatedElements(diff, self.__base, self.__new)
                
                intersection = set.intersection(set(relatedElements),set([c.GetBaseNewDiff().GetElement() for c in self.conflicting if c.GetBaseNewDiff().GetAction() == EDiffActions.DELETE])) 
                if len(intersection) == 0:
                    self.__MergeDataDiff(diff)
                else:
                    self.__DataConflict(CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), diff, list(intersection))
                
        for diff in self.__baseNewDiffer.projectTreeDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                if diff.GetElement().GetParent() not in [c.GetBaseNewDiff().GetElement() for c in self.conflicting if c.GetBaseNewDiff().GetAction() == EDiffActions.DELETE]:
                    self.__MergeProjectTreeDiff(diff)
                else:
                    self.__ProjectTreeConflict(CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), diff, [diff.GetElement().GetParent()])
                
        for diff in self.__baseNewDiffer.visualDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                
                relatedElements = self.__RelatedElements(diff, self.__base, self.__new)
                
                intersection = set.intersection(set(relatedElements),set([c.GetBaseNewDiff().GetElement() for c in self.conflicting if c.GetBaseNewDiff().GetAction() == EDiffActions.DELETE])) 
                
                if len(intersection) == 0:
                    self.__MergeDataDiff(diff)
                else:
                    self.__VisualConflict(CDiffResult(EDiffActions.LET, diff.GetElement(), diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath(), message="Let "+diff.GetElement() + " in place"), diff, list(intersection))
                
    
    def __RelatedElements(self, diff, base, other):
        '''
        Returns related elements for object in diff
        @type diff: CDiffResult
        @param diff: diff for which we find related elements
        @type base: CProject
        @param base: 
        @type other: CProject
        @param other: 
        @rtype: list
        @return: related elements
        '''
        p = other
        relatedElements = []
        
        
        if diff.GetAction() == EDiffActions.DELETE:
            p = base
        
                
                
        if isinstance(diff.GetElement(), CBase):
            
            if isinstance(diff.GetElement(), CConnection):
                connectedElements = [p.GetProjectTreeNodeById(diff.GetElement().GetSource().GetId()), p.GetProjectTreeNodeById(diff.GetElement().GetDestination().GetId())]
                parentsSource = p.GetProjectTreeNodeById(connectedElements[0].GetId()).GetAllParents()
                parentsDestination = p.GetProjectTreeNodeById(connectedElements[1].GetId()).GetAllParents()
                relatedElements = connectedElements + parentsSource + parentsDestination
            else:        
                relatedElements = p.GetProjectTreeNodeById(diff.GetElement().GetId()).GetAllParents()
        
        elif isinstance(diff.GetElement(), CProjectTreeNode):
            relatedElements = diff.GetElement().GetAllParents()
        
        
        elif isinstance(diff.GetElement(), CBaseView):
            if isinstance(diff.GetElement(), CConnectionView):
                connectedElements = [p.GetProjectTreeNodeById(diff.GetElement().GetObject().GetSource().GetId()), p.GetProjectTreeNodeById(diff.GetElement().GetObject().GetDestination().GetId())]
                parentsSource = p.GetProjectTreeNodeById(connectedElements[0].GetId()).GetAllParents()
                parentsDestination = p.GetProjectTreeNodeById(connectedElements[1].GetId()).GetAllParents()
                relatedElements = connectedElements + parentsSource + parentsDestination
                relatedViews = [diff.GetElement().GetParentDiagram().GetViewById(connectedElements[0].GetId()), diff.GetElement().GetParentDiagram().GetViewById(connectedElements[1].GetId())]
                relatedElements = relatedElements + relatedViews
            
            else:        
                relatedElements = p.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents() +[diff.GetElement().GetObject()]
        
        return relatedElements        
        
        
    def __FindConflictsForDataDiff(self, diff, otherDiffer, project):
        '''
        Finds if data diff is not in conflict with diffs in other differ
        @type diff: CDiffResult
        @param diff: checking diff
        @type otherDiffer: CDiffer
        @param otherDiffer: other differ to search for conflicting diffs
        @type project: CProject
        @param project: Project for searching in elements
        @rtype: list
        @return: List of conflicting diffs in other differ
        '''
        result = []
        
        relatedElements = []
        if diff.GetAction() != EDiffActions.DELETE:
            # zisti vsetky elementy vo vztahu
            if isinstance(diff.GetElement(), CConnection):
                connectedElements = [project.GetProjectTreeNodeById(diff.GetElement().GetSource().GetId()), project.GetProjectTreeNodeById(diff.GetElement().GetDestination().GetId())]
                parentsSource = project.GetProjectTreeNodeById(connectedElements[0].GetId()).GetAllParents()
                parentsDestination = project.GetProjectTreeNodeById(connectedElements[1].GetId()).GetAllParents()
                relatedElements = connectedElements + parentsSource + parentsDestination
            else:        
                relatedElements = project.GetProjectTreeNodeById(diff.GetElement().GetId()).GetAllParents()
        
        
        if diff.GetAction() == EDiffActions.MODIFY:
            
            
            
            # ak som upravoval datove zlozky
            for d in otherDiffer.GetDataDiff().get(EDiffActions.MODIFY, []):
                # prejdi vsetky data diffy z druheho, kde som tiez upravoval
                if d.GetElement() == diff.GetElement() and d.GetDataPath() == diff.GetDataPath() and d.GetNewState() != diff.GetNewState():
                    # ak som upravoval na rovnakom mieste datovu zlozku
                    result.append(d)


            
                
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky data diffy z druheho, ktore som vymazal
                if d.GetElement() == diff.GetElement() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    # upravoval som vymazany element
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement() or d.GetElement() in relatedElements:
                    # upravoval som vymazany element                    
                    result.append(d)
                    
            
        
        elif diff.GetAction() == EDiffActions.INSERT:
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in relatedElements:
                    # pozri ci je na ceste k vlozenemu elementu
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in [p.GetObject() for p in relatedElements]:
                    # pozri ci je na ceste k vlozenemu elementu
                    result.append(d)
        
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
        
        return result
    
    def __MergeDataDiff(self, diff):
        '''
        Append diff to merging
        @type diff: CDiffResult
        @param diff: diff to be appended
        '''
        self.merging.append(diff)
    
    def __DataConflict(self, baseWorkDiff, baseNewDiff, relatedObjects = None):
        '''
        Creates and append new data conflict to conflicting
        @type baseWorkDiff: CDiffResult
        @param baseWorkDiff: first diff in conflict
        @type baseNewDiff: CDiffResult
        @param baseNewDiff: second diff in conflict
        @type relatedObjects: list
        @param relatedObjects: related objects for conflict
        '''
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Data Conflict', relatedObjects)
        if conflict not in self.conflicting:
            self.conflicting.append(conflict)    
        
    
    
    
    
    def __FindConflictsForProjectTreeDiff(self, diff, otherDiffer, project):
        '''
        Finds if project tree diff is not in conflict with diffs in other differ
        @type diff: CDiffResult
        @param diff: checking diff
        @type otherDiffer: CDiffer
        @param otherDiffer: other differ to search for conflicting diffs
        @type project: CProject
        @param project: Project for searching in elements
        @rtype: list
        @return: List of conflicting diffs in other differ
        '''
        result = []
        if diff.GetAction() == EDiffActions.INSERT:
            # ak som pridaval project tree node
            
            # zisti vsetkych jeho parentov a zabran ich vymazaniu
            parents = project.GetProjectTreeNodeById(diff.GetElement().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in parents:
                    # pozri ci je na ceste k vlozenemu elementu
                    result.append(d)
            
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
            
        elif diff.GetAction() == EDiffActions.MOVE:
            # zisti vsetkych jeho parentov a zabran ich vymazaniu
            parents = project.GetProjectTreeNodeById(diff.GetElement().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in parents:
                    # pozri ci je na ceste k presunutemu elementu
                    result.append(d)
                if d.GetElement() == diff.GetElement():
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.MOVE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        # ak som presunul ten isty element na ine miesto
                        result.append(d)
                        
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetObject():
                    result.append(d)
                if d.GetElement() in [p.GetObject() for p in parents]:
                    result.append(d)
        
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            parents = project.GetProjectTreeNodeById(diff.GetElement().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement():
                    # zmenil som poradie na vymazanom elemente
                    result.append(d)
                if d.GetElement() in parents:
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.ORDER_CHANGE, []):
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        # presunutie toho isteho elementu na rozne miesto
                        result.append(d)
                        
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetObject():
                    result.append(d)
                if d.GetElement() in [p.GetObject() for p in parents]:
                    result.append(d)
       
        
        return result
       
    def __MergeProjectTreeDiff(self, diff):
        '''
        Append diff to merging
        @type diff: CDiffResult
        @param diff: diff to be appended
        '''
        self.merging.append(diff)
        
    
    def __ProjectTreeConflict(self, baseWorkDiff, baseNewDiff, relatedObjects = None):
        '''
        Creates and append new project tree conflict to conflicting
        @type baseWorkDiff: CDiffResult
        @param baseWorkDiff: first diff in conflict
        @type baseNewDiff: CDiffResult
        @param baseNewDiff: second diff in conflict
        @type relatedObjects: list
        @param relatedObjects: related objects for conflict
        '''
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Project tree Conflict', relatedObjects)
        if conflict not in self.conflicting:
            self.conflicting.append(conflict)
            
    
    def __FindConflictsForVisualDiff(self, diff, otherDiffer, project):
        '''
        Finds if visual diff is not in conflict with diffs in other differ
        @type diff: CDiffResult
        @param diff: checking diff
        @type otherDiffer: CDiffer
        @param otherDiffer: other differ to search for conflicting diffs
        @type project: CProject
        @param project: Project for searching in elements
        @rtype: list
        @return: List of conflicting diffs in other differ
        '''
        result = []
        # zisti vsetky elementy vo vztahu
        #print diff
        
        relatedElements = []
        relatedViews = []
        if diff.GetAction() != EDiffActions.DELETE:
            if isinstance(diff.GetElement(), CConnectionView):
                connectedElements = [project.GetProjectTreeNodeById(diff.GetElement().GetObject().GetSource().GetId()), project.GetProjectTreeNodeById(diff.GetElement().GetObject().GetDestination().GetId())]
                parentsSource = project.GetProjectTreeNodeById(connectedElements[0].GetId()).GetAllParents()
                parentsDestination = project.GetProjectTreeNodeById(connectedElements[1].GetId()).GetAllParents()
                relatedElements = connectedElements + parentsSource + parentsDestination
                relatedViews = [diff.GetElement().GetParentDiagram().GetViewById(connectedElements[0].GetId()), diff.GetElement().GetParentDiagram().GetViewById(connectedElements[1].GetId())]
                
            else:        
                relatedElements = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
        
        
        
        if diff.GetAction() == EDiffActions.INSERT:
            #parents = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE,[]):
                if d.GetElement().GetObject() == diff.GetElement().GetParentDiagram() or d.GetElement() in relatedElements:
                    result.append(d)
            
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    result.append(d)
                    
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() in relatedViews:
                    result.append(d)
            
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
            
        elif diff.GetAction() == EDiffActions.MODIFY:
            
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE,[]):
                if d.GetElement() == diff.GetElement() or d.GetElement() in relatedViews:
                    result.append(d)
                    
                    
            #parents = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement().GetParentDiagram() or d.GetElement() in relatedElements:
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram()  or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    result.append(d)
                    
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.MODIFY,[]):
                if d.GetElement() == diff.GetElement() and d.GetDataPath() == diff.GetDataPath() and d.GetNewState() != diff.GetNewState():
                    result.append(d)
                    
            
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.ORDER_CHANGE, []):
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        result.append(d)
            
            
            #parents = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
                        
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE,[]):
                if d.GetElement() == diff.GetElement():
                    result.append(d)
            
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement().GetParentDiagram() or d.GetElement() in relatedElements:
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    result.append(d)
        return result
    
    
    def __MergeVisualDiff(self, diff):
        '''
        Append diff to merging
        @type diff: CDiffResult
        @param diff: diff to be appended
        '''
        self.merging.append(diff)
    
    def __VisualConflict(self, baseWorkDiff, baseNewDiff, relatedObjects = None):
        '''
        Creates and append new visual conflict to conflicting
        @type baseWorkDiff: CDiffResult
        @param baseWorkDiff: first diff in conflict
        @type baseNewDiff: CDiffResult
        @param baseNewDiff: second diff in conflict
        @type relatedObjects: list
        @param relatedObjects: related objects for conflict
        '''
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Visual Conflict', relatedObjects)
        if conflict not in self.conflicting:
            self.conflicting.append(conflict)    