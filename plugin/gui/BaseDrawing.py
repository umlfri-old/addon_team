'''
Created on 13.4.2010

@author: Peterko
'''

class CBaseDrawing(object):
    '''
    classdocs
    '''


    def __init__(self, context):
        '''
        Constructor
        '''
        self.defaultElementWidth, self.defaultElementHeight = 50,50
        self.defaultLabelWidth, self.defaultLabelHeight = 30,10
        self.context = context
        
    def ChangeColor(self, context, r, g, b, alpha=None):
        if alpha is None:
            context.set_source_rgb(float(r)/255.0, float(g)/255.0, float(b)/255.0)
        else: 
            context.set_source_rgba(float(r)/255.0, float(g)/255.0, float(b)/255.0, alpha)