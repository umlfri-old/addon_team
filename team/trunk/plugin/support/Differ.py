'''
Created on 27.2.2010

@author: Peterko
'''
from difflib import *
from DiffResult import CDiffResult
from DiffActions import EDiffActions
from dictToTuple import dictToTuple, tupleToDict
import copy

class CDiffer(object):
    '''
    Class that provides diffing capabilities
    '''


    def __init__(self, project1, project2):
        '''
        Constructor
        @type project1: CProject
        @param project1: Old project included in diff
        @type project2: CProject
        @param project2: New project included in diff
        '''
        self.__project1 = project1
        self.__project2 = project2
        
        
        self.visualDiff = []
        self.projectTreeDiff = []
        self.dataDiff = []
        self.__DiffProjects()
        
        
        
    def __DiffProjects(self):
        '''
        Diffs projects, data diff, project tree diff, visual diff
        '''
        result = []
        elements1 = self.__project1.GetElements().values()
        elements1.sort()
        elements2 = self.__project2.GetElements().values()
        elements2.sort()
        smElements = SequenceMatcher(None, elements1, elements2)
        
        diagrams1 = self.__project1.GetDiagrams().values()
        diagrams1.sort()
        diagrams2 = self.__project2.GetDiagrams().values()
        diagrams2.sort()
        smDiagrams = SequenceMatcher(None, diagrams1, diagrams2)
        
        connections1 = self.__project1.GetConnections().values()
        connections1.sort()
        connections2 = self.__project2.GetConnections().values()
        connections2.sort()
        smConnections = SequenceMatcher(None, connections1, connections2)
        
        diagramsOpcodes = smDiagrams.get_opcodes()
        
        elementsOpcodes = smElements.get_opcodes()
        
        connectionsOpcodes = smConnections.get_opcodes()
        
        
        self.__ComputeDiff(diagramsOpcodes, diagrams1, diagrams2)
        self.__ComputeDiff(elementsOpcodes, elements1, elements2)
        self.__ComputeDiff(connectionsOpcodes, connections1, connections2)
        
        
        self.projectTreeDiff.extend(self.__DiffProjectTree())
        
        
        for id,diagrams in self.__MatchingDiagrams().items():
            
            
            if diagrams[0] is not None and diagrams[1] is not None:
                elViews1 = diagrams[0].GetElementViewsOrdered()
                elViews2 = diagrams[1].GetElementViewsOrdered()
                self.visualDiff.extend(self.__DiffOrder(elViews1, elViews2))
            
            
            matchingViews = self.__MatchingViews(diagrams[0], diagrams[1])
            for id, views in matchingViews.items():
                self.visualDiff.extend(self.__DiffElementsVisual(views[0], views[1]))
        

    def __MatchingDiagrams(self):
        '''
        Returns dictionary of matching diagrams from two projects
        @rtype: dic
        @return: Dictionary of matching diagrams
        '''
        uniqueDiagramIds = list(set(self.__project1.GetDiagrams().keys()+self.__project2.GetDiagrams().keys()))
        result = {}
        for id in uniqueDiagramIds:
            result[id] = (self.__project1.GetById(id), self.__project2.GetById(id))
        return result
    
    def __MatchingViews(self, diagram1, diagram2):
        '''
        Returns dictionary of matching views in given diagrams
        @type diagram1: CDiagram
        @param diagram1: First diagram
        @type diagram2: CDiagram
        @param diagram2: Second diagram
        @rtype: dic
        @return: Dictionary of matching views
        '''
        result = {}
        if diagram1 is None:
            diag2ViewIds = diagram2.GetViews().keys()
            for id in diag2ViewIds:
                result[id] = (None, diagram2.GetViewById(id))
        elif diagram2 is None:
            diag1ViewIds = diagram1.GetViews().keys()
            for id in diag1ViewIds:
                result[id] = (diagram1.GetViewById(id), None)
        else:
            uniqueViewIds = list(set(diagram1.GetViews().keys()+diagram2.GetViews().keys()))
            for id in uniqueViewIds:
                result[id] = (diagram1.GetViewById(id), diagram2.GetViewById(id))
            
        return result
        
    def __ComputeDiff(self, opcodes, sequence1, sequence2):
        '''
        Computes diff between two sequences of whatever
        @type opcodes: tuple
        @param opcodes: Opcodes, result from sequence matcher
        @type sequence1: tuple
        @param sequence1: First sequence in comparison
        @type sequence2: tuple
        @param sequence2: Second sequence in comparison
        '''
        for tag, i1, i2, j1, j2 in opcodes:
            if (tag == EDiffActions.DELETE):
                
                for si in sequence1[i1:i2]:
                    newDiffResult = CDiffResult(EDiffActions.DELETE, si, message=_("Deleted ")+str(si))
                    self.dataDiff.append(newDiffResult)
            elif (tag == EDiffActions.INSERT):
                
                for si in sequence2[j1:j2]:
                    newDiffResult = CDiffResult(EDiffActions.INSERT, si, message=_("Inserted ")+str(si))
                    self.dataDiff.append(newDiffResult)
            elif (tag == EDiffActions.REPLACE):
                
                for si1 in sequence1[i1:i2]:
                    self.dataDiff.append(CDiffResult(EDiffActions.DELETE, si1, message=_("Deleted ") +str(si1)))
                for si2 in sequence2[j1:j2]:                    
                    self.dataDiff.append(CDiffResult(EDiffActions.INSERT, si2, message=_("Inserted ")+str(si2)))
            if (tag == EDiffActions.EQUAL):
                
                for si1, si2 in zip(sequence1[i1:i2], sequence2[j1:j2]):
                    self.dataDiff.extend(self.__DiffElementsData(si1, si2))
                    
    
    def __DiffElementsData(self, el1, el2):
        '''
        Computes diff between data of two elements
        @type el1: CBase
        @param el1: First element in comparison
        @type el2: CBase
        @param el2: Second element in comparison
        @rtype: list
        @return: List of computed diffs
        '''
        data1 = el1.GetData()
        
        data2 = el2.GetData()
        
        tuple1 = dictToTuple(data1)
        
        tuple2 = dictToTuple(data2)
        
        result = []
         
        if data1 == data2:
            
            pass
        else:
            self.__DiffData(el1, el2, tuple1, tuple2, result, [])
        return result
    
    def __DiffData(self, el1, el2, tuple1, tuple2, result, dataPath):
        '''
        Computes diff between two tuples found in two elements recursive
        @type el1: object
        @param el1: any object from structure
        @type el2: object
        @param el2: any object from structure
        @type tuple1: tuple
        @param tuple1: first tuple in comparison
        @type tuple2: tuple
        @param tuple2: second tuple in comparison
        @type result: list
        @param result: parameter where result will be stored after execution
        @type dataPath: list
        @param dataPath: sequence path to given modification
        
        '''
        sm = SequenceMatcher(None, tuple1, tuple2)
        op = sm.get_opcodes()
        
        for tag, i1, i2, j1, j2 in op:
            if (tag == EDiffActions.EQUAL):
                pass
            elif (tag == EDiffActions.DELETE):
        
                for seq in tuple1[i1:i2]:
                    if type(seq[0]) == type(''):
                        d = tupleToDict((seq,))
                    else:
                        d = tupleToDict(seq)
                    
                    result.append(CDiffResult(EDiffActions.MODIFY, el1, d, None, dataPath, message=_("Deleted ")+str(d)+_(" from ")+str(el1)+_(" in path ")+str(dataPath)))
            elif (tag == EDiffActions.INSERT):
                for seq in tuple2[j1:j2]:
                    if type(seq[0]) == type(''):
                        d = tupleToDict((seq,))
                    else:
                        d = tupleToDict(seq)
                    
                    result.append(CDiffResult(EDiffActions.MODIFY, el2, None, d, dataPath, message=_("Inserted ")+str(d)+_(" into ")+str(el2)+_(" in path ")+str(dataPath)))
        
                pass
            elif (tag == EDiffActions.REPLACE):
                
                if (j2 - j1 > i2 - i1):
                    r = j2 - j1
                else :
                    r = i2 - i1
                for i in range(r):
                    try:
                        seq1 = tuple1[i1+i]
                    except :
                        seq1 = ()
                    try:
                        seq2 = tuple2[j1+i]
                    except:
                        seq2 = ()
                    if (seq2 == ()):
                        seq1 = (seq1,)
                    if (seq1 == ()):
                        seq2 = (seq2,)
                    
                    try:
                        if type(seq1[0]) == type('') and type(seq1[1]) == type(u''):
                
                            myPath = copy.deepcopy(dataPath)
                            myPath.append(seq1[0])
                            if type(seq1[0]) == type(''):
                                d1 = tupleToDict((seq1,))
                            else:
                                d1 = tupleToDict(seq1)
                                
                            if type(seq2[0]) == type(''):
                                d2 = tupleToDict((seq2,))
                            else:
                                d2 = tupleToDict(seq2)
                            result.append(CDiffResult(EDiffActions.MODIFY, el1, d1, d2, myPath, message=_("Modified ")+str(d1)+_(" from ")+str(el1)+_(" in path ")+str(dataPath)+_(" : New value ")+str(d2)))
                        else:
                            myPath = copy.deepcopy(dataPath)
                            if type(seq1[0]) == type(''):
                
                                myPath.append(seq1[0])
                            elif type(tuple1[0]) != type(''):
                                if len(seq1) == 1:
                                    myPath.append(tuple1.index(seq1[0]))
                                else:
                                    myPath.append(tuple1.index(seq1))
                            
                            self.__DiffData(el1, el2, seq1, seq2, result, myPath)
                    except :
                        myPath = copy.deepcopy(dataPath)
                        if type(seq2[0]) == type(''):
                            myPath.append(seq2[0])
                        elif type(tuple2[0]) != type(''):
                            if len(seq2) == 1:
                                myPath.append(tuple2.index(seq2[0]))
                            else:
                                myPath.append(tuple2.index(seq2))
                        
                        self.__DiffData(el1, el2, seq1, seq2, result, myPath)



    def __DiffElementsLogical(self, el1, el2):
        '''
        Diff elements logical (data diff)
        @type el1: CBase
        @param el1: First object for comparison
        @type el2: CBase
        @param el2: Second object for comparison
        @rtype: list
        @return: list of diff result for given elements
        '''
        if el1 is None and el2 is not None:
            return [CDiffResult(EDiffActions.INSERT, el2, message=_("Inserted ")+str(el2))]
        elif el1 is not None and el2 is None:
            return [CDiffResult(EDiffActions.DELETE, el1, message=_("Deleted ")+str(el1))]
        else:
            return self.__DiffElementsData(el1, el2) 
                    
    def __DiffElementsVisual(self, elView1, elView2):
        '''
        Diff elements visual
        @type elView1: CBaseView
        @param elView1: First view for comparison
        @type elView2: CBaseView
        @param elView2: Second view for comparison
        @rtype: list
        @return: list of diff result for given views
        '''
        if elView1 is None and elView2 is not None:
            return [CDiffResult(EDiffActions.INSERT, elView2, message=_("Inserted ")+str(elView2))]
        elif elView1 is not None and elView2 is None:
            return [CDiffResult(EDiffActions.DELETE, elView1, message=_("Deleted ")+str(elView1))]
        else:
            tuple1 = dictToTuple(elView1.GetViewData())
            tuple2 = dictToTuple(elView2.GetViewData())
            result = []
            self.__DiffData(elView1, elView2, tuple1, tuple2, result, [])
            return result
    
    def __DiffProjectTree(self, root1 = None, root2 = None):
        '''
        Diff project tree
        @type root1: CProjectTreeNode
        @param root1: Root of first project tree node
        @type root2: CProjectTreeNode
        @param root2: Root of second project tree node
        @rtype: list
        @return: list of diff result under given roots
        '''
        if root1 is None:
            root1 = self.__project1.GetProjectTreeRoot()
        if root2 is None:
            root2 = self.__project2.GetProjectTreeRoot()
    
        map1 = self.__TreeNodesParents(self.__project1)
        map2 = self.__TreeNodesParents(self.__project2)
        
        
        result = []
        for e in set(map1.keys()+map2.keys()):
            if e not in map1:
                result.append(CDiffResult(EDiffActions.INSERT, e, None, e.GetParent(), message=_("Inserted ")+str(e)+_(" under parent ")+str(e.GetParent())))
            elif e not in map2:
                result.append(CDiffResult(EDiffActions.DELETE, e, e.GetParent(), message=_("Deleted ")+str(e)+_(" under parent ")+str(e.GetParent())))
            elif map2[e] != map1[e]:
                oldParent = self.__project1.GetProjectTreeNodeById(e.GetId()).GetParent()
                newParent = self.__project2.GetProjectTreeNodeById(e.GetId()).GetParent()
                result.append(CDiffResult(EDiffActions.MOVE, 
                                          e, 
                                          oldParent, 
                                          newParent,
                                          message=_("Moved ")+str(e)+_(" from parent ")+str(oldParent)+ _(" under parent ")+str(newParent)))
        for parent in set(map1.values()+map2.values()):
            if parent is not None:
                
                p = self.__project1.GetProjectTreeNodeById(parent.GetId())
                childs1 = []
                if p is not None:
                    childs1 = p.GetChildsOrdered()
                
                p = self.__project2.GetProjectTreeNodeById(parent.GetId())
                childs2 = []
                if p is not None:
                    childs2 = p.GetChildsOrdered()
                
                
                result.extend(self.__DiffOrder(childs1, childs2))
                
        return result
        
        
    def __DiffOrder(self, list1, list2):
        '''
        Computes order changes in given lists
        @type list1: list
        @param list1: First list to be compared
        @type list2: list
        @param list2: Second list to be compared
        @rtype: list
        @return: Diff results of order change in lists
        '''
        reducedChilds1 = [c for c in list1 if c in list2]
                
        reducedChilds2 = [c for c in list2 if c in list1]
        
        result = []
        
        for rc in reducedChilds1:
            index1 = reducedChilds1.index(rc)
            index2 = reducedChilds2.index(rc)
            oldOriginalIndex = list1.index(rc)
            newOriginalIndex = list2.index(rc)
            if index1 != index2:
                result.append(CDiffResult(EDiffActions.ORDER_CHANGE, rc, oldOriginalIndex, newOriginalIndex,
                                          message = _("Changed order of ")+str(rc)+ _("from index ")+str(oldOriginalIndex)+ _(" to index ")+str(newOriginalIndex)))
        
        return result
                
                

    
    
    def __TreeNodesParents(self, project):
        '''
        Creates map of tree nodes and its parents
        @type project: CProject
        @param project: Project for which map has to be created
        @rtype: dic
        @return: map of tree nodes and its parents
        '''
        nodes = project.GetProjectTreeNodes()
        result = {}
        for node in nodes:
            result[node] = node.GetParent()
        return result
    
    def __DiffListToDict(self, diffList):
        '''
        Creates dic from list of diffs, keys are diff actions
        @type diffList: list
        @param diffList: list of diff to be converted
        @rtype: dic
        @return: Dictionaty from list of diffs
        '''
        result = {}
        for d in diffList:
            if d.GetAction() not in result:
                result[d.GetAction()] = [d]
            else:
                result[d.GetAction()].append(d)
                
        return result
    
    def GetProjectTreeDiff(self):
        '''
        Returns dic of project tree diffs
        @rtype: dic
        @return: dic of project tree diffs
        '''
        return self.__DiffListToDict(self.projectTreeDiff)
    
    def GetDataDiff(self):
        '''
        Returns dic of data diffs
        @rtype: dic
        @return: dic of data diffs
        '''
        return self.__DiffListToDict(self.dataDiff)
    
    def GetVisualDiff(self):
        '''
        Returns dic of visual diffs
        @rtype: dic
        @return: dic of visual diffs
        '''
        return self.__DiffListToDict(self.visualDiff)
    
    def GetOldProject(self):
        '''
        Returns old project
        @rtype: CProject
        @return: old project
        '''
        return self.__project1
    
    def GetNewProject(self):
        '''
        Returns new project
        @rtype: CProject
        @return: new project
        '''
        return self.__project2