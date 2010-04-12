'''
Created on 12.4.2010

@author: Peterko
'''
from structure import *
from support import EDiffActions
import math

class CDiffDrawing(object):
    '''
    classdocs
    '''
    
    defaultElementWidth, defaultElementHeight = 50,50
    defaultLabelWidth, defaultLabelHeight = 30,10

    def __init__(self, newDiagram, oldDiagram, diffs):
        '''
        Constructor
        '''
        
        self.__oldDiagram = oldDiagram
        
        self.__newDiagram = newDiagram
        print 'old diagram',self.__oldDiagram
        print 'new diagram',self.__newDiagram
        self.__diffs = diffs
        
    def Paint(self, widget):
        con = widget.window.cairo_create()
        self.__ChangeColor(con, 255, 255, 255)
        rect = widget.get_allocation()
        con.rectangle(0,0, rect.width, rect.height)
        con.fill()
        if self.__oldDiagram is not None:
            for view in self.__oldDiagram.GetViews().values():
                self.__PaintView(con, view, 128, 128, 128)
                
        for diff in self.__diffs:
            if isinstance(diff.GetElement(), CBaseView):
                # vyber iba vizualne diffy
                if diff.GetElement().GetParentDiagram() == self.__oldDiagram or diff.GetElement().GetParentDiagram() == self.__newDiagram :
                    # vyber iba take diffy, ktore su na tomto diagrame
                    view = diff.GetElement()
                    if diff.GetAction() == EDiffActions.DELETE:
                        self.__PaintView(con, view, 255, 0, 0, 0.2)
                        
                    elif diff.GetAction() == EDiffActions.INSERT:
                        self.__PaintView(con, view, 0, 255, 0, 0.2)
                        
                    elif diff.GetAction() == EDiffActions.MODIFY:
                        oldView = self.__oldDiagram.GetViewById(view.GetObject().GetId())
                        self.__PaintView(con, oldView, 0, 0, 255, 0.2)
                        newView = self.__newDiagram.GetViewById(view.GetObject().GetId())
                        self.__PaintView(con, newView, 0, 0, 255, 0.2)
    
    
    def __PaintView(self, context, view, r, g, b, a=None):
        if isinstance(view, CElementView):
            self.__PaintElement(context, view, r, g, b, a)
        elif isinstance(view, CConnectionView):
            self.__PaintConnection(context, view, r, g, b, a)                
                    
    
    def __PaintConnection(self, context, connection, r, g, b, a = None):
        self.__ChangeColor(context, r, g, b, a)
                
        sourceView = connection.GetSourceView()
        destView = connection.GetDestinationView()
        sourceViewCenter = (int(sourceView.GetPosition()['x']) + (self.defaultElementWidth + int(sourceView.GetSize()['dw'])) / 2,
                            int(sourceView.GetPosition()['y']) + (self.defaultElementHeight + int(sourceView.GetSize()['dh'])) / 2)
        
        destViewCenter = (int(destView.GetPosition()['x']) + (self.defaultElementWidth + int(destView.GetSize()['dw'])) / 2,
                            int(destView.GetPosition()['y']) + (self.defaultElementHeight + int(destView.GetSize()['dh'])) / 2)
        context.move_to(sourceViewCenter[0],sourceViewCenter[1])
        for point in connection.GetPoints():
            context.line_to(int(point['x']), int(point['y']))
        context.line_to(destViewCenter[0],destViewCenter[1])
        
        for label in connection.GetLabels():
            context.save()
            idx = int(label['idx'])
            lineStart = sourceViewCenter
            lineEnd = destViewCenter
            if len(connection.GetPoints()) > 0:
                if idx - 1 > 0:
                    try:
                        lineStart = (int(connection.GetPoints()[idx - 1]['x']), int(connection.GetPoints()[idx - 1]['y']))
                    except:
                        pass
                        
                try:
                    lineEnd = (int(connection.GetPoints()[idx]['x']), int(connection.GetPoints()[idx]['y']))
                except:
                    pass
            
            
            pos = float(label['pos'])
            
            context.move_to(lineStart[0], lineStart[1])
            
            context.rel_move_to((lineEnd[0] - lineStart[0]) * pos, (lineEnd[1] - lineStart[1]) * pos)
            
            
            angle = float(label['angle'])
            
            
            context.rotate(-(angle))
            
            dist = float(label['dist'])
            context.rel_move_to(dist, 0)
            context.restore()
            (px, py) = context.get_current_point()
            context.rectangle(px, py, self.defaultLabelWidth, self.defaultLabelHeight)
            
            
        
        
        context.stroke()
        
        
    def __PaintElement(self, context, element, r, g, b, a = None):
        self.__ChangeColor(context, r, g, b, a)
                
        context.rectangle(int(element.GetPosition()['x']), 
                      int(element.GetPosition()['y']), 
                      self.defaultElementWidth + int(element.GetSize()['dw']), 
                      self.defaultElementHeight + int(element.GetSize()['dh']))
        context.fill()     
        
         
    def __ChangeColor(self, context, r, g, b, alpha=None):
        if alpha is None:
            context.set_source_rgb(float(r)/255.0, float(g)/255.0, float(b)/255.0)
        else: 
            context.set_source_rgba(float(r)/255.0, float(g)/255.0, float(b)/255.0, alpha)