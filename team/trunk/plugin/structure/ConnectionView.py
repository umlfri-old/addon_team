'''
Created on 14.3.2010

@author: Peterko
'''
from BaseView import CBaseView

class CConnectionView(CBaseView):
    '''
    classdocs
    '''


    def __init__(self, connection):
        '''
        Constructor
        '''
        super(CConnectionView, self).__init__(connection)
        self.__points = []
        self.__labels = []
        
    def AddPoint(self, point):
        self.__points.append(point)
        
    def GetPoints(self):
        return self.__points
    
    def AddLabel(self, label):
        self.__labels.append(label)
        
    def GetLabels(self):
        return self.__labels