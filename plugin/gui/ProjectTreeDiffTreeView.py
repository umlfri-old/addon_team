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


    def __init__(self, differ, model):
        '''
        Constructor
        '''
        self.differ = differ
        self.projectOld = self.differ.GetOldProject()
        self.projectNew = self.differ.GetNewProject()
        #self.diffs = diffs[:]
        self.model = model
        self.connectionsIter = None
        self.Create()
        
    def Create(self):
        self.model.clear()
        self.__Append(self.projectOld.GetProjectTreeRoot())
        self.__AppendConnections()
        self.__ShowDiffs()
        
    def __Append(self, node, iter=None, icon = None, icon2 = None):
        
        iter = self.model.append(iter, [node.GetObject().GetName(), icon, icon2, node])
        for child in node.GetChildsOrdered():
            self.__Append(child, iter, icon, icon2)
            
    def __AppendConnections(self):
        self.connectionsIter = self.model.append(None, ['Connections', None, None, None])
        for c in self.projectOld.GetConnections().values():
            self.model.append(self.connectionsIter, [c.GetSource().GetName()+' -> '+c.GetDestination().GetName(), None, None, c])
            
    def __ShowDiffs(self):
        self.diffs = self.differ.GetProjectTreeDiff().get(EDiffActions.INSERT, [])
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowInsertDiff(diff)
            self.diffs.reverse()
            
        self.diffs = self.differ.GetProjectTreeDiff().get(EDiffActions.DELETE, [])
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowDeleteDiff(diff)
            self.diffs.reverse()
            
        self.diffs = self.differ.GetProjectTreeDiff().get(EDiffActions.MOVE, [])
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowMoveDiff(diff)
            self.diffs.reverse()
            
        self.diffs = self.differ.GetProjectTreeDiff().get(EDiffActions.ORDER_CHANGE, [])
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowOrderChangeDiff(diff)
            self.diffs.reverse()
        
        self.diffs = self.differ.GetDataDiff().get(EDiffActions.INSERT, [])
        self.diffs = [d for d in self.diffs if isinstance(d.GetElement(), CConnection)]
        print 'insert connections'
        print self.diffs
        for d in self.diffs:
            iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert.png")
            icon = gtk.gdk.pixbuf_new_from_file(iconfile)
            c = d.GetElement()
            self.model.append(self.connectionsIter, [c.GetSource().GetName()+' -> '+c.GetDestination().GetName(), icon, None, c])
            
        self.diffs = self.differ.GetDataDiff().get(EDiffActions.DELETE, [])
        self.diffs = [d for d in self.diffs if isinstance(d.GetElement(), CConnection)]
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowDeleteConnectionsDiff(diff)
            self.diffs.reverse()
        
        
        self.diffs = self.differ.GetDataDiff().get(EDiffActions.MODIFY, [])
        while len(self.diffs) > 0:
            diff = self.diffs[0]
            self.__ShowModifiedDiff(diff)
            self.diffs.reverse()
            
        
    def __ShowInsertDiff(self, diff):
        def func(model, path, iter, diff):
            
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetElement().GetParent():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                pos = model.iter_nth_child(iter, diff.GetElement().GetAbsoluteIndex())
                model.insert_before(iter, pos, [diff.GetElement().GetObject().GetName(), icon, None, diff.GetElement()])
                
                self.__MarkParentAsModified(path, True)
                
                self.diffs.remove(diff)
                return True
            
            
        
        self.model.foreach(func, diff)
        
        
    def __ShowDeleteDiff(self, diff):
        def func(model, path, iter, diff):
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                self.__MarkParentAsModified(path)
                self.diffs.remove(diff)
                return True
        
        self.model.foreach(func, diff)
        
        
    def __ShowMoveDiff(self, diff):
        def func1(model, path, iter, diff):
            if model.get_value(iter, 3) is not None and model.get_value(iter,3)  == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete-move.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                
                self.__MarkParentAsModified(path)
                
                self.diffs.remove(diff)
                return True
        
        def func2(model, path, iter, diff):
            
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetNewState():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert-move.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                new = self.projectNew.GetProjectTreeNodeById(diff.GetElement().GetId())
                pos = model.iter_nth_child(iter, new.GetAbsoluteIndex())
                model.insert_before(iter, pos, [new.GetObject().GetName(), icon, None, new])
                
                self.__MarkParentAsModified(path, True)
                
                #self.diffs.remove(diff)
                return True
        
        self.model.foreach(func1, diff)
        self.model.foreach(func2, diff)
    
    
    def __ShowOrderChangeDiff(self, diff):
        def func1(model, path, iter, diff):
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"order-change-old.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                
                self.__MarkParentAsModified(path)
                
                self.diffs.remove(diff)
                return True
        
        def func2(model, path, iter, diff):
            
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetElement().GetParent():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"order-change-new.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                if diff.GetNewState() > diff.GetPreviousState():
                
                    pos = model.iter_nth_child(iter, diff.GetNewState() + 1)
                else:
                    pos = model.iter_nth_child(iter, diff.GetNewState())
                model.insert_before(iter, pos, [diff.GetElement().GetObject().GetName(), icon, None, diff.GetElement()])
                
                self.__MarkParentAsModified(path, True)
                
                #self.diffs.remove(diff)
                return True
        
        self.model.foreach(func1, diff)
        self.model.foreach(func2, diff)
    
    def __ShowDeleteConnectionsDiff(self, diff):
        def func(model, path, iter, diff):
            if model.get_value(iter, 3) is not None and model.get_value(iter,3) == diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, icon)
                self.__MarkParentAsModified(path)
                self.diffs.remove(diff)
                
        self.model.foreach(func, diff)
    
    def __ShowModifiedDiff(self, diff):
        def func(model, path, iter, diff):
            if model.get_value(iter, 3) is not None and model.get_value(iter,3).GetObject()== diff.GetElement():
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"modify.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                model.set_value(iter, 0, self.projectNew.GetById(diff.GetElement().GetId()).GetName())
                model.set_value(iter, 2, icon)
                self.__MarkParentAsModified(path)
            
        self.model.foreach(func, diff)
        self.diffs.remove(diff)
    
    
    def __MarkParentAsModified(self, path, include = False):
        if include == False:
            path = path[0:-1]
        for i,x in enumerate(path):
            newpath = path[0:i+1]
            newiter = self.model.get_iter(newpath)
            iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"modify.png")
            icon = gtk.gdk.pixbuf_new_from_file(iconfile)
            self.model.set_value(newiter, 2, icon)