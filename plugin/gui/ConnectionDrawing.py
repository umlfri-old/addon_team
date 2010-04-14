'''
Created on 13.4.2010

@author: Peterko
'''
from BaseDrawing import CBaseDrawing
from math import pi

class CConnectionDrawing(CBaseDrawing):
    '''
    classdocs
    '''


    def __init__(self, connectionView, context):
        '''
        Constructor
        '''
        super(CConnectionDrawing, self).__init__(context)
        self.connectionView = connectionView
        
    def Paint(self):
        sourceView = self.connectionView.GetSourceView()
        destView = self.connectionView.GetDestinationView()
        sourceViewCenter = (int(sourceView.GetPosition()['x']) + (self.defaultElementWidth + int(sourceView.GetSize()['dw'])) / 2,
                            int(sourceView.GetPosition()['y']) + (self.defaultElementHeight + int(sourceView.GetSize()['dh'])) / 2)
        
        destViewCenter = (int(destView.GetPosition()['x']) + (self.defaultElementWidth + int(destView.GetSize()['dw'])) / 2,
                            int(destView.GetPosition()['y']) + (self.defaultElementHeight + int(destView.GetSize()['dh'])) / 2)
        self.context.move_to(sourceViewCenter[0],sourceViewCenter[1])
        for point in self.connectionView.GetPoints():
            self.context.line_to(int(point['x']), int(point['y']))
        self.context.line_to(destViewCenter[0],destViewCenter[1])
        self.context.stroke()
        
        self.context.arc(destViewCenter[0], destViewCenter[1], 5, 0, 2*pi)
        self.context.fill()
        
        for label in self.connectionView.GetLabels():
            self.context.save()
            idx = int(label['idx'])
            lineStart = sourceViewCenter
            lineEnd = destViewCenter
            if len(self.connectionView.GetPoints()) > 0:
                if idx - 1 > 0:
                    try:
                        lineStart = (int(self.connectionView.GetPoints()[idx - 1]['x']), int(self.connectionView.GetPoints()[idx - 1]['y']))
                    except:
                        pass
                        
                try:
                    lineEnd = (int(self.connectionView.GetPoints()[idx]['x']), int(self.connectionView.GetPoints()[idx]['y']))
                except:
                    pass
            
            
            pos = float(label['pos'])
            
            self.context.move_to(lineStart[0], lineStart[1])
            
            self.context.rel_move_to((lineEnd[0] - lineStart[0]) * pos, (lineEnd[1] - lineStart[1]) * pos)
            
            
            angle = float(label['angle'])
            
            
            self.context.rotate(-(angle))
            
            dist = float(label['dist'])
            self.context.rel_move_to(dist, 0)
            self.context.restore()
            (px, py) = self.context.get_current_point()
            self.context.rectangle(px, py, self.defaultLabelWidth, self.defaultLabelHeight)
            
            
        
        
        self.context.stroke()