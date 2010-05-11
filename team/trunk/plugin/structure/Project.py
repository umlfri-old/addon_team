'''
Created on 6.3.2010

@author: Peterko
'''
from Diagram import CDiagram
from Element import CElement
from Connection import CConnection
from ElementView import CElementView
from ConnectionView import CConnectionView
from imports.etree import etree

from imports.Indent import Indent
from ProjectTreeNode import CProjectTreeNode
from Base import CBase

UMLPROJECT_NAMESPACE = '{http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd}'


class CProject(object):
    '''
    Class representing UML .FRI project
    '''


    def __init__(self, project=None,xmlData=None):
        '''
        Constructor
        @type project: IProject
        @param project: Project from plugin system from which our project can be created
        @type xmlData: string
        @param xmlData: Xml data from which our project can be constructed
        '''
        self.__diagrams = {}
        self.__elements = {}
        self.__connections = {}
        self.__projectTreeRoot = None
        self.__saveVersion = None
        self.__metamodelUri = None
        self.__metamodelVersion = None
        self.__defaultDiagram = None 
        self.__counters = None
        if (xmlData is not None):
            self.__LoadProjectFromXml(xmlData)
        if (project is not None):
            self.__LoadProjectFromApp(project)
    
    def __LoadProjectFromApp(self, project):
        '''
        Loads project from application IProject
        @type project: IProject
        @param project: Project from plugin system
        '''
        
        
        root = project.GetRoot()
        if root is not None:
            self.__LoadProjectRecursive(root, None)
   
    def __LoadProjectRecursive(self, root, treeParent):
        '''
        Loads project from application project recursivly from root
        @type root: IElementObject
        @param root: root element
        @type treeParent: IElementObject
        @param treeParent: parent of root element
        
        '''
        if root is not None:
            
            if root.GetClass().find('Element') != -1:
                
                
                id = root.GetId().lstrip('#')
                if self.GetById(id) is None:
                    newElement = CElement(id, root.GetType())
                    newElement.SetData(root.GetSaveInfo())
                    self.__elements[id] = newElement
                else:
                    newElement = self.GetById(id)
                newProjectTreeNode = CProjectTreeNode(newElement, treeParent)
                if treeParent is None:
                    self.__projectTreeRoot = newProjectTreeNode
                else :
                    treeParent.AddChild(newProjectTreeNode)
                childs = root.GetChilds()
                diagrams = root.GetDiagrams()
                connections = root.GetConnections()
                
                for e in childs+connections+diagrams:
                    
                    self.__LoadProjectRecursive(e, newProjectTreeNode)
            elif root.GetClass().find('Diagram') != -1:
                
                id = root.GetId().lstrip('#')
                newDiagram = CDiagram(id, root.GetType())
                newDiagram.SetData(root.GetSaveInfo())
                newProjectTreeNode = CProjectTreeNode(newDiagram, treeParent)
                treeParent.AddChild(newProjectTreeNode)
                visualElements = root.GetElements()
                for ve in visualElements:
                    
                    veo = ve.GetObject()
                    size = (unicode(ve.GetSize()[0] - ve.GetMinimalSize()[0]), unicode(ve.GetSize()[1] - ve.GetMinimalSize()[1]))
                    
                    elementViewObject = self.GetById(veo.GetId().lstrip('#'))
                    if elementViewObject is None:
                        evoId = veo.GetId().lstrip('#')
                        elementViewObject = CElement(evoId, veo.GetType())
                        elementViewObject.SetData(veo.GetSaveInfo())
                        self.__elements[evoId] = elementViewObject
                    newElementView = CElementView(elementViewObject, newDiagram, (unicode(ve.GetPosition()[0]), unicode(ve.GetPosition()[1])), size)
                    newDiagram.AddElementView(newElementView)
                    
                visualConnections = root.GetConnections()
                for vc in visualConnections:
                    
                    vco = vc.GetObject()
                    connectionViewObject = self.GetById(vco.GetId().lstrip('#'))
                    if connectionViewObject is None:
                        cvoId = vco.GetId().lstrip('#')
                        connectionViewObject = CConnection(cvoId, vco.GetType(), self.GetById(vco.GetSource().GetId().lstrip('#')), self.GetById(vco.GetDestination().GetId().lstrip('#')))
                        connectionViewObject.SetData(vco.GetSaveInfo())
                        self.__connections[cvoId] = connectionViewObject
                    newConnectionView = CConnectionView(connectionViewObject, newDiagram)
                    for point in vc.GetPoints()[1:len(vc.GetPoints())-1]:
                        newConnectionView.AddPoint((unicode(point[0]), unicode(point[1])))
                    for label in vc.GetAllLabelPositions():
                        
                        newConnectionView.AddLabel(label)
                    newDiagram.AddConnectionView(newConnectionView)
                    
                self.__diagrams[id] = newDiagram
            elif root.GetClass().find('Connection') != -1:
                id = root.GetId().lstrip('#')
                if self.GetById(id) is None:
                    source = root.GetSource()
                    
                    dest = root.GetDestination()
                    
                    mySource = self.GetById(source.GetId().lstrip('#'))
                    
                    if mySource is None:
                        sourceId = source.GetId().lstrip('#')
                        mySource = CElement(sourceId, source.GetType())
                        mySource.SetData(source.GetSaveInfo())
                        
                        self.__elements[sourceId] = mySource
                    myDest = self.GetById(dest.GetId().lstrip('#'))
                    
                    if myDest is None:
                        destId = dest.GetId().lstrip('#')
                        myDest = CElement(destId, dest.GetType())
                        myDest.SetData(dest.GetSaveInfo())
                        
                        self.__elements[destId] = myDest
                    newConnection = CConnection(id, root.GetType(), mySource, myDest)
                    newConnection.SetData(root.GetSaveInfo())
                    self.__connections[id] = newConnection 
            
           
   
    def __LoadProjectFromXml(self, xmlData):
        '''
        Create all project structure from xml data
        @type xmlData: string
        @param xmlData: xml data 
        '''
        # need to get plain xml file data
        root = etree.XML(xmlData)
        self.__saveVersion = tuple(int(i) for i in root.get('saveversion').split('.'))
        for element in root:
            if element.tag == UMLPROJECT_NAMESPACE+'metamodel':
                uri = None
                version = None
                
                for item in element:
                    if item.tag == UMLPROJECT_NAMESPACE+'uri':
                        uri = item.text
                    elif item.tag == UMLPROJECT_NAMESPACE+'version':
                        version = item.text
                self.__metamodelUri = uri
                self.__metamodelVersion = version
            if element.tag == UMLPROJECT_NAMESPACE + 'objects':
                
                for subelement in element:
                    if subelement.tag == UMLPROJECT_NAMESPACE + 'object':
                        id = subelement.get('id')
                        type = subelement.get('type')
                        newElement = CElement(id, type)
                        newElement.SetData(CProject.__LoadData(subelement[0]))
                        self.__elements[id] = newElement
            elif element.tag == UMLPROJECT_NAMESPACE + 'connections':
                
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
                
                for diagram in element:
                    if diagram.tag == UMLPROJECT_NAMESPACE + 'diagram':
                        id = diagram.get('id')
                        type = diagram.get('type')
                        newDiagram = CDiagram(id, type)
                        newDiagram.SetData(CProject.__LoadData(diagram[0])) 
                        self.__diagrams[id] = newDiagram
            elif element.tag == UMLPROJECT_NAMESPACE + 'projecttree':
                
                
                projectTreeRoot = element[0]
                self.__CreateProjectTree(projectTreeRoot, None)
            
            elif element.tag == UMLPROJECT_NAMESPACE + 'counters':
                self.__counters = element
                        
    
    def __CreateProjectTree(self, element, parent):
        '''
        Creates project tree recurisvely
        @type element: Element
        @param element: root element
        @type parent: CProjectTreeNode
        @param parent: parent of element
        '''
        if parent is None:
            
            if (element.tag == UMLPROJECT_NAMESPACE+'node'):
                id = element.get('id')
                newProjectTreeNode = CProjectTreeNode(self.GetById(id), parent)
                self.__projectTreeRoot = newProjectTreeNode
                for child in self.__GetNodeChilds(element):
                    self.__CreateProjectTree(child, newProjectTreeNode)
        else:
            if (element.tag == UMLPROJECT_NAMESPACE+'node'):
                id = element.get('id')
                newProjectTreeNode = CProjectTreeNode(self.GetById(id), parent)
                parent.AddChild(newProjectTreeNode)
                for child in self.__GetNodeChilds(element):
                    self.__CreateProjectTree(child, newProjectTreeNode)
            elif (element.tag == UMLPROJECT_NAMESPACE+'diagram'):
                id = element.get('id')
                self.__LoadDiagram(element)
                newProjectTreeNode = CProjectTreeNode(self.GetById(id), parent)
                parent.AddChild(newProjectTreeNode)
                 
    
    def __GetNodeChilds(self, element):
        '''
        Get childs of element when creating project from xml data
        @type element: Element
        @param element: element for getting childs
        '''
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
        '''
        Loads data of element to meaningful structure
        @type element: Element
        @param element: element
        @rtype: dic
        @return: Returns all data of element in dictionary
        '''
        if element.tag == UMLPROJECT_NAMESPACE + 'dict':
            return dict([(item.get('name'), CProject.__LoadData(item)) for item in element])
        elif element.tag == UMLPROJECT_NAMESPACE + 'list':
            return [CProject.__LoadData(item) for item in element]
        elif element.tag == UMLPROJECT_NAMESPACE + 'text':
            return unicode(element.text or '')
    
    def __LoadDiagram(self, element):
        '''
        Loads diagram when creating project from xml data
        @type element: Element
        @param element: element representing diagram
        '''
        id = element.get('id')
        diagram = self.GetById(id)
        if 'default' in element.attrib and element.attrib['default'].lower() in ('1', 'true'):
            self.__defaultDiagram = diagram
        for item in element:
            
            if item.tag == UMLPROJECT_NAMESPACE+ 'element':
            
                position = (unicode(item.get('x')), unicode(item.get('y')))
                size = (unicode(item.get('dw')), unicode(item.get('dh')))
                elId = item.get('id')
                elementView = CElementView(self.GetById(elId), diagram ,position, size)
                diagram.AddElementView(elementView)
            elif item.tag == UMLPROJECT_NAMESPACE + 'connection':
            
                conId = item.get('id')
                connectionView = CConnectionView(self.GetById(conId), diagram)
                for subitem in item:
                    
                    if subitem.tag == UMLPROJECT_NAMESPACE + 'point':
                        point = (unicode(subitem.get('x')), unicode(subitem.get('y')))
                        connectionView.AddPoint(point)
                    elif subitem.tag == UMLPROJECT_NAMESPACE + 'label':
                        label = dict(zip(subitem.keys(), [unicode(value) for value in subitem.values()]))
                        label.pop('num')
                        label['idx'] = unicode(label['idx'])
                        
                        connectionView.AddLabel(label)
                diagram.AddConnectionView(connectionView)
        
    
    
    
    def GetById(self, id):
        '''
        Returns data object by id
        @type id: string
        @param id: id of object
        @rtype: CBase
        @return: data object
        '''
        id = id.lstrip('#')
        return self.__elements.get(id) or self.__connections.get(id) or self.__diagrams.get(id)
    
    def DeleteById(self, id):
        '''
        Deletes data object by id
        @type id: string
        @param id: id of object
        '''
        id = id.lstrip('#')
        try:
            self.__elements.pop(id)
        except:
            pass
        try:
            self.__connections.pop(id)
        except: 
            pass
        try:
            self.__diagrams.pop(id)
        except:
            pass
        
    
    def GetProjectTreeRoot(self):
        '''
        Returns project tree root
        @rtype: CProjectTreeNode
        @return: project tree root
        '''
        return self.__projectTreeRoot
    
    def GetElements(self):
        '''
        Returns all elements
        @rtype: list
        @return: list of all elements
        '''
        return self.__elements
    
    def GetDiagrams(self):
        '''
        Returns all diagrams
        @rtype: list
        @return: list of all diagrams
        '''
        return self.__diagrams
    
    def GetConnections(self):
        '''
        Returns all connections
        @rtype: list
        @return: list of all connections
        '''
        return self.__connections
    
    def GetProjectTreeNodes(self, root = None):
        '''
        Returns all project tree nodes under given root in list
        @type root: CProjectTreeNode
        @param root: root of project tree nodes
        @rtype: list
        @return: list of all project tree nodes under given root
        '''
        if root is None:
            root = self.__projectTreeRoot
        stack = [root]
        result = []
        while len(stack) > 0:
            stack.extend(root.GetChildsOrdered())
            root = stack.pop()
            result.append(root)
        return result
    
    def GetProjectTreeNodeById(self, id, root = None):
        '''
        Returns project tree node by its id, search under given root
        @type id: string
        @param id: id of project tree node
        @type root: CProjectTreeNode
        @param root: root under which will be searched
        @rtype: CProjectTreeNode
        @return: project tree node by its id
        '''
        if root is None:
            root = self.__projectTreeRoot
        stack = [root]
        while not(root.GetId() == id or len(stack) == 0):
            stack.extend(root.GetChildsOrdered())
            root = stack.pop()
        if root.GetId() == id:
            return root
        else:
            return None
        
        
    def GetCounters(self):
        '''
        Returns project counters
        @rtype: Element
        @return: project counters
        '''
        return self.__counters
        
    # ----------------------    
    # destructive operations
    # ----------------------
    
    # raise exception on failure
    def AddObject(self, obj):
        '''
        Adds object to project
        @type obj: CBase
        @param obj: Object to be added
        @raise Exception: on failure
        '''
        if isinstance(obj, CElement):
            
            
            self.__elements[obj.GetId()] = obj
        
        elif isinstance(obj, CConnection):
            
            source = self.GetById(obj.GetSource().GetId())
            if source is None:
                raise Exception('Source not found')
            dest = self.GetById(obj.GetDestination().GetId())
            if dest is None:
                raise Exception('Destination not found')
            
            con = CConnection(obj.GetId(), obj.GetType(), source, dest)
            
            con.SetData(obj.GetData())
            self.__connections[con.GetId()] = con
            
        elif isinstance(obj, CDiagram):
            
            diag = CDiagram(obj.GetId(), obj.GetType())
            diag.SetData(obj.GetData())
            self.__diagrams[diag.GetId()] = diag
        
    def AddProjectTreeNode(self, treeNode):
        '''
        Adds object tree node to project
        @type obj: CProjectTreeNode
        @param obj: Project tree node to be added
        @raise Exception: on failure
        @rtype: CProjectTreeNode
        @return: added project tree node
        '''
        
        obj = self.GetById(treeNode.GetId())
        if obj is None:
            raise Exception('Project tree node object not found')
        
        parent = self.GetProjectTreeNodeById(treeNode.GetParent().GetId())
        
        if parent is None:

            raise Exception ('Project tree node parent not found')
        
        if self.GetProjectTreeNodeById(obj.GetId()) is None:
        
        

            
            newProjectTreeNode = CProjectTreeNode(obj, parent)
            parent.AddChild(newProjectTreeNode, treeNode.GetIndex())
            
            
            
            return newProjectTreeNode
        
    def AddView(self, view):
        '''
        Adds view to project
        @type obj: CBaseView
        @param obj: View to be added
        @raise Exception: on failure
        '''
        
        obj = self.GetById(view.GetObject().GetId())
        if obj is None:
            raise Exception ('View object not found')
        
        diagram = self.GetById(view.GetParentDiagram().GetId())
        if diagram is None:
            raise Exception ('Diagram for view not found')
        
        if isinstance(obj, CElement):
            newView = CElementView(obj, diagram, view.GetPosition(), view.GetSize())
        
            diagram.AddElementView(newView, view.GetIndex())
        elif isinstance(obj, CConnection):
            newView = CConnectionView(obj, diagram)
        
            for point in view.GetPoints():
                newView.AddPoint(point)
                
            
            for label in view.GetLabels():
                newView.AddLabel(label)
            
            diagram.AddConnectionView(newView, view.GetIndex())
    
    def DeleteObject(self, obj):
        '''
        Deletes given object from project
        @type obj: CBase
        @param obj: Object to be deleted
        '''
        if isinstance(obj, CElement):
            
            node = self.GetProjectTreeNodeById(obj.GetId())
            if node is not None:
                self.DeleteProjectTreeNode(node)
        
        elif isinstance(obj, CConnection):
            
            self.DeleteById(obj.GetId())
            
            for d in self.__diagrams.values():
                
                d.DeleteViewById(obj.GetId())
                
        elif isinstance(obj, CDiagram):
            
            node = self.GetProjectTreeNodeById(obj.GetId())
            if node is not None:
                self.DeleteProjectTreeNode(node)
    
    def DeleteProjectTreeNode(self, treeNode):
        '''
        Deletes given project tree node from project
        @type treeNode: CProjectTreeNode
        @param treeNode: project tree node to be deleted
        '''
        
        node = self.GetProjectTreeNodeById(treeNode.GetId())
        
        if node is not self.__projectTreeRoot:
            
            if node is not None:
                parent = node.GetParent()
                
                
                childs = parent.DeleteChild(node)
                 
                for ch in childs:
                    self.DeleteById(ch.GetId())
                    
                    for d in self.__diagrams.values():
                        
                        d.DeleteViewById(ch.GetId())
            
    
    def DeleteView(self, view):
        '''
        Deletes given view from project
        @type treeNode: CBaseView
        @param treeNode: view to be deleted
        '''
        
        diagram = self.GetById(view.GetParentDiagram().GetId())
        
        if diagram is not None:
            diagram.DeleteViewById(view.GetObject().GetId())


    def MoveProjectTreeNode(self, node, oldParent, newParent):
        '''
        Move project tree node from old parent to new parent
        @type node: CProjectTreeNode
        @param node: node to be moved
        @type oldParent: CProjectTreeNode
        @param oldParent: old parent of given node
        @type newParent: CProjectTreeNode
        @param newParent: new parent of given node
        @raise Exception: on failure
        '''
        
        node = self.GetProjectTreeNodeById(node.GetId())
        if node is None:
            raise Exception ('Project tree node not found')
        
        
        oldParent = self.GetProjectTreeNodeById(oldParent.GetId())
        if oldParent is None:
            raise Exception ('Old parent not found')
        
        newParent = self.GetProjectTreeNodeById(newParent.GetId())
        if newParent is None:
            raise Exception ('New parent not found')
        
        if newParent.GetChild(node.GetId()) is None:
            
            newParent.AddChild(node)
            
            
            
            oldParent.DeleteChild(node)

    def ChangeOrderTreeNode(self, node, oldOrder, newOrder):
        '''
        Change order of node under its parent
        @type node: CProjectTreeNode
        @param node: node to be modified
        @type oldOrder: int
        @param oldOrder: old order of node
        @type newOrder: int
        @param newOrder: new order of node
        '''
        node = self.GetProjectTreeNodeById(node.GetId())
        parent = node.GetParent()
        parent.ChangeOrderNode(node, newOrder)
    
    
    def ChangeOrderView(self, view, oldOrder, newOrder):
        '''
        Change order of view under its diagram
        @type view: CBaseView
        @param view: view to be modified
        @type oldOrder: int
        @param oldOrder: old order of view
        @type newOrder: int
        @param newOrder: new order of view
        '''
        diagram = self.GetById(view.GetParentDiagram().GetId())
        view = diagram.GetViewById(view.GetObject().GetId())
        diagram.ChangeOrderView(view, newOrder)


    def ModifyObjectData(self, element, oldState, newState, path):
        '''
        Modifies data of given object
        @type element: CBase
        @param element: Element to be modified
        @type oldState: list or dict
        @param oldState: old state of data
        @type newState: list or dict
        @param newState: new state of data
        @type path: list
        @param path: path to given change
        '''
        el = self.GetById(element.GetId())
        el.ModifyData(oldState, newState, path)

    def ModifyViewData(self, view, oldState, newState, path):
        '''
        Modifies data of given view
        @type view: CBaseView
        @param view: View to be modified
        @type oldState: list or dict
        @param oldState: old state of data
        @type newState: list or dict
        @param newState: new state of data
        @type path: list
        @param path: path to given change
        '''
        diagram = self.GetById(view.GetParentDiagram().GetId())
        view = diagram.GetViewById(view.GetObject().GetId())
        view.ModifyData(oldState, newState, path)

    
    def UpdateCounters(self, newCounters):
        '''
        Updates counters, choose higher from self counters and new counters
        @type newCounters: Element
        @param newCounters: new counters
        '''
        for (old,new) in zip(self.__counters, newCounters):
            if int(old.get('value')) < int(new.get('value')):
                old.set('value', new.get('value'))


    def GetSaveXml(self):
        '''
        Generates xml representation of project
        @rtype: string
        @return: xml representation of project
        '''
        
        
        def SaveDomainObjectInfo(data, name=None):
            if isinstance(data, dict):
                element = etree.Element(UMLPROJECT_NAMESPACE+'dict')
                d = list(data.iteritems())
                d.sort()
                for key, value in d:
                    element.append(SaveDomainObjectInfo(value, key))
            elif isinstance(data, list):
                element = etree.Element(UMLPROJECT_NAMESPACE+'list')
                for value in data:
                    element.append(SaveDomainObjectInfo(value))
            elif isinstance(data, (str, unicode)):
                element = etree.Element(UMLPROJECT_NAMESPACE+'text')
                element.text = data
            else:
                pass
                
            if name:
                element.set('name', name)
            return element
        
        def savetree(node, element):
            nodeNode = etree.Element(UMLPROJECT_NAMESPACE+'node', id=unicode(node.GetId()))
            if len(node.GetChildNodes())>0:
                childsNode = etree.Element(UMLPROJECT_NAMESPACE+'childs')
                for chld in node.GetChildNodes():
                    savetree(chld, childsNode)
                nodeNode.append(childsNode)
                
            diagramsNode = etree.Element(UMLPROJECT_NAMESPACE+'diagrams')
            if len(node.GetChildDiagrams())>0:
                for area in node.GetChildDiagrams():
                    diagramNode = etree.Element(UMLPROJECT_NAMESPACE+'diagram', id=unicode(area.GetId()))
                    if area is self.__defaultDiagram:
                        diagramNode.attrib['default'] = 'true'
                    for e in area.GetObject().GetElementViews():
                        pos = e.GetPosition()
                        size = e.GetSizeRelative()
                        elementNode = etree.Element(UMLPROJECT_NAMESPACE+'element', id=unicode(e.GetObject().GetId()), x=unicode(pos['x']), y=unicode(pos['y']), dw=unicode(size['dw']), dh=unicode(size['dh']))
                        diagramNode.append(elementNode)
                        
                    for c in area.GetObject().GetConnectionViews():
                        connectionNode = etree.Element(UMLPROJECT_NAMESPACE+'connection', id=unicode(c.GetObject().GetId()))
                        print c.GetPoints()
                        for pos in c.GetPoints():
                            print pos
                            pointNode = etree.Element(UMLPROJECT_NAMESPACE+'point', x=unicode(pos['x']), y=unicode(pos['y']))
                            connectionNode.append(pointNode)
                            
                        for num, info in enumerate(c.GetLabels()):
                            connectionNode.append(etree.Element(UMLPROJECT_NAMESPACE+'label', 
                                dict(map(lambda x: (x[0], unicode(x[1])), info.iteritems())), #transform {key:value, ...} -> {key:unicode(value), ...}
                                num=unicode(num)))
                                
                        diagramNode.append(connectionNode)
                    diagramsNode.append(diagramNode)
            nodeNode.append(diagramsNode)
            element.append(nodeNode)
        
        elements, connections, diagrams = self.__elements.values(), self.__connections.values(), self.__diagrams.values()
        
        rootNode = etree.XML('<umlproject saveversion="%s" xmlns="http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd"></umlproject>'%('.'.join(str(i) for i in self.__saveVersion)))
        
        metamodelNode = etree.Element(UMLPROJECT_NAMESPACE+'metamodel')
        objectsNode = etree.Element(UMLPROJECT_NAMESPACE+'objects')
        connectionsNode = etree.Element(UMLPROJECT_NAMESPACE+'connections')
        diagramsNode = etree.Element(UMLPROJECT_NAMESPACE+'diagrams')
        projtreeNode = etree.Element(UMLPROJECT_NAMESPACE+'projecttree')
        counterNode = self.__counters
        
        # metamodel informations
        metamodelUriNode = etree.Element(UMLPROJECT_NAMESPACE+'uri')
        metamodelUriNode.text = self.__metamodelUri
        metamodelVersionNode = etree.Element(UMLPROJECT_NAMESPACE+'version')
        metamodelVersionNode.text = self.__metamodelVersion
        
        metamodelNode.append(metamodelUriNode)
        metamodelNode.append(metamodelVersionNode)
        rootNode.append(metamodelNode)
        
        elements = list(elements)
        
        elements.sort(key = CBase.GetId)
        
        for obj in elements:
            objectNode = etree.Element(UMLPROJECT_NAMESPACE+'object', type=unicode(obj.GetType()), id=unicode(obj.GetId()))
            objectNode.append(SaveDomainObjectInfo(obj.GetSaveData()))
            objectsNode.append(objectNode)
            
        rootNode.append(objectsNode)
        
        connections = list(connections)
        connections.sort(key = CBase.GetId)
        for connection in connections:
            connectionNode = etree.Element(UMLPROJECT_NAMESPACE+'connection', type=unicode(connection.GetType()), id=unicode(connection.GetId()), source=unicode(connection.GetSource().GetId()), destination=unicode(connection.GetDestination().GetId()))
            connectionNode.append(SaveDomainObjectInfo(connection.GetSaveData()))
            connectionsNode.append(connectionNode)
        
        rootNode.append(connectionsNode)
        
        diagrams = list(diagrams)
        diagrams.sort(key = CBase.GetId)
        for diagram in diagrams:
            diagramNode = etree.Element(UMLPROJECT_NAMESPACE + 'diagram', id=unicode(diagram.GetId()), type=unicode(diagram.GetType()))
            diagramNode.append(SaveDomainObjectInfo(diagram.GetSaveData()))
            diagramsNode.append(diagramNode)
            
        rootNode.append(diagramsNode)
        
        savetree(self.__projectTreeRoot, projtreeNode)
        rootNode.append(projtreeNode)
        

        rootNode.append(counterNode)
        

        #make human-friendly tree
        Indent(rootNode)
        
        return '<?xml version="1.0" encoding="utf-8"?>\n'+etree.tostring(rootNode, encoding='utf-8')
    
    


            
    def __str__(self):
        return str(self.__diagrams.keys())+str(self.__elements.keys())+str(self.__connections.keys())