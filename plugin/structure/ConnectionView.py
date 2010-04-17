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
        
        self.viewData = {'points':[], 'labels':[]}
        
    def AddPoint(self, point):
        if type(point) == type({}):
            point = (point['x'], point['y'])
        self.viewData['points'].append({'x':point[0], 'y':point[1]})
        
    def GetPoints(self):
        return self.viewData['points']
    
    def AddLabel(self, label):
        
        self.viewData['labels'].append(label)
        
    def GetLabels(self):
        return self.viewData['labels']
    
    def GetSourceView(self):
        return self.GetParentDiagram().GetViewById(self.GetObject().GetSource().GetId())
    
    def GetDestinationView(self):
        return self.GetParentDiagram().GetViewById(self.GetObject().GetDestination().GetId())
    
    def ModifyData(self, oldState, newState, path):
        print 'modifying connection view'
        print oldState, newState, path
        if oldState is None:
            #pridanie
            if type(newState) is type([]):
                self.viewData[path[0]].extend(newState)
            else:
                self.viewData[path[0]].append(newState)
        elif newState is None:
            #vymazanie
            
            self.viewData[path[0]].remove(oldState)
            
        else:
            #uprava
            self.viewData[path[0]][path[1]].update(newState)
            
    