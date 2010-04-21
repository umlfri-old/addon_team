'''
Created on 12.4.2010

@author: Peterko
'''
from structure import *
from ElementDrawing import CElementDrawing
from ConnectionDrawing import CConnectionDrawing

class CDiagramDrawing(object):
    '''
    classdocs
    '''
    
    

    def __init__(self, diagram):
        '''
        Constructor
        '''
        
        self.__diagram = diagram
        self.size = [0,0]
        self.__paintedElements = {}
        self.__paintedConnections = {}
        self.__context = None
        
    def Paint(self, context):
        if self.__diagram is not None:
            for view in self.__diagram.GetViews().values():
                self.__context = context
                self.__PaintView(context, view, 128, 128, 128, 0.2)
                

    def GetViewAtPoint(self, point):
        return self.GetConnectionAtPoint(point) or self.GetElementAtPoint(point)

    def GetSelectionOfView(self, view):
        return self.GetPathOfConnection(view) or self.GetPathOfElement(view)
        
    
    def GetElementAtPoint(self, point):
        result = None
        if self.__context is not None:
            for el, path in self.__paintedElements.items():
                self.__context.new_path()
                self.__context.append_path(path)
                if self.__context.in_fill(point[0], point[1]):
                    result = el
                
        return result
    
    def GetPathOfElement(self, el):
        return self.__paintedElements.get(el, None)
    
    def GetConnectionAtPoint(self, point):
        result = None
        if self.__context is not None:
            for con, path in self.__paintedConnections.items():
                self.__context.new_path()
                self.__context.append_path(path)
                if self.__context.in_stroke(point[0], point[1]):
                    result = con
        return result
    
    def GetPathOfConnection(self, con):
        return self.__paintedConnections.get(con, None)
    
    def __PaintView(self, context, view, r, g, b, a=None):
        if isinstance(view, CElementView):
            path = self.__PaintElement(context, view, r, g, b, a)
            self.__paintedElements[view] = path
        elif isinstance(view, CConnectionView):
            path = self.__PaintConnection(context, view, r, g, b, a)
            self.__paintedConnections[view] = path
                    
    
    def __PaintConnection(self, context, connection, r, g, b, a = None):
        
        cd = CConnectionDrawing(connection, context)
        cd.ChangeColor(context, r, g, b, a)
        return cd.Paint()        
        
        
        
    def __PaintElement(self, context, element, r, g, b, a = None):
      
        ed = CElementDrawing(element, context)
        ed.ChangeColor(context, r, g, b, a)
        return ed.Paint()        
          
        
    def GetSize(self):
        if self.__context is not None:
            self.__context.new_path()
            for path in self.__paintedElements.values() + self.__paintedConnections.values():
                self.__context.append_path(path)
            ext = self.__context.fill_extents()
            return (ext[2],ext[3])
        else:
            return (0,0)
    