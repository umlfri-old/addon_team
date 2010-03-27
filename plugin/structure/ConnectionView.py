'''
Created on 14.3.2010

@author: Peterko
'''
from BaseView import CBaseView

class CConnectionView(CBaseView):
    '''
    classdocs
    '''


    def __init__(self, connection, parentDiagram):
        '''
        Constructor
        '''
        super(CConnectionView, self).__init__(connection, parentDiagram)
        self.__points = []
        self.__labels = []
        self.viewData = {'points':[], 'labels':[]}
        
    def AddPoint(self, point):
        self.__points.append({'x':point[0], 'y':point[1]})
        self.viewData['points'] = self.__points
        
    def GetPoints(self):
        return self.__points
    
    def AddLabel(self, label):
        self.__labels.append(label)
        self.viewData['labels'] = self.__labels
        
    def GetLabels(self):
        return self.__labels
    
