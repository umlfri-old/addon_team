'''
Created on 13.4.2010

@author: Peterko
'''
from support import EDiffActions
import os
from imports.gtk2 import gtk 

class CDataDiffTreeView(object):
    '''
    Class representing tree view with data diff
    '''


    def __init__(self, objectOld, objectNew, differ, model, conflicts):
        '''
        Constructor
        @type objectOld: CBase
        @param objectOld: old object
        @type objectNew: CBase
        @param objectNew: new object
        @type differ: CDiffer
        @param differ: CDiffer instance holding diffs of given objects
        @type model: gtk.TreeModel
        @param model: model where diff will be held
        @type conflicts: list
        @param conflicts: list of conflicts, possible conflicts between objects
        '''
        self.objectOld = objectOld
        self.objectNew = objectNew
        self.differ = differ
        self.model = model
        self.conflicts = conflicts
        self.Create()
        
    def Create(self):
        '''
        Fills model with appropriate data
        '''
        self.model.clear()
        if self.objectOld is None:
            self.__ShowData(self.objectNew, EDiffActions.INSERT)
        elif self.objectNew is None:
            self.__ShowData(self.objectOld, EDiffActions.DELETE)
        else:
            self.__ShowData(self.objectOld)
            self.__ShowDiffs()
            self.__ShowConflicts()
    
    
    def __ShowConflicts(self):
        '''
        Shows conflicts
        '''
        def func(model, path, iter, displayedConflicts):
            for dp in [c.GetDataPath() for c in displayedConflicts]:
                found = True
                if len(path) == len(dp):
            
                    for i,x in enumerate(path):
                        it = model.get_iter(path[0:i+1])
                        value = model.get_value(it, 0)
                        if str(value) != str(dp[i]):
                            found = False
                            break
                else:
                    found = False 
                
                if found:
                    iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"conflict.png")
                    icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                
                    model.set_value(iter, 3, icon)
        
        if self.conflicts is not None:
            displayedConflicts = []
            for c in self.conflicts:
                if c.GetElement() == self.objectNew or c.GetElement() == self.objectOld:
                    displayedConflicts.append(c)
            
            self.model.foreach(func, displayedConflicts)

    def __ShowData(self, obj, action = None):
        '''
        Shows data of given object
        @type obj: CBase
        @param obj: object whose data will be displayed
        @type action: EDiffActions
        @param action: Diff action to be displayed
        '''
        icon = None
        if action is not None:
            if action == EDiffActions.INSERT:
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert.png")
            
            elif action == EDiffActions.DELETE:
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete.png")
                
            icon = gtk.gdk.pixbuf_new_from_file(iconfile)
        
        self.__Append(obj.GetData(), None, icon, None, None)
        
    def __Append(self, data, iter = None, icon = None, conflictIcon = None, diff=None):
        '''
        Appends data to model recursively
        @type data: list or tuple
        @param data: data to be appended
        @type iter: gtk.TreeIter
        @param iter: parent iter under which data will be appended
        @type icon: gtk.gdk.Pixbuf
        @param icon: icon to be displayed
        @type conflictIcon: gtk.gdk.Pixbuf
        @param conflictIcon: conflict icon to be displayed or None
        @type diff: CDiffResult
        @param diff: diff that will be associated with data
        '''
        if type(data) == type({}):
            for k,v in data.items():
                if type(v) == type([]):
                    it = self.model.append(iter, [k, None, icon, conflictIcon, diff])
                    for i,d in enumerate(v):
                        self.__Append({i:d}, it, icon, conflictIcon, diff)
                elif type(v) == type({}):
                    it = self.model.append(iter, [k, None, icon, conflictIcon, diff])
                    self.__Append(v, it, icon, conflictIcon)
                else:
                    self.model.append(iter, [k,v,icon, conflictIcon, diff])
                    
        elif type(data) == type([]):
            for i,d in enumerate(data):
                self.__Append({i:d}, iter, icon, conflictIcon, diff)
            
            
    def __ShowDiffs(self):
        '''
        Shows all diffs
        '''
        diffs = self.differ.GetDataDiff().get(EDiffActions.MODIFY,[])
        # vyber iba diffy, ktore sa tykaju tychto elementov
        diffs = [d for d in diffs if d.GetElement() == (self.objectOld or self.objectNew)]
        for diff in diffs:
            if diff.GetPreviousState() is None:
                self.__DataDiffInsert(diff)
            elif diff.GetNewState() is None:
                self.__DataDiffDelete(diff)
            else:
                self.__DataDiffModify(diff)
            
    def __DataDiffInsert(self, diff):
        '''
        Shows insert data diff
        @type diff: CDiffResult
        @param diff: diff
        '''
        def func(model, path, iter, diff):
            found = True
            if len(path) == len(diff.GetDataPath()):
                
                for i,x in enumerate(path):
                    it = model.get_iter(path[0:i+1])
                    value = model.get_value(it, 0)
                    if str(value) != str(diff.GetDataPath()[i]):
                        found = False
                        break
            else:
                found = False 
            if found:
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"insert.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                if type(diff.GetNewState()) == type([]):
                    self.__Append(diff.GetNewState(), iter, icon)
                else:
                    self.__Append({model.iter_n_children(iter):diff.GetNewState()}, iter, icon, None, diff)
                    
                self.__MarkParentAsModified(model.get_path(iter), True)
                return True
                
        
        self.model.foreach(func, diff)
        
    def __DataDiffDelete(self, diff):
        '''
        Shows delete data diff
        @type diff: CDiffResult
        @param diff: diff
        '''
        def func(model, path, iter, diff):
            
            # zobrazi aj vsetkym potomkom delete
            def func2(model, path, iter, subpath):
                if path[0:len(subpath)] == subpath:
                    model.set_value(iter, 2, icon)
            
            
            
            
            
            found = True
            
            
            if len(path) == len(diff.GetDataPath()):
                for i,x in enumerate(path):
            
                    it = model.get_iter(path[0:i+1])
                    value = model.get_value(it, 0)
            
                    if str(value) != str(diff.GetDataPath()[i]):
                        found = False
                        break
            else:
                found = False 
            if found:
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"delete.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                # nasiel som parenta
                r = self.objectOld.GetData()
                for item in diff.GetDataPath()[0:len(diff.GetDataPath())]:
                    r = r[item]
            
                index = r.index(diff.GetPreviousState())
            
                
                it = model.iter_nth_child(iter, index)
            
                model.set_value(it, 2, icon)
                model.set_value(it, 4, diff)
                
                self.__MarkParentAsModified(model.get_path(it))
                
                model.foreach(func2, model.get_path(it))
                
                
                
                return True
        
        
        
        
        self.model.foreach(func, diff)
        
        
    def __DataDiffModify(self, diff):
        '''
        Shows modify data diff
        @type diff: CDiffResult
        @param diff: diff
        '''
        def func(model, path, iter, diff):
            found = True
            
            
            if len(path) == len(diff.GetDataPath()):
                for i,x in enumerate(path):
            
                    it = model.get_iter(path[0:i+1])
                    value = model.get_value(it, 0)
            
                    if str(value) != str(diff.GetDataPath()[i]):
                        found = False
                        break
            else:
                found = False 
            if found:
                iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"modify.png")
                icon = gtk.gdk.pixbuf_new_from_file(iconfile)
                model.set_value(iter, 1, diff.GetNewState().values()[0])
                model.set_value(iter, 2, icon)
                model.set_value(iter, 4, diff)
                self.__MarkParentAsModified(model.get_path(iter))
        
        print diff
        self.model.foreach(func, diff)    
        
        
        
        
        
    def __MarkParentAsModified(self, path, include = False):
        '''
        Marks parent of any diff as modified
        @type path: tuple
        @param path: path with diff
        @type include: bool
        @param include: True if path should be marked too, False otherwise
        '''
        if include == False:
            path = path[0:-1]
        for i,x in enumerate(path):
            newpath = path[0:i+1]
            newiter = self.model.get_iter(newpath)
            iconfile = os.path.join(os.path.dirname(__file__),'..','icons' ,"modify.png")
            icon = gtk.gdk.pixbuf_new_from_file(iconfile)
            self.model.set_value(newiter, 2, icon)
    
        
        
        