'''
Created on 14.3.2010

@author: Peterko
'''
from BaseView import CBaseView

class CConnectionView(CBaseView):
    '''
    Class representing visual of connection data object
    '''


    def __init__(self, connection, parentDiagram):
        '''
        Constructor
        @type connection: CConnection
        @param connection: Underlying object representation
        @type parentDiagram: CDiagram
        @param parentDiagram: Parent diagram of view
        '''
        super(CConnectionView, self).__init__(connection, parentDiagram)
        
        self.viewData = {'points':[], 'labels':[]}
        
    def AddPoint(self, point):
        '''
        Adds point to points
        @type point: dic or tuple
        @param point: Point to be added 
        '''
        if type(point) == type({}):
            point = (point['x'], point['y'])
        self.viewData['points'].append({'x':point[0], 'y':point[1]})
        
    def GetPoints(self):
        '''
        Returns points
        @rtype: list
        @return: Points
        '''
        return self.viewData['points']
    
    def AddLabel(self, label):
        '''
        Adds label to labels
        @type label: dic
        @param label: Label to be added 
        '''
        self.viewData['labels'].append(label)
        
    def GetLabels(self):
        '''
        Returns labels
        @rtype: list
        @return: Labels
        '''
        return self.viewData['labels']
    
    def GetSourceView(self):
        '''
        Returns view of source element
        @rtype: CElementView
        @return: view of source element
        '''
        return self.GetParentDiagram().GetViewById(self.GetObject().GetSource().GetId())
    
    def GetDestinationView(self):
        '''
        Returns view of destination element
        @rtype: CElementView
        @return: view of destination element
        '''
        return self.GetParentDiagram().GetViewById(self.GetObject().GetDestination().GetId())
    
    def ModifyData(self, oldState, newState, path):
        '''
        Modifies data in path from old state to new state
        @type oldState: object
        @param oldState: old state of data
        @type newState: object
        @param newState: new state of data
        @type path: list
        @param path: path to modification
        '''
        if oldState is None:
            
            if type(newState) is type([]):
                self.viewData[path[0]].extend(newState)
            else:
                self.viewData[path[0]].append(newState)
        elif newState is None:
            
            
            self.viewData[path[0]].remove(oldState)
            
        else:
            
            self.viewData[path[0]][path[1]].update(newState)
            
    