'''
Created on 12.4.2010

@author: Peterko
'''
from structure import *
from ElementDrawing import CElementDrawing
from ConnectionDrawing import CConnectionDrawing

class CDiagramDrawing(object):
    '''
    Class representing drawing of diagram
    '''
    
    

    def __init__(self, diagram):
        '''
        Constructor
        @type diagram: CDiagram
        @param diagram: underlying diagram object
        '''
        
        self.__diagram = diagram
        self.size = [0,0]
        self.__paintedElements = {}
        self.__paintedConnections = {}
        self.__context = None
        
    def Paint(self, context):
        '''
        Paints diagram on given context
        @type context: CairoContext
        @param context: will be painted on this context
        '''
        if self.__diagram is not None:
            for view in self.__diagram.GetViews().values():
                self.__context = context
                self.__PaintView(context, view, 128, 128, 128, 0.2)
                

    def GetViewAtPoint(self, point):
        '''
        Returns view at given point
        @type point: tuple
        @param point: point coordinates (x, y)
        @rtype: CBaseView
        @return: view at given point or None
        '''
        return self.GetConnectionAtPoint(point) or self.GetElementAtPoint(point)

    def GetSelectionOfView(self, view):
        '''
        Returns cairo path of given view
        @type view: CBaseView
        @param view: desired view
        @rtype: cairo.Path
        @return: cairo path of given view or None
        '''
        return self.GetPathOfConnection(view) or self.GetPathOfElement(view)
        
    
    def GetElementAtPoint(self, point):
        '''
        Returns element view at given point
        @type point: tuple
        @param point: point coordinates (x, y)
        @rtype: CElementView
        @return: element view at given point or None
        '''
        result = None
        if self.__context is not None:
            for el, path in self.__paintedElements.items():
                self.__context.new_path()
                self.__context.append_path(path)
                if self.__context.in_fill(point[0], point[1]):
                    result = el
                
        return result
    
    def GetPathOfElement(self, el):
        '''
        Returns cairo path of given element view
        @type el: CElementView
        @param el: desired element view
        @rtype: cairo.Path
        @return: cairo path of given element view or None
        '''
        return self.__paintedElements.get(el, None)
    
    def GetConnectionAtPoint(self, point):
        '''
        Returns connection view at given point
        @type point: tuple
        @param point: point coordinates (x, y)
        @rtype: CConnectionView
        @return: connection view at given point or None
        '''
        result = None
        if self.__context is not None:
            for con, path in self.__paintedConnections.items():
                self.__context.new_path()
                self.__context.append_path(path)
                if self.__context.in_stroke(point[0], point[1]):
                    result = con
        return result
    
    def GetPathOfConnection(self, con):
        '''
        Returns cairo path of given connection view
        @type con: CElementView
        @param con: desired connection view
        @rtype: cairo.Path
        @return: cairo path of given connection view or None
        '''
        return self.__paintedConnections.get(con, None)
    
    def __PaintView(self, context, view, r, g, b, a=None):
        '''
        Paints view at given context with desired color
        @type context: CairoContext
        @param context: will be painted on this context
        @type view: CBaseView
        @param view: view to be painted
        @type r: int
        @param r: red part of color
        @type g: int
        @param g: green part of color
        @type b: int
        @param b: blue part of color
        @type a: float
        @param a: alpha
        '''
        if isinstance(view, CElementView):
            path = self.__PaintElement(context, view, r, g, b, a)
            self.__paintedElements[view] = path
        elif isinstance(view, CConnectionView):
            path = self.__PaintConnection(context, view, r, g, b, a)
            self.__paintedConnections[view] = path
                    
    
    def __PaintConnection(self, context, connection, r, g, b, a = None):
        '''
        Paints connection view at given context with desired color
        @type context: CairoContext
        @param context: will be painted on this context
        @type connection: CConnectionView
        @param connection: connection view to be painted
        @type r: int
        @param r: red part of color
        @type g: int
        @param g: green part of color
        @type b: int
        @param b: blue part of color
        @type a: float
        @param a: alpha
        '''
        cd = CConnectionDrawing(connection, context)
        cd.ChangeColor(context, r, g, b, a)
        return cd.Paint()        
        
        
        
    def __PaintElement(self, context, element, r, g, b, a = None):
        '''
        Paints element view at given context with desired color
        @type context: CairoContext
        @param context: will be painted on this context
        @type element: CElementView
        @param element: element view to be painted
        @type r: int
        @param r: red part of color
        @type g: int
        @param g: green part of color
        @type b: int
        @param b: blue part of color
        @type a: float
        @param a: alpha
        '''
        ed = CElementDrawing(element, context)
        ed.ChangeColor(context, r, g, b, a)
        return ed.Paint()        
          
        
    def GetSize(self):
        '''
        Returns size of diagram
        @rtype: tuple
        @return: size of diagram (x, y)
        '''
        if self.__context is not None:
            self.__context.new_path()
            for path in self.__paintedElements.values() + self.__paintedConnections.values():
                self.__context.append_path(path)
            ext = self.__context.fill_extents()
            return (ext[2],ext[3])
        else:
            return (0,0)
    