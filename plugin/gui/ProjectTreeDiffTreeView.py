'''
Created on 13.4.2010

@author: Peterko
'''
from structure import *
from support import EDiffActions
import os
from imports.gtk2 import gtk 

class CProjectTreeDiffTreeView(object):
    '''
    classdocs
    '''


    def __init__(self, projectOld, projectNew, diffs, model):
        '''
        Constructor
        '''
        self.projectOld = projectOld
        self.projectNew = projectNew
        self.diffs = diffs[:]
        self.model = model
        self.Create()
        
    def Create(self):
        self.model.clear()
        self.__Append(self.projectOld.GetProjectTreeRoot())
        self.__ShowDiffs()
        
    def __Append(self, node, iter=None, icon = None):
        
        iter = self.model.append(iter, [node.GetObject().GetName(), icon, node])
        for child in node.GetChildsOrdered():
            self.__Append(child, iter, icon)
            
    def __ShowDiffs(self):
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            if isinstance(diff.GetElement(), CProjectTreeNode):
                if diff.GetAction() == EDiffActions.INSERT:
                    self.__ShowInsertDiff(diff)
                elif diff.GetAction() == EDiffActions.DELETE:
                    self.__ShowDeleteDiff(diff)
                elif diff.GetAction() == EDiffActions.MOVE:
                    self.__ShowMoveDiff(diff)
                elif diff.GetAction() == EDiffActions.ORDER_CHANGE:
                    self.__ShowOrderChangeDiff(diff)
                
                
            elif isinstance(diff.GetElement(), CBase):
                self.diffs.remove(diff)
            else:
                self.diffs.remove(diff)
            
            self.diffs.reverse()
            
    def __ShowInsertDiff(self, diff):
        def func(model, path, iter, diff):
            
            if model.get_value(iter, 2) == diff.GetElement().GetParent():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                pos = model.iter_nth_child(iter, diff.GetElement().GetAbsoluteIndex())
                model.insert_before(iter, pos, [diff.GetElement().GetObject().GetName(), icon, diff.GetElement()])
                
                self.diffs.remove(diff)
                return True
            
            
        
        self.model.foreach(func, diff)
        
        
    def __ShowDeleteDiff(self, diff):
        def func(model, path, iter, diff):
            if model.get_value(iter, 2) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                self.diffs.remove(diff)
                return True
        
        self.model.foreach(func, diff)
        
        
    def __ShowMoveDiff(self, diff):
        def func1(model, path, iter, diff):
            if model.get_value(iter, 2) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete-move.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                self.diffs.remove(diff)
                return True
        
        def func2(model, path, iter, diff):
            
            if model.get_value(iter, 2) == diff.GetNewState():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert-move.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                new = self.projectNew.GetProjectTreeNodeById(diff.GetElement().GetId())
                pos = model.iter_nth_child(iter, new.GetAbsoluteIndex())
                model.insert_before(iter, pos, [new.GetObject().GetName(), icon, new])
                
                #self.diffs.remove(diff)
                return True
        
        self.model.foreach(func1, diff)
        self.model.foreach(func2, diff)
    
    
    def __ShowOrderChangeDiff(self, diff):
        def func1(model, path, iter, diff):
            if model.get_value(iter, 2) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"order-change-old.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                self.diffs.remove(diff)
                return True
        
        def func2(model, path, iter, diff):
            
            if model.get_value(iter, 2) == diff.GetElement().GetParent():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"order-change-new.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                if diff.GetNewState() > diff.GetPreviousState():
                
                    pos = model.iter_nth_child(iter, diff.GetNewState() + 1)
                else:
                    pos = model.iter_nth_child(iter, diff.GetNewState())
                model.insert_before(iter, pos, [diff.GetElement().GetObject().GetName(), icon, diff.GetElement()])
                
                #self.diffs.remove(diff)
                return True
        
        self.model.foreach(func1, diff)
        self.model.foreach(func2, diff)
    