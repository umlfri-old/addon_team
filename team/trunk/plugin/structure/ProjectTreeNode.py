'''
Created on 14.3.2010

@author: Peterko
'''

from Element import CElement
from Diagram import CDiagram

class CProjectTreeNode(object):
    '''
    Class representing project tree node of given data object
    '''


    def __init__(self, objectRepresentation, parent=None):
        '''
        Constructor
        @type objectRepresentation: CBase 
        @param objectRepresentation: Underlying data object
        @type parent: CProjectTreeNode
        @param parent: Parent of project tree node
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
    

        
    def GetIndex(self):
        '''
        Returns index of project tree node under its parent
        @rtype: int
        @return: index of project tree node under its parent
        '''
        if self.__parent is not None:
            if isinstance(self.__objectRepresentation, CElement):
                
                return self.__parent.GetChildElementsOrdered().index(self)
            
            elif isinstance(self.__objectRepresentation, CDiagram):
                
                return self.__parent.GetChildDiagramsOrdered().index(self)
                
        else:
            return 0   
    
    def GetAbsoluteIndex(self):
        '''
        Returns absolute index of project tree node under its parent
        @rtype: int
        @return: absolute index of project tree node under its parent
        '''
        if self.__parent is not None:
            return self.__parent.GetChildsOrdered().index(self)
        else:
            return 0
        
        
    def GetId(self):
        '''
        Returns identification
        @rtype: string
        @return: identification
        '''
        return self.__id
    
    def AddChild(self, child, index = None):
        '''
        Adds child under project tree node
        @type child: CProjectTreeNode
        @param child: Child to be added
        @type index: int
        @param index: desired index of child
        '''
        if isinstance(child.GetObject(), CElement):
            self.AddChildElement(child, index)
        elif isinstance(child.GetObject(), CDiagram):
            self.AddChildDiagram(child, index)
    
    
    def AddChildElement(self, child, index = None):
        '''
        Adds child element under project tree node
        @type child: CProjectTreeNode
        @param child: Child to be added
        @type index: int
        @param index: desired index of child
        '''
        self.__childElements[child.GetId()] = child
        if index is not None:
            self.__childElementsOrdered.insert(index, child)
        else:
            self.__childElementsOrdered.append(child)
        
    
    def AddChildDiagram(self, child, index = None):
        '''
        Adds child diagram under project tree node
        @type child: CProjectTreeNode
        @param child: Child to be added
        @type index: int
        @param index: desired index of child
        '''
        self.__childDiagrams[child.GetId()] = child
        if index is not None:
            self.__childDiagramsOrdered.insert(index,child)
        else:
            self.__childDiagramsOrdered.append(child)
            
        
        
    def GetChild(self, id):
        '''
        Returns child by given id
        @type id: string
        @param id: id of child to be retrieved
        @rtype: CProjectTreeNode
        @return: found project tree node or None
        '''
        return self.__childElements.get(id) or self.__childDiagrams.get(id)
    
    def GetChilds(self):
        '''
        Returns all childs of project tree node
        @rtype: dic
        @return: all childs of project tree node
        '''
        result = self.__childDiagrams.copy()
        result.update(self.__childElements)
        return result
    
    def GetChildNodes(self):
        '''
        Returns all childs element nodes of project tree node
        @rtype: dic
        @return: all childs element nodes of project tree node
        '''
        return self.__childElementsOrdered
    
    def GetChildDiagrams(self):
        '''
        Returns all childs diagram nodes of project tree node
        @rtype: dic
        @return: all childs diagram nodes of project tree node
        '''
        return self.__childDiagramsOrdered
    
    
    def GetChildElementsOrdered(self):
        '''
        Returns all childs element nodes of project tree node ordered
        @rtype: list
        @return: all childs element nodes of project tree node ordered
        '''
        return self.__childElementsOrdered
    
    def GetChildDiagramsOrdered(self):
        '''
        Returns all childs diagram nodes of project tree node ordered
        @rtype: list
        @return: all childs diagram nodes of project tree node ordered
        '''
        return self.__childDiagramsOrdered
    
    def GetChildsOrdered(self):
        '''
        Returns all childs of project tree node ordered
        @rtype: list
        @return: all childs of project tree node ordered
        '''
        return self.__childDiagramsOrdered + self.__childElementsOrdered
    
    def GetObject(self):
        '''
        Returns object representation
        @rtype: CBase
        @return: object representation
        '''
        return self.__objectRepresentation
    
    def GetParent(self):
        '''
        Returns parent of project tree node
        @rtype: CProjectTreeNode
        @return: parent of project tree node
        '''
        return self.__parent
    
    def GetAllParents(self):
        '''
        Returns all parents of project tree node
        @rtype: list
        @return: all parents of project tree node
        '''
        result = []
        parent = self.GetParent()
        while parent is not None:
            result.append(parent)
            parent = parent.GetParent()
        return result
    
    def DeleteChild(self, child):
        '''
        Deletes child under project tree node
        @type child: CProjectTreeNode
        @param child: project tree node child to be deleted
        @rtype: list
        @return: List of all childs and itself of child
        '''
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
        '''
        Change order of given child node
        @type node: CProjectTreeNode
        @param node: Node to be changed
        @type newIndex: int
        @param newIndex: new index of given node
        '''
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
        return 'Project tree node of \"'+str(self.__objectRepresentation)+'\"'
    
    def __hash__(self):
        return hash(self.GetId()) + hash(self.__class__)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return hash(self) != hash(other)
    
    def __cmp__(self, other):
        return cmp(hash(self), hash(other))