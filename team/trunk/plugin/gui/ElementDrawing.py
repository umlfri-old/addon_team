'''
Created on 13.4.2010

@author: Peterko
'''
from BaseDrawing import CBaseDrawing

class CElementDrawing(CBaseDrawing):
    '''
    classdocs
    '''
    

    def __init__(self, elementView, context):
        '''
        Constructor
        '''
        super(CElementDrawing, self).__init__(context)
        self.elementView = elementView
        
    def Paint(self):
        self.context.rectangle(int(self.elementView.GetPosition()['x']), 
                      int(self.elementView.GetPosition()['y']), 
                      self.defaultElementWidth + int(self.elementView.GetSize()['dw']), 
                      self.defaultElementHeight + int(self.elementView.GetSize()['dh']))
        self.context.fill()   