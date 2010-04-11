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
from lib.lib import Indent
from ProjectTreeNode import CProjectTreeNode
from Base import CBase


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
        #self.__saveVersion = (1,1,0)
        #self.__metamodelUri = project.GetMetamodel().GetUri()
        #self.__metamodelVersion = project.GetMetamodel().GetVersion()
        
        root = project.GetRoot()
        if root is not None:
            self.__LoadProjectRecursive(root, None)
   
    def __LoadProjectRecursive(self, root, treeParent):
        if root is not None:
            
            if root.GetClass().find('Element') != -1:
                # ak je to element
                
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
                    treeParent.AddChildElement(newProjectTreeNode)
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
                newProjectTreeNode = CProjectTreeNode(newDiagram, treeParent)
                treeParent.AddChildDiagram(newProjectTreeNode)
                visualElements = root.GetElements()
                for ve in visualElements:
                    # nacitaj vizualne elementy
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
                    #nacitaj vizualne spojenia
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
            
            elif element.tag == UMLPROJECT_NAMESPACE + 'counters':
                self.__counters = element
                        
    
    def __CreateProjectTree(self, element, parent):
        if parent is None:
            # ak nemame koren
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
                parent.AddChildElement(newProjectTreeNode)
                for child in self.__GetNodeChilds(element):
                    self.__CreateProjectTree(child, newProjectTreeNode)
            elif (element.tag == UMLPROJECT_NAMESPACE+'diagram'):
                id = element.get('id')
                self.__LoadDiagram(element)
                newProjectTreeNode = CProjectTreeNode(self.GetById(id), parent)
                parent.AddChildDiagram(newProjectTreeNode)
                 
    
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
        if 'default' in element.attrib and element.attrib['default'].lower() in ('1', 'true'):
            self.__defaultDiagram = diagram
        for item in element:
            # nacitaj elementy a spojenia z diagramu
            if item.tag == UMLPROJECT_NAMESPACE+ 'element':
            #nacitaj element
                position = (unicode(item.get('x')), unicode(item.get('y')))
                size = (unicode(item.get('dw')), unicode(item.get('dh')))
                elId = item.get('id')
                elementView = CElementView(self.GetById(elId), diagram ,position, size)
                diagram.AddElementView(elementView)
            elif item.tag == UMLPROJECT_NAMESPACE + 'connection':
            #nacitaj spojenie
                conId = item.get('id')
                connectionView = CConnectionView(self.GetById(conId), diagram)
                for subitem in item:
                    #nacitaj sprostosti zo spojenia
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
        id = id.lstrip('#')
        return self.__elements.get(id) or self.__connections.get(id) or self.__diagrams.get(id)
    
    def DeleteById(self, id):
        print id
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
        return self.__projectTreeRoot
    
    def GetElements(self):
        return self.__elements
    
    def GetDiagrams(self):
        return self.__diagrams
    
    def GetConnections(self):
        return self.__connections
    
    def GetProjectTreeNodes(self, root = None):
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
        return self.__counters
        
    # ----------------------    
    # destructive operations
    # ----------------------
    
    # raise exception on failure
    def AddObject(self, obj):
        if isinstance(obj, CElement):
            # pridaj element
            
            self.__elements[obj.GetId()] = obj
        
        elif isinstance(obj, CConnection):
            # pridaj spojenie
            # najdi zdroj a ciel v aktualnom projekte, lebo nemusia to byt tie iste objekty
            source = self.GetById(obj.GetSource().GetId())
            if source is None:
                raise Exception('Source not found')
            dest = self.GetById(obj.GetDestination().GetId())
            if dest is None:
                raise Exception('Destination not found')
            # vytvor novy connection
            con = CConnection(obj.GetId(), obj.GetType(), source, dest)
            # skopiruj mu data
            con.SetData(obj.GetData())
            self.__connections[con.GetId()] = con
            
        elif isinstance(obj, CDiagram):
            # pridaj diagram
            # vytvor ho
            diag = CDiagram(obj.GetId(), obj.GetType())
            diag.SetData(obj.GetData())
            self.__diagrams[diag.GetId()] = diag
        
    def AddProjectTreeNode(self, treeNode):
        # dostan objekt (ten by mal byt aj tak novy)
        obj = self.GetById(treeNode.GetId())
        if obj is None:
            raise Exception('Project tree node object not found')
        # zisti rodica
        parent = self.GetProjectTreeNodeById(treeNode.GetParent().GetId())
        
        if parent is None:
#            parent = self.AddProjectTreeNode(treeNode.GetParent())
            raise Exception ('Project tree node parent not found')
        
        if self.GetProjectTreeNodeById(obj.GetId()) is None:
        
        
            # vytvor novy node
            newProjectTreeNode = CProjectTreeNode(obj, parent)
            
            if isinstance(obj, CDiagram):
                # ak je to diagram, pridaj diagram
                parent.AddChildDiagram(newProjectTreeNode, treeNode.GetIndex())
                
            elif isinstance(obj, CElement):
                # ak je to element, pridaj element
                parent.AddChildElement(newProjectTreeNode, treeNode.GetIndex())
            
            return newProjectTreeNode
        
    def AddView(self, view):
        
        # najdi objekt, ktoremu to patri
        obj = self.GetById(view.GetObject().GetId())
        if obj is None:
            raise Exception ('View object not found')
        # najdi diagram, do ktoreh sa ma pridat
        diagram = self.GetById(view.GetParentDiagram().GetId())
        if diagram is None:
            raise Exception ('Diagram for view not found')
        
        if isinstance(obj, CElement):
            # ak je to element
            # vytvor novy element view
            newView = CElementView(obj, diagram, view.GetPosition(), view.GetSize())
            # pridaj ho do diagramu
            diagram.AddElementView(newView, view.GetIndex())
        elif isinstance(obj, CConnection):
            # ak je to spojenie
            
            # vytvor novy connection view
            newView = CConnectionView(obj, diagram)
            # skopiruj body
            for point in view.GetPoints():
                newView.AddPoint(point)
                
            # skopiruj labels
            for label in view.GetLabels():
                newView.AddLabel(label)
            # pridaj do diagramu
            diagram.AddConnectionView(newView, view.GetIndex())
    
    def DeleteObject(self, obj):
        if isinstance(obj, CElement):
            # najdi element v projektovom strome
            node = self.GetProjectTreeNodeById(obj.GetId())
            if node is not None:
                self.DeleteProjectTreeNode(node)
        
        elif isinstance(obj, CConnection):
            # odober spojenie, vyhod ho zo zoznamu spojeni
            self.DeleteById(obj.GetId())
            # vymaz spojenie view zo vsetkych diagramov
            for d in self.__diagrams.values():
                
                d.DeleteViewById(obj.GetId())
                
        elif isinstance(obj, CDiagram):
            # najdi diagram v projektovom strome
            node = self.GetProjectTreeNodeById(obj.GetId())
            if node is not None:
                self.DeleteProjectTreeNode(node)
    
    def DeleteProjectTreeNode(self, treeNode):
        # najdi ho v projektovom strome
        node = self.GetProjectTreeNodeById(treeNode.GetId())
        # ak to nie je koren
        if node is not self.__projectTreeRoot:
            # najdi parenta
            if node is not None:
                parent = node.GetParent()
                
                # vymaz vsetkych potomkov
                childs = parent.DeleteChild(node)
                # vymaz vsetky objekty predstavujuce potomkov 
                for ch in childs:
                    self.DeleteById(ch.GetId())
                    # vymaz objekt zo vsetkych diagramov
                    for d in self.__diagrams.values():
                        # vymaz ho zo vsetkych diagramov
                        d.DeleteViewById(ch.GetId())
            
    
    def DeleteView(self, view):
        # najdi diagram, do ktoreho patri
        diagram = self.GetById(view.GetParentDiagram().GetId())
        # vymaz ho z daneho diagramu
        if diagram is not None:
            diagram.DeleteViewById(view.GetObject().GetId())


    def MoveProjectTreeNode(self, node, oldParent, newParent):
        # najdi node
        node = self.GetProjectTreeNodeById(node.GetId())
        if node is None:
            raise Exception ('Project tree node not found')
        
        # najdi stareho rodica
        oldParent = self.GetProjectTreeNodeById(oldParent.GetId())
        if oldParent is None:
            raise Exception ('Old parent not found')
        # najdi noveho rodica
        newParent = self.GetProjectTreeNodeById(newParent.GetId())
        if newParent is None:
            raise Exception ('New parent not found')
        
        if isinstance(node.GetObject(), CDiagram):
            # ak je to diagram
            newParent.AddChildDiagram(node)
        elif isinstance(node.GetObject(), CElement):
            # ak je to element
            newParent.AddChildElement(node)
        
        # vymaz ho zo stareho rodica
        oldParent.DeleteChild(node)

    def ChangeOrderTreeNode(self, node, oldOrder, newOrder):
        print 'CHANGE ORDER', node, oldOrder, newOrder
        node = self.GetProjectTreeNodeById(node.GetId())
        parent = node.GetParent()
        parent.ChangeOrderNode(node, newOrder)
    
    
    def ChangeOrderView(self, view, oldOrder, newOrder):
        print 'CHANGE ORDER', view, oldOrder, newOrder
        diagram = self.GetById(view.GetParentDiagram().GetId())
        view = diagram.GetViewById(view.GetObject().GetId())
        diagram.ChangeOrderView(view, newOrder)


    def ModifyObjectData(self, element, oldState, newState, path):
        el = self.GetById(element.GetId())
        el.ModifyData(oldState, newState, path)

    def ModifyViewData(self, view, oldState, newState, path):
        diagram = self.GetById(view.GetParentDiagram().GetId())
        view = diagram.GetViewById(view.GetObject().GetId())
        view.ModifyData(oldState, newState, path)

    # updatni pocitadla,  vyber vyssie z nich
    def UpdateCounters(self, newCounters):
        for (old,new) in zip(self.__counters, newCounters):
            if old.get('value') < new.get('value'):
                old.set('value', new.get('value'))


    def GetSaveXml(self):
        #assert self.__metamodel is not None
        
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
                #raise ProjectError("unknown data format")
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
        
#        for type in self.GetMetamodel().GetElementFactory().IterTypes():
#            counterNode.append(etree.Element(UMLPROJECT_NAMESPACE+'count', id = type.GetId(), value = unicode(type.GetCounter())))
#        for type in self.GetMetamodel().GetDiagramFactory():
#            counterNode.append(etree.Element(UMLPROJECT_NAMESPACE+'count', id = type.GetId(), value = unicode(type.GetCounter())))
#        
        rootNode.append(counterNode)
        

        #make human-friendly tree
        Indent(rootNode)
        
        return '<?xml version="1.0" encoding="utf-8"?>\n'+etree.tostring(rootNode, encoding='utf-8')
    
    


            
    def __str__(self):
        return str(self.__diagrams.keys())+str(self.__elements.keys())+str(self.__connections.keys())