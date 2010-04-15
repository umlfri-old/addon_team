'''
Created on 2.4.2010

@author: Peterko
'''
from Differ import CDiffer
from DiffActions import EDiffActions
import itertools
from structure import CProjectTreeNode
from structure import CConnection, CConnectionView
from Conflict import CConflict

class CConflicter(object):
    '''
    classdocs
    '''


    def __init__(self, newProject, baseProject, workProject):
        '''
        Constructor
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
        return self.conflicting
        
    
    def GetMerging(self):
        return self.merging
        
    def __TryMerge(self):
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
                self.__MergeDataDiff(diff)
        
        for diff in self.__baseWorkDiffer.projectTreeDiff:
            if diff not in [c.GetBaseWorkDiff() for c in self.conflicting]:
                self.__MergeProjectTreeDiff(diff)
     
        for diff in self.__baseWorkDiffer.visualDiff:
            if diff not in [c.GetBaseWorkDiff() for c in self.conflicting]:
                self.__MergeVisualDiff(diff)
                
        for diff in self.__baseNewDiffer.dataDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                self.__MergeDataDiff(diff)
                
        for diff in self.__baseNewDiffer.projectTreeDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                self.__MergeProjectTreeDiff(diff)
                
        for diff in self.__baseNewDiffer.visualDiff:
            if diff not in [c.GetBaseNewDiff() for c in self.conflicting]:
                self.__MergeVisualDiff(diff)
                
        
        
    def __FindConflictsForDataDiff(self, diff, otherDiffer, project):
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
                    print 'modyfing same data of elements different way'
                    result.append(d)


            
                
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky data diffy z druheho, ktore som vymazal
                if d.GetElement() == diff.GetElement() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    # upravoval som vymazany element
                    print 'modifying data of deleted element'
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement() or d.GetElement() in relatedElements:
                    # upravoval som vymazany element
                    print 'modifying data of deleted element'
                    result.append(d)
                    
            
        
        elif diff.GetAction() == EDiffActions.INSERT:
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in relatedElements:
                    # pozri ci je na ceste k vlozenemu elementu
                    print 'insert element under deleted element'
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in [p.GetObject() for p in relatedElements]:
                    # pozri ci je na ceste k vlozenemu elementu
                    print 'insert element under deleted element'
                    result.append(d)
        
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
        
        return result
    
    def __MergeDataDiff(self, diff):
        
        self.merging.append(diff)
    
    def __DataConflict(self, baseWorkDiff, baseNewDiff):
        print 'data conflict'
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Data Conflict')
        if conflict not in self.conflicting:
            self.conflicting.append(conflict)    
        
    
    
    
    
    def __FindConflictsForProjectTreeDiff(self, diff, otherDiffer, project):
        result = []
        if diff.GetAction() == EDiffActions.INSERT:
            # ak som pridaval project tree node
            
            # zisti vsetkych jeho parentov a zabran ich vymazaniu
            parents = diff.GetElement().GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in parents:
                    # pozri ci je na ceste k vlozenemu elementu
                    print 'insert project tree node under deleted element'
                    result.append(d)
            
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
            
        elif diff.GetAction() == EDiffActions.MOVE:
            # zisti vsetkych jeho parentov a zabran ich vymazaniu
            parents = diff.GetElement().GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() in parents:
                    # pozri ci je na ceste k presunutemu elementu
                    print 'move project tree node under deleted node'
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.MOVE, []):
                # prejdi vsetky vymazane elementy
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        # ak som presunul ten isty element na ine miesto
                        print 'move project tree node under different parents'
                        result.append(d)
        
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            parents = diff.GetElement().GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement():
                    # zmenil som poradie na vymazanom elemente
                    print 'change order of deleted node'
                    result.append(d)
                if d.GetElement() in parents:
                    print 'change order under deleted node'
                    result.append(d)
                    
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.ORDER_CHANGE, []):
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        # presunutie toho isteho elementu na rozne miesto
                        print 'change order of same nodes differently'
                        result.append(d)
       
        
        return result
       
    def __MergeProjectTreeDiff(self, diff):
        
        self.merging.append(diff)
        
    
    def __ProjectTreeConflict(self, baseWorkDiff, baseNewDiff):
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Project tree Conflict')
        print 'project tree conflict adding trying'
        if conflict not in self.conflicting:
            print 'project tree conflict ADDED'
            self.conflicting.append(conflict)
        else:
            print 'project tree conflict NOT ADDED'    
    
    def __FindConflictsForVisualDiff(self, diff, otherDiffer, project):
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
                    print 'insert view under deleted diagram'
                    result.append(d)
            
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    print 'insert view under deleted diagram'
                    result.append(d)
                    
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() in relatedViews:
                    print 'deleted view for inserted connection'
                    result.append(d)
            
        elif diff.GetAction() == EDiffActions.DELETE:
            pass
            
        elif diff.GetAction() == EDiffActions.MODIFY:
            
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE,[]):
                if d.GetElement() == diff.GetElement() or d.GetElement() in relatedViews:
                    print 'modifying deleted view'
                    result.append(d)
                    
                    
            #parents = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement().GetParentDiagram() or d.GetElement() in relatedElements:
                    print 'modifying view in deleted diagram'
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram()  or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    print 'modifying view in deleted diagram'
                    result.append(d)
                    
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.MODIFY,[]):
                if d.GetElement() == diff.GetElement() and d.GetDataPath() == diff.GetDataPath() and d.GetNewState() != diff.GetNewState():
                    print 'modifying same visual data of views differently'
                    result.append(d)
                    
            
        elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.ORDER_CHANGE, []):
                if d.GetElement() == diff.GetElement():
                    if d.GetNewState() != diff.GetNewState():
                        print 'changing order of same views differently'
                        result.append(d)
            
            
            #parents = project.GetProjectTreeNodeById(diff.GetElement().GetParentDiagram().GetId()).GetAllParents()
                        
            for d in otherDiffer.GetVisualDiff().get(EDiffActions.DELETE,[]):
                if d.GetElement() == diff.GetElement():
                    print 'changing order of deleted view'
                    result.append(d)
            
            for d in otherDiffer.GetProjectTreeDiff().get(EDiffActions.DELETE, []):
                if d.GetElement().GetObject() == diff.GetElement().GetParentDiagram() or d.GetElement() in relatedElements:
                    print 'changing order of view in deleted diagram'
                    result.append(d)
                    
            for d in otherDiffer.GetDataDiff().get(EDiffActions.DELETE, []):
                if d.GetElement() == diff.GetElement().GetParentDiagram() or d.GetElement() in [p.GetObject() for p in relatedElements]:
                    print 'changing order of view in deleted diagram'
                    result.append(d)
        return result
    
    
    def __MergeVisualDiff(self, diff):
        
        self.merging.append(diff)
    
    def __VisualConflict(self, baseWorkDiff, baseNewDiff):
        conflict = CConflict(baseWorkDiff, baseNewDiff, 'Visual Conflict')
        if conflict not in self.conflicting:
            self.conflicting.append(conflict)    
        
        
        

        
        
        
    def __str__(self):
        return 'new: '+str(self.__new.GetProjectTreeRoot()) \
            + 'old: '+str(self.__base.GetProjectTreeRoot()) \
            + 'work: '+str(self.__work.GetProjectTreeRoot())