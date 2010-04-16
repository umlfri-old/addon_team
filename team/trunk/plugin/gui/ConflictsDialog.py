'''
Created on 15.4.2010

@author: Peterko
'''
from support import *
from imports.gtk2 import gtk
from DiffDialog import CDiffDialog

class CConflictsDialog(object):
    '''
    classdocs
    '''


    def __init__(self, wTree, conflictSolver, baseWorkDiffer, baseNewDiffer, diffDialog):
        self.wTree = wTree
        self.conflictSolver = conflictSolver
        self.baseWorkDiffer = baseWorkDiffer
        self.baseNewDiffer = baseNewDiffer
        self.response = None
        self.diffDialog = diffDialog
        
        self.wid = self.wTree.get_object('conflictSolvingDlg')
        self.__UpdateConflictsTreeView()
        
        self.wTree.get_object('acceptMineBtn').connect('clicked', self.on_accept_mine_btn_clicked)
        self.wTree.get_object('acceptTheirsBtn').connect('clicked', self.on_accept_theirs_btn_clicked)
        self.wTree.get_object('showMineDiffBtn').connect('clicked', self.on_show_mine_diff_btn_clicked)
        self.wTree.get_object('showTheirsDiffBtn').connect('clicked', self.on_show_theirs_diff_btn_clicked)
        self.wTree.get_object('showMergedProjectBtn').connect('clicked', self.on_show_merged_project_btn_clicked)
        
            
        
    
    def Run(self):
        while 1:
            response = self.wid.run()
            if response == 0:
                print 'remaining conflicts',len(self.conflictSolver.GetUnresolvedConflicts())
                if len(self.conflictSolver.GetUnresolvedConflicts()) > 0:
                    self.ShowError(self.wid, 'You must resolve all conflicts')
                else:
                    self.wid.hide()
                    self.response = True
                    break
                    
            else:
                self.wid.hide()
                self.response = False
                break
    
    def Response(self):
        return self.response
    
    def on_show_mine_diff_btn_clicked(self, wid):
        print 'showing mine diff'
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(self.baseWorkDiffer)
        self.diffDialog.SetConflicts([c.GetBaseWorkDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
        self.diffDialog.Run()
        
    def on_show_theirs_diff_btn_clicked(self, wid):
        print 'showing theirs diff'
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(self.baseNewDiffer)
        self.diffDialog.SetConflicts([c.GetBaseNewDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
        self.diffDialog.Run()
        
    
    
    def on_show_merged_project_btn_clicked(self, wid):
        falseDiffer = CDiffer(self.conflictSolver.GetMerger().GetProject(), self.conflictSolver.GetMerger().GetProject())
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(falseDiffer)
        self.diffDialog.SetConflicts(None)
        self.diffDialog.Run()
    
    
            
    def on_accept_mine_btn_clicked(self, wid):
        print 'accepting mine'
        self.__AcceptChanges(CConflictSolver.ACCEPT_MINE)
                
    def on_accept_theirs_btn_clicked(self, wid):
        print 'acceptin theirs'
        self.__AcceptChanges(CConflictSolver.ACCEPT_THEIRS)
        
    def __AcceptChanges(self, solution):
        if self.conflictSolver is not None:
            print 'BEFORE',len(self.conflictSolver.GetUnresolvedConflicts())
            conflictsTreeView = self.wTree.get_object('conflictsTreeView')
            treeselection = conflictsTreeView.get_selection()
            (model, iter) = treeselection.get_selected()
            if iter is not None:
                conflict = model.get_value(iter, 1)
                self.conflictSolver.ResolveConflict(conflict, solution)
                print 'AFTER',len(self.conflictSolver.GetUnresolvedConflicts())
                self.__UpdateConflictsTreeView()
                
    def __UpdateConflictsTreeView(self):
        if self.conflictSolver is not None:
            conflictsListStore = self.wTree.get_object('conflictsListStore')
            conflictsListStore.clear()
            
            for conflict in self.conflictSolver.GetUnresolvedConflicts():
                conflictsListStore.append([str(conflict), conflict])
                
    def ShowError(self, parent, message):
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()