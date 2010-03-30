'''
Created on 14.3.2010

@author: Peterko
'''

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
        
    def GetId(self):
        return self.__id
    
    def AppendChildElement(self, child):
        self.__childElements[child.GetId()] = child
        self.__childElementsOrdered.append(child)
    
    def AppendChildDiagram(self, child):
        self.__childDiagrams[child.GetId()] = child
        self.__childDiagramsOrdered.append(child)
        
    def GetChild(self, id):
        return self.__childElements.get(id) or self.__childDiagrams.get(id)
    
    def GetChilds(self):
        result = self.__childDiagrams.copy()
        result.update(self.__childElements)
        return result
    
    def GetChildsOrdered(self):
        return self.__childDiagramsOrdered + self.__childElementsOrdered
    
    def GetObject(self):
        return self.__objectRepresentation
    
    def GetParent(self):
        return self.__parent
    
    def __str__(self):
        return 'Tree node '+str(self.__objectRepresentation)
    
    def __hash__(self):
        return hash(self.GetId())
    
    def __cmp__(self, other):
        return cmp(self.GetId(), other.GetId())