'''
Created on 13.4.2010

@author: Peterko
'''
from BaseDrawing import CBaseDrawing

class CElementDrawing(CBaseDrawing):
    '''
    Class representing drawing of element
    '''
    

    def __init__(self, elementView, context):
        '''
        Constructor
        @type elementView: CElementView
        @param elementView: underlying element view object
        @type context: CairoContext
        @param context: will be painted on this context
        '''
        super(CElementDrawing, self).__init__(context)
        self.elementView = elementView
        
    def Paint(self):
        '''
        Paints element drawing
        @rtype: cairo.Path
        @return: returns path that was painted
        '''
        self.context.rectangle(int(self.elementView.GetPosition()['x']), 
                      int(self.elementView.GetPosition()['y']), 
                      self.defaultElementWidth + int(self.elementView.GetSize()['dw']), 
                      self.defaultElementHeight + int(self.elementView.GetSize()['dh']))
        
        path = self.context.copy_path()
        self.context.fill()
        return path   