'''
Created on 10.4.2010

@author: Peterko
'''
from DiffActions import EDiffActions
from structure import *

class CMerger(object):
    '''
    classdocs
    '''


    def __init__(self, project):
        '''
        Constructor
        '''
        self.__project = project
        
    def GetProject(self):
        return self.__project
        
    def MergeDiffs(self, diffs):
        stopper = {}
        while len(diffs) > 0 :
            diff  = diffs.pop()
            print 'merging', diff, stopper.get(diff, -1)
            if stopper.get(diff, -1) == len(diffs):
                raise Exception('Unable to merge all diffs', [str(d) for d in diffs])
            stopper[diff] = len(diffs)
            
            ok = self.MergeDiff(diff)
            print ok
            if not ok:
                diffs.insert(0, diff)
    
        
    def MergeDiff(self, diff):
        print 'merging',diff
        result = True
        element = diff.GetElement()
        try:
            if diff.GetAction() == EDiffActions.INSERT:
                
                if isinstance(element, CBase):
                    print 'adding object'
                    self.__project.AddObject(element)
                
                elif isinstance(element, CProjectTreeNode):
                    print 'adding project tree node'
                    self.__project.AddProjectTreeNode(element)
                    
                elif isinstance(element, CBaseView):
                    print 'adding view'
                    self.__project.AddView(element)
                
            
            elif diff.GetAction() == EDiffActions.DELETE:
                if isinstance(element, CBase):
                    print 'deleting object'
                    self.__project.DeleteObject(element)
                
                
                elif isinstance(element, CProjectTreeNode):
                    print 'deleting project tree node'
                    self.__project.DeleteProjectTreeNode(element)
                    
                elif isinstance(element, CBaseView):
                    print 'deleting view'
                    self.__project.DeleteView(element) 
                
                
            
            elif diff.GetAction() == EDiffActions.MODIFY:
                if isinstance(element, CBase):
                    print 'modifying object data'
                    self.__project.ModifyObjectData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
                elif isinstance(element, CBaseView):
                    print 'modyfing view data'
                    self.__project.ModifyViewData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
                    
            elif diff.GetAction() == EDiffActions.MOVE:
                print 'moving project tree node'
                self.__project.MoveProjectTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
            
            elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
                if isinstance(element, CProjectTreeNode):
                    print 'changing order project tree node'
                    self.__project.ChangeOrderTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
                elif isinstance(element, CBaseView):
                    print 'changing order view'
                    self.__project.ChangeOrderView(element, diff.GetPreviousState(), diff.GetNewState())
        except Exception, e:
            print e
            result = False
        return result
        