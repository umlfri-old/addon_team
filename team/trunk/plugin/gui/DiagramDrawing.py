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
        
        
    def Paint(self, context):
        if self.__diagram is not None:
            for view in self.__diagram.GetViews().values():
                self.__PaintView(context, view, 128, 128, 128, 0.2)
                

    
    def __PaintView(self, context, view, r, g, b, a=None):
        if isinstance(view, CElementView):
            self.__PaintElement(context, view, r, g, b, a)
        elif isinstance(view, CConnectionView):
            self.__PaintConnection(context, view, r, g, b, a)                
                    
    
    def __PaintConnection(self, context, connection, r, g, b, a = None):
        
        cd = CConnectionDrawing(connection, context)
        cd.ChangeColor(context, r, g, b, a)
        cd.Paint()        
        
        
        
    def __PaintElement(self, context, element, r, g, b, a = None):
      
        ed = CElementDrawing(element, context)
        ed.ChangeColor(context, r, g, b, a)
        ed.Paint()        
          
        
         
    