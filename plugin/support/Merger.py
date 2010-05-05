'''
Created on 10.4.2010

@author: Peterko
'''
from DiffActions import EDiffActions
from structure import *

class CMerger(object):
    '''
    Class provides merging capabilities. Merges diffs to desired project
    '''


    def __init__(self, project):
        '''
        Constructor
        @type project: CProject
        @param project: Project that will accept merges
        '''
        self.__project = project
        
    def GetProject(self):
        '''
        Returns project
        @rtype: CProject
        @return: project
        '''
        return self.__project
        
    def MergeDiffs(self, diffs):
        '''
        Tries to merge all diffs from given
        @type diffs: list
        @param diffs: Diffs to be merged
        @raise Exception: if all diffs cannot be applied, raises exception
        '''
        
        stopper = {}
        while len(diffs) > 0 :
            diff  = diffs.pop()
            if stopper.get(diff, -1) == len(diffs):
                raise Exception(_('Unable to merge all diffs'), [str(d) for d in diffs])
            stopper[diff] = len(diffs)
            
            ok = self.MergeDiff(diff)
            if not ok:
                diffs.insert(0, diff)
    
        
    def MergeDiff(self, diff):
        '''
        Merges one diff
        @type diff: CDiffResult
        @param diff: diff to be applied
        @rtype: bool
        @return: True if diff was applied, False otherwise
        '''
        result = True
        element = diff.GetElement()
        try:
            if diff.GetAction() == EDiffActions.INSERT:
                
                if isinstance(element, CBase):
                    self.__project.AddObject(element)
                
                elif isinstance(element, CProjectTreeNode):
                    self.__project.AddProjectTreeNode(element)
                    
                elif isinstance(element, CBaseView):
                    self.__project.AddView(element)
                
            
            elif diff.GetAction() == EDiffActions.DELETE:
                if isinstance(element, CBase):
                    self.__project.DeleteObject(element)
                
                
                elif isinstance(element, CProjectTreeNode):
                    self.__project.DeleteProjectTreeNode(element)
                    
                elif isinstance(element, CBaseView):
                    self.__project.DeleteView(element) 
                
                
            
            elif diff.GetAction() == EDiffActions.MODIFY:
                if isinstance(element, CBase):
                    self.__project.ModifyObjectData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
                elif isinstance(element, CBaseView):
                    self.__project.ModifyViewData(element, diff.GetPreviousState(), diff.GetNewState(), diff.GetDataPath())
                    
            elif diff.GetAction() == EDiffActions.MOVE:
                self.__project.MoveProjectTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
            
            elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
                if isinstance(element, CProjectTreeNode):
                    self.__project.ChangeOrderTreeNode(element, diff.GetPreviousState(), diff.GetNewState())
                elif isinstance(element, CBaseView):
                    self.__project.ChangeOrderView(element, diff.GetPreviousState(), diff.GetNewState())
            
            elif diff.GetAction() == EDiffActions.LET:
                pass
                
        except Exception, e:
            print e
            result = False
        return result
        