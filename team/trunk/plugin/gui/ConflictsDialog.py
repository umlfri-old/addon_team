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


    def __init__(self, wTree, conflictSolver, baseWorkDiffer, baseNewDiffer):
        self.wTree = wTree
        self.conflictSolver = conflictSolver
        self.baseWorkDiffer = baseWorkDiffer
        self.baseNewDiffer = baseNewDiffer
        self.response = None
        wid = self.wTree.get_object('conflictSolvingDlg')
        self.__UpdateConflictsTreeView()
        
        id1 = self.wTree.get_object('acceptMineBtn').connect('clicked', self.on_accept_mine_btn_clicked)
        id2 = self.wTree.get_object('acceptTheirsBtn').connect('clicked', self.on_accept_theirs_btn_clicked)
        id3 = self.wTree.get_object('showMineDiffBtn').connect('clicked', self.on_show_mine_diff_btn_clicked)
        id4 = self.wTree.get_object('showTheirsDiffBtn').connect('clicked', self.on_show_theirs_diff_btn_clicked)
        id5 = self.wTree.get_object('showMergedProjectBtn').connect('clicked', self.on_show_merged_project_btn_clicked)
        while 1:
            response = wid.run()
            if response == 0:
                print 'remaining conflicts',len(self.conflictSolver.GetUnresolvedConflicts())
                if len(self.conflictSolver.GetUnresolvedConflicts()) > 0:
                    self.ShowError(wid, 'You must resolve all conflicts')
                else:
                    wid.hide()
                    self.response = True
                    break
                    
            else:
                wid.hide()
                self.response = False
                break
            
        self.wTree.get_object('acceptMineBtn').disconnect(id1)
        self.wTree.get_object('acceptTheirsBtn').disconnect(id2)
        self.wTree.get_object('showMineDiffBtn').disconnect(id3)
        self.wTree.get_object('showTheirsDiffBtn').disconnect(id4)
        self.wTree.get_object('showMergedProjectBtn').disconnect(id5)
   
    def Response(self):
        return self.response
    
    def on_show_mine_diff_btn_clicked(self, wid):
        print 'showing mine diff'
        mineDiff = CDiffDialog(self.wTree, self.baseWorkDiffer, [c.GetBaseWorkDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
        
    def on_show_theirs_diff_btn_clicked(self, wid):
        print 'showing theirs diff'
        theirsDiff = CDiffDialog(self.wTree, self.baseNewDiffer, [c.GetBaseNewDiff() for c in self.conflictSolver.GetUnresolvedConflicts()])
    
    
    def on_show_merged_project_btn_clicked(self, wid):
        falseDiffer = CDiffer(self.conflictSolver.GetMerger().GetProject(), self.conflictSolver.GetMerger().GetProject())
        merged = CDiffDialog(self.wTree, falseDiffer, None)
    
    
            
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