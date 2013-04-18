'''
Created on 13.4.2010

@author: Peterko
'''

class CBaseDrawing:
    '''
    Base class for drawing objects
    '''


    def __init__(self, context):
        '''
        Constructor
        @type context: CairoContext
        @param context: cairo context, will be painted on this context
        '''
        self.defaultElementWidth, self.defaultElementHeight = 50,50
        self.defaultLabelWidth, self.defaultLabelHeight = 30,10
        self.context = context
        self.context.new_path()
        
    def ChangeColor(self, context, r, g, b, alpha=None):
        '''
        Change color on given context
        @type context: CairoContext
        @param context: cairo context on which color will be changed
        @type r: int or float
        @param r: red part of color
        @type g: int or float
        @param g: green part of color
        @type b: int or float
        @param b: blue part of color
        @type alpha: float
        @param alpha: alpha part from 0.0 to 1.0
        '''
        if alpha is None:
            context.set_source_rgb(float(r)/255.0, float(g)/255.0, float(b)/255.0)
        else: 
            context.set_source_rgba(float(r)/255.0, float(g)/255.0, float(b)/255.0, alpha)