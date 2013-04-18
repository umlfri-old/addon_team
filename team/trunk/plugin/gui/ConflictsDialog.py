'''
Created on 15.4.2010

@author: Peterko
'''
from support import *
from imports.gtk2 import gtk
from DiffDialog import CDiffDialog

class CConflictsDialog:
    '''
    Class representing dialog for conflict solving
    '''


    def __init__(self, wTree):
        '''
        Constructor
        @type wTree: gtk.Builder
        @param wTree: gtk builder with objects needed to construct dialog
        '''
        self.wTree = wTree
        self.conflictSolver = None
        self.baseWorkDiffer = None
        self.baseNewDiffer = None
        self.response = None
        
        
        self.wid = self.wTree.get_object('conflictSolvingDlg')
        
        self.wTree.get_object('acceptMineBtn').connect('clicked', self.on_accept_mine_btn_clicked)
        self.wTree.get_object('acceptTheirsBtn').connect('clicked', self.on_accept_theirs_btn_clicked)
        self.wTree.get_object('showMineDiffBtn').connect('clicked', self.on_show_mine_diff_btn_clicked)
        self.wTree.get_object('showTheirsDiffBtn').connect('clicked', self.on_show_theirs_diff_btn_clicked)
        self.wTree.get_object('showMergedProjectBtn').connect('clicked', self.on_show_merged_project_btn_clicked)
        self.wTree.get_object('conflictsTreeView').connect_after('cursor-changed', self.on_conflicts_tree_view_cursor_changed)
        
    def SetAttributes(self, conflictSolver, baseWorkDiffer, baseNewDiffer, diffDialog):
        '''
        Sets all attributes
        @type conflictSolver: CConflictSolver
        @param conflictSolver: conflict solver
        @type baseWorkDiffer: CDiffer
        @param baseWorkDiffer: differ with diffs from base to work project
        @type baseNewDiffer: CDiffer
        @param baseNewDiffer: differ with diffs from base to new project
        @type diffDialog: CDiffDialog
        @param diffDialog: CDiffDialog instance, will be used for displaying diffs
        '''    
        self.conflictSolver = conflictSolver
        self.baseWorkDiffer = baseWorkDiffer
        self.baseNewDiffer = baseNewDiffer
        self.diffDialog = diffDialog    
        
    
    def Run(self):
        '''
        Runs dialog, sets response
        '''
        self.__UpdateConflictsTreeView()
        while 1:
            response = self.wid.run()
            if response == 0:
                if len(self.conflictSolver.GetUnresolvedConflicts()) > 0:
                    self.ShowError(self.wid, _('You must resolve all conflicts'))
                else:
                    self.wid.hide()
                    self.response = True
                    break
                    
            else:
                self.wid.hide()
                self.response = False
                break
    
    def Response(self):
        '''
        Returns response
        @rtype: bool
        @return: True if dialog was closed with OK, False otherwise 
        '''
        return self.response
    
    def on_show_mine_diff_btn_clicked(self, wid):
        '''
        Shows mine diff
        '''
        
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(self.baseWorkDiffer)
        self.diffDialog.SetConflicts([c.GetBaseWorkDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
        self.diffDialog.Run()
        
    def on_show_theirs_diff_btn_clicked(self, wid):
        '''
        Shows theirs diff
        '''
        
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(self.baseNewDiffer)
        self.diffDialog.SetConflicts([c.GetBaseNewDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
        self.diffDialog.Run()
        
    
    
    def on_show_merged_project_btn_clicked(self, wid):
        '''
        Show merged project
        '''
        falseDiffer = CDiffer(self.conflictSolver.GetMerger().GetProject(), self.conflictSolver.GetMerger().GetProject())
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(falseDiffer)
        self.diffDialog.SetConflicts(None)
        self.diffDialog.Run()
    
    
            
    def on_accept_mine_btn_clicked(self, wid):
        
        self.__AcceptChanges(CConflictSolver.ACCEPT_MINE)
                
    def on_accept_theirs_btn_clicked(self, wid):
        
        self.__AcceptChanges(CConflictSolver.ACCEPT_THEIRS)
        
    def __AcceptChanges(self, solution):
        '''
        Applies conflict resolution for selected conflict
        @type solution: CConflictSolver.resolution
        @param solution: resolution enumeration
        '''
        if self.conflictSolver is not None:

            conflictsTreeView = self.wTree.get_object('conflictsTreeView')
            
            treeselection = conflictsTreeView.get_selection()
            treeselection.set_mode(gtk.SELECTION_SINGLE)
            (model, iter) = treeselection.get_selected()
            if iter is not None:
                conflict = model.get_value(iter, 1)
                self.conflictSolver.ResolveConflict(conflict, solution)

                self.__UpdateConflictsTreeView()
                
                
    def on_conflicts_tree_view_cursor_changed(self, treeView):
        def func(model, path, iter, related):
            if model.get_value(iter, 1) in related:
                treeView.get_selection().select_iter(iter)
        
        
        selection = treeView.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        (model,iter) = selection.get_selected()
        conflict = model.get_value(iter, 1)
        related = self.conflictSolver.FindRelatedConflicts(conflict)
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        
        model.foreach(func, related)
        return False
                
    def __UpdateConflictsTreeView(self):
        '''
        Updates conflicts tree view
        '''
        if self.conflictSolver is not None:
            conflictsListStore = self.wTree.get_object('conflictsListStore')
            conflictsListStore.clear()
            
            for conflict in self.conflictSolver.GetUnresolvedConflicts():
                conflictsListStore.append([str(conflict), conflict])
                
    def ShowError(self, parent, message):
        '''
        Shows error dialog
        @type parent: gtk.Widget
        @param parent: parent widget for error dialog
        @type message: string
        @param message: text message that will be displayed
        '''
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()