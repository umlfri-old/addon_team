'''
Created on 13.4.2010

@author: Peterko
'''
from BaseDrawing import CBaseDrawing
from ConnectionDrawing import CConnectionDrawing
from ElementDrawing import CElementDrawing
from support import EDiffActions
from structure import *

class CDiffDrawing(CBaseDrawing):
    '''
    classdocs
    '''


    def __init__(self, context, diff, oldDiagram, newDiagram):
        '''
        Constructor
        '''
        super(CDiffDrawing, self).__init__(context)
        self.diff = diff
        self.oldDiagram = oldDiagram
        self.newDiagram = newDiagram
        
    def Paint(self):
        print 'painting'
        
        if self.diff.GetAction() == EDiffActions.DELETE:
            self.ChangeColor(self.context, 255, 0, 0, 0.2)
            self.__PaintElement(self.diff.GetElement())
        elif self.diff.GetAction() == EDiffActions.INSERT:
            self.ChangeColor(self.context, 0, 255, 0, 0.2)
            self.__PaintElement(self.diff.GetElement())
            
        elif self.diff.GetAction() == EDiffActions.MODIFY:
            oldElementView = self.oldDiagram.GetViewById(self.diff.GetElement().GetObject().GetId())
            self.ChangeColor(self.context, 255, 255, 0, 0.2)
            self.__PaintElement(oldElementView)
            
            newElementView = self.newDiagram.GetViewById(self.diff.GetElement().GetObject().GetId())
            
            self.ChangeColor(self.context, 0, 255, 255, 0.2)
            self.__PaintElement(newElementView)
            
        elif self.diff.GetAction() == EDiffActions.ORDER_CHANGE:
            oldElementView = self.oldDiagram.GetViewById(self.diff.GetElement().GetObject().GetId())
            self.ChangeColor(self.context, 255, 0, 255, 0.2)
            self.__PaintElement(oldElementView)
            
            newElementView = self.newDiagram.GetViewById(self.diff.GetElement().GetObject().GetId())
            
            self.__PaintElement(newElementView)
                
    def __PaintElement(self, elementView):
        if isinstance(elementView, CConnectionView):
            cd = CConnectionDrawing(elementView, self.context)
            cd.Paint()
        elif isinstance(elementView, CElementView):
            ed = CElementDrawing(elementView,self.context)
            ed.Paint()