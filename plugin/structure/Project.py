'''
Created on 6.3.2010

@author: Peterko
'''
from Diagram import CDiagram
from Element import CElement
from Connection import CConnection
from ElementView import CElementView
from ConnectionView import CConnectionView
from lib.Depend.etree import etree
from lib.consts import UMLPROJECT_NAMESPACE
from ProjectTreeNode import CProjectTreeNode

class CProject(object):
    '''
    classdocs
    '''


    def __init__(self, project=None,xmlData=None):
        '''
        Constructor
        '''
        self.__diagrams = {}
        self.__elements = {}
        self.__connections = {}
        self.__projectTreeRoot = None
        if (xmlData is not None):
            self.__LoadProjectFromXml(xmlData)
        if (project is not None):
            self.__LoadProjectFromApp(project)
    
    def __LoadProjectFromApp(self, project):
        root = project.GetRoot()
        if root is not None:
            self.__LoadProjectRecursive(root, None)
   
    def __LoadProjectRecursive(self, root, treeParent):
        if root is not None:
            if root.GetClass().find('Element') != -1:
                # ak je to element
                
                id = root.GetId().lstrip('#')
                newElement = CElement(id, root.GetType())
                newElement.SetData(root.GetSaveInfo())
                self.__elements[id] = newElement
                newProjectTreeNode = CProjectTreeNode(newElement)
                if treeParent is None:
                    self.__projectTreeRoot = newProjectTreeNode
                else :
                    treeParent.AppendChildElement(newProjectTreeNode)
                childs = root.GetChilds()
                diagrams = root.GetDiagrams()
                connections = root.GetConnections()
                for e in childs+connections+diagrams:
                    self.__LoadProjectRecursive(e, newProjectTreeNode)
            elif root.GetClass().find('Diagram') != -1:
                #ak je to diagram
                id = root.GetId().lstrip('#')
                newDiagram = CDiagram(id, root.GetType())
                newDiagram.SetData(root.GetSaveInfo())
                newProjectTreeNode = CProjectTreeNode(newDiagram)
                treeParent.AppendChildDiagram(newProjectTreeNode)
                visualElements = root.GetElements()
                for ve in visualElements:
                    # nacitaj vizualne elementy
                    veo = ve.GetObject()
                    newElementView = CElementView(self.GetById(veo.GetId().lstrip('#')), ve.GetPosition(), ve.GetSize())
                    newDiagram.AddElementView(newElementView)
                    
                visualConnections = root.GetConnections()
                for vc in visualConnections:
                    #nacitaj vizualne spojenia
                    vco = vc.GetObject()
                    newConnectionView = CConnectionView(self.GetById(vco.GetId().lstrip('#')))
                    for point in vc.GetPoints()[1:len(vc.GetPoints())-1]:
                        newConnectionView.AddPoint(point)
                    for label in vc.GetAllLabelPositions():
                        newConnectionView.AddLabel(label)
                    newDiagram.AddConnectionView(newConnectionView)
                    
                self.__diagrams[id] = newDiagram
            elif root.GetClass().find('Connection') != -1:
                id = root.GetId().lstrip('#')
                source = root.GetSource()
                dest = root.GetDestination()
                newConnection = CConnection(id, root.GetType(), self.GetById(source.GetId().lstrip('#')), self.GetById(dest.GetId().lstrip('#')))
                newConnection.SetData(root.GetSaveInfo())
                self.__connections[id] = newConnection 
            
           
   
    def __LoadProjectFromXml(self, xmlData):
        '''
        Create all project structure from xml data
        '''
        # need to get plain xml file data
        root = etree.XML(xmlData)
        for element in root:
            if element.tag == UMLPROJECT_NAMESPACE + 'objects':
                #nacitaj objekty
                for subelement in element:
                    if subelement.tag == UMLPROJECT_NAMESPACE + 'object':
                        id = subelement.get('id')
                        type = subelement.get('type')
                        newElement = CElement(id, type)
                        newElement.SetData(CProject.__LoadData(subelement[0]))
                        self.__elements[id] = newElement
            elif element.tag == UMLPROJECT_NAMESPACE + 'connections':
                #nacitaj spojenia
                for connection in element:
                    if connection.tag == UMLPROJECT_NAMESPACE + 'connection':
                        id = connection.get('id')
                        type = connection.get('type')
                        sourceid = connection.get('source')
                        destinationid = connection.get('destination')
                        newConnection = CConnection(id, type, self.GetById(sourceid), self.GetById(destinationid))
                        newConnection.SetData(CProject.__LoadData(connection[0])) 
                        self.__connections[id] = newConnection
            elif element.tag == UMLPROJECT_NAMESPACE + 'diagrams':
                #nacitaj diagramy
                for diagram in element:
                    if diagram.tag == UMLPROJECT_NAMESPACE + 'diagram':
                        id = diagram.get('id')
                        type = diagram.get('type')
                        newDiagram = CDiagram(id, type)
                        newDiagram.SetData(CProject.__LoadData(diagram[0])) 
                        self.__diagrams[id] = newDiagram
            elif element.tag == UMLPROJECT_NAMESPACE + 'projecttree':
                
                #nacitaj strom projektu
                projectTreeRoot = element[0]
                self.__CreateProjectTree(projectTreeRoot, None)
                        
    
    def __CreateProjectTree(self, element, parent):
        if parent is None:
            # ak nemame koren
            if (element.tag == UMLPROJECT_NAMESPACE+'node'):
                id = element.get('id')
                newProjectTreeNode = CProjectTreeNode(self.GetById(id))
                self.__projectTreeRoot = newProjectTreeNode
                for child in self.__GetNodeChilds(element):
                    self.__CreateProjectTree(child, newProjectTreeNode)
        else:
            if (element.tag == UMLPROJECT_NAMESPACE+'node'):
                id = element.get('id')
                newProjectTreeNode = CProjectTreeNode(self.GetById(id))
                parent.AppendChildElement(newProjectTreeNode)
                for child in self.__GetNodeChilds(element):
                    self.__CreateProjectTree(child, newProjectTreeNode)
            elif (element.tag == UMLPROJECT_NAMESPACE+'diagram'):
                id = element.get('id')
                self.__LoadDiagram(element)
                newProjectTreeNode = CProjectTreeNode(self.GetById(id))
                parent.AppendChildDiagram(newProjectTreeNode)
                 
    
    def __GetNodeChilds(self, element):
        result = []
        for childs in element:
            if (childs.tag == UMLPROJECT_NAMESPACE+'childs'):
                for child in childs:
                    if child.tag == UMLPROJECT_NAMESPACE+'node':
                        result.append(child)
            elif (childs.tag == UMLPROJECT_NAMESPACE+'diagrams'):
                for child in childs:
                    if child.tag == UMLPROJECT_NAMESPACE+'diagram':
                        result.append(child)
        return result
    
    @staticmethod
    def __LoadData(element):
        if element.tag == UMLPROJECT_NAMESPACE + 'dict':
            return dict([(item.get('name'), CProject.__LoadData(item)) for item in element])
        elif element.tag == UMLPROJECT_NAMESPACE + 'list':
            return [CProject.__LoadData(item) for item in element]
        elif element.tag == UMLPROJECT_NAMESPACE + 'text':
            return unicode(element.text or '')
    
    def __LoadDiagram(self, element):
        
        id = element.get('id')
        diagram = self.GetById(id)
        for item in element:
            # nacitaj elementy a spojenia z diagramu
            if item.tag == UMLPROJECT_NAMESPACE+ 'element':
            #nacitaj element
                position = (item.get('x'), item.get('y'))
                size = (item.get('dw'), item.get('dh'))
                elId = item.get('id')
                elementView = CElementView(self.GetById(elId), position, size)
                diagram.AddElementView(elementView)
            elif item.tag == UMLPROJECT_NAMESPACE + 'connection':
            #nacitaj spojenie
                conId = item.get('id')
                connectionView = CConnectionView(self.GetById(conId))
                for subitem in item:
                    #nacitaj sprostosti zo spojenia
                    if subitem.tag == UMLPROJECT_NAMESPACE + 'point':
                        point = (subitem.get('x'), subitem.get('y'))
                        connectionView.AddPoint(point)
                    elif subitem.tag == UMLPROJECT_NAMESPACE + 'label':
                        label = dict(zip(subitem.keys(), subitem.values()))
                        label.pop('num')
                        connectionView.AddLabel(label)
                diagram.AddConnectionView(connectionView)
        
    
    
    
    def GetById(self, id):
        return self.__elements.get(id) or self.__connections.get(id) or self.__diagrams.get(id)
    
    def GetProjectTreeRoot(self):
        return self.__projectTreeRoot
    
    def GetElements(self):
        return self.__elements
    
    def GetDiagrams(self):
        return self.__diagrams
    
    def GetConnections(self):
        return self.__connections
    
    def __str__(self):
        return str(self.__diagrams.keys())+str(self.__elements.keys())+str(self.__connections.keys())