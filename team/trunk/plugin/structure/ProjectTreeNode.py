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
        self.__index = 0
    
    def SetIndex(self, index):
        self.__index = index
        
    def GetIndex(self):
        return self.__index
        
    def GetId(self):
        return self.__id
    
    def AddChildElement(self, child, index = None):
        self.__childElements[child.GetId()] = child
        if index is not None:
            self.__childElementsOrdered.insert(index, child)
        else:
            self.__childElementsOrdered.append(child)
        child.SetIndex(index or len(self.__childElementsOrdered)-1)
    
    def AddChildDiagram(self, child, index = None):
        self.__childDiagrams[child.GetId()] = child
        if index is not None:
            self.__childDiagramsOrdered.insert(index,child)
        else:
            self.__childDiagramsOrdered.append(child)
            
        child.SetIndex(index or len(self.__childDiagramsOrdered)-1)
        
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
    
    
    def GetChildsOrdered(self):
        return self.__childDiagramsOrdered + self.__childElementsOrdered
    
    def GetObject(self):
        return self.__objectRepresentation
    
    def GetParent(self):
        return self.__parent
    
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
    
    def __str__(self):
        return 'Tree node '+str(self.__objectRepresentation)
    
    def __hash__(self):
        return hash(self.GetId())
    
    def __cmp__(self, other):
        return cmp(self.GetId(), other.GetId())