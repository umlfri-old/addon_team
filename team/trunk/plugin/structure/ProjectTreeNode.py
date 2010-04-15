'''
Created on 14.3.2010

@author: Peterko
'''

from Element import CElement
from Diagram import CDiagram

class CProjectTreeNode(object):
    '''
    classdocs
    '''


    def __init__(self, objectRepresentation, parent=None):
        '''
        Constructor
        '''
        self.__id = objectRepresentation.GetId()
        self.__childElements = {}
        self.__childElementsOrdered = []
        self.__childDiagrams = {}
        self.__childDiagramsOrdered = []
        self.__objectRepresentation = objectRepresentation
        self.__parent = parent
        self.__index = 0
        self.__absoluteIndex = 0
    
#    def SetIndex(self, index):
#        self.__index = index
        
    def GetIndex(self):
        
        if self.__parent is not None:
            if isinstance(self.__objectRepresentation, CElement):
                
                return self.__parent.GetChildElementsOrdered().index(self)
            
            elif isinstance(self.__objectRepresentation, CDiagram):
                
                return self.__parent.GetChildDiagramsOrdered().index(self)
                
        else:
            return 0   
#    def SetAbsoluteIndex(self, index):
#        self.__absoluteIndex = index
    
    def GetAbsoluteIndex(self):
        if self.__parent is not None:
            return self.__parent.GetChildsOrdered().index(self)
        else:
            return 0
        
        
    def GetId(self):
        return self.__id
    
    def AddChild(self, child, index = None):
        if isinstance(child.GetObject(), CElement):
            self.AddChildElement(child, index)
        elif isinstance(child.GetObject(), CDiagram):
            self.AddChildDiagram(child, index)
    
    
    def AddChildElement(self, child, index = None):
        self.__childElements[child.GetId()] = child
        if index is not None:
            self.__childElementsOrdered.insert(index, child)
        else:
            self.__childElementsOrdered.append(child)
        
    
    def AddChildDiagram(self, child, index = None):
        self.__childDiagrams[child.GetId()] = child
        if index is not None:
            self.__childDiagramsOrdered.insert(index,child)
        else:
            self.__childDiagramsOrdered.append(child)
            
        
        
    def GetChild(self, id):
        return self.__childElements.get(id) or self.__childDiagrams.get(id)
    
    def GetChilds(self):
        result = self.__childDiagrams.copy()
        result.update(self.__childElements)
        return result
    
    def GetChildNodes(self):
        return self.__childElementsOrdered
    
    def GetChildDiagrams(self):
        return self.__childDiagramsOrdered
    
    
    def GetChildElementsOrdered(self):
        #self.__childElementsOrdered.sort(key=CProjectTreeNode.GetIndex)
        return self.__childElementsOrdered
    
    def GetChildDiagramsOrdered(self):
        #self.__childDiagramsOrdered.sort(key=CProjectTreeNode.GetIndex)
        return self.__childDiagramsOrdered
    
    def GetChildsOrdered(self):
        #self.__childDiagramsOrdered.sort(key=CProjectTreeNode.GetIndex)
        #self.__childElementsOrdered.sort(key=CProjectTreeNode.GetIndex)
        return self.__childDiagramsOrdered + self.__childElementsOrdered
    
    def GetObject(self):
        return self.__objectRepresentation
    
    def GetParent(self):
        return self.__parent
    
    def GetAllParents(self):
        result = []
        parent = self.GetParent()
        while parent is not None:
            result.append(parent)
            parent = parent.GetParent()
        return result
    
    def DeleteChild(self, child):
        #vymaze child a vrati vsetky jeho deti, aby mohli byt vymazane
        result = [child]
        ch = child.GetChildsOrdered()
        
        while len(ch) > 0:
            r = ch.pop()
            result.append(r)
            ch.extend(r.GetChildsOrdered())
            
        try:
            self.__childElements.pop(child.GetId())
            self.__childElementsOrdered.remove(child)
        except:
            pass
        try:
            self.__childDiagrams.pop(child.GetId())
            self.__childDiagramsOrdered.remove(child)
            
        except:
            pass
        return result
    
    def ChangeOrderNode(self, node, newIndex):
        try:
            self.__childElementsOrdered.remove(node)
            self.AddChildElement(node, newIndex)
        except:
            pass
        
        try:
            self.__childDiagramsOrdered.remove(node)
            self.AddChildDiagram(node, newIndex)
        except:
            pass
    
    def __str__(self):
        return 'Tree node '+str(self.__objectRepresentation)
    
    def __hash__(self):
        return hash(self.GetId()) + hash(self.__class__)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return hash(self) != hash(other)
    
    def __cmp__(self, other):
        return cmp(hash(self), hash(other))