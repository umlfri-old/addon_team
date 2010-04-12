'''
Created on 28.3.2010

@author: Peterko
'''

from lib.Depend.gtk2 import gtk, cairo
from lib.Depend.gtk2 import pygtk
from lib.consts import PROJECT_CLEARXML_EXTENSION
from support import CConflictSolver
from structure import *
import math
from DiffDrawing import CDiffDrawing

class Gui(object):
    '''
    classdocs
    '''
    

    def __init__(self, plugin):
        '''
        Constructor
        '''
        self.plugin = plugin
        #print 'constructing'
        self.wTree = gtk.Builder()
        self.wTree.add_from_file( "./share/addons/team/plugin/Gui/gui.glade" )
        
        dic = { 
            
            'on_revisionTxt_grab_focus': self.on_revisionTxt_grab_focus,
            'on_logsTreeView_button_press_event' : self.on_logsTreeView_button_press_event,
            'on_diffRevisionsMenu_activate' : self.on_diffRevisionsMenu_activate
        }
        
        self.wTree.connect_signals( dic )
        
        #gtk.main()


    def CheckinMessageDialog(self):
        wid = self.wTree.get_object('checkinMessageDlg')
        text = self.wTree.get_object('checkinMessageTxt')
        buf = text.get_buffer()
        buf.set_text('<Checkin message>')
        response = wid.run()
        wid.hide()
        if response == 0:
            buf = text.get_buffer()
            (start,end) = buf.get_bounds()
            return buf.get_text(start, end)
        else:
            return None
        
        
    
    def DiffResultsDialog(self, results, projectNew, projectOld):
        wid = self.wTree.get_object('diffResultsDlg')

#        diffsListStore = self.wTree.get_object('diffsListStore')
#        diffsListStore.clear()
#        for diff in results:
#            diffsListStore.append([str(diff)])

        self.__UpdateProjectTreeDiffTreeStore(results, projectNew, projectOld)
        response = wid.run()
        wid.hide()
    
    def __UpdateDiagramDiffDrawingArea(self, newDiagram, oldDiagram, results):
        area = self.wTree.get_object('diagramDiffDrawingArea')
        diffDrawing = CDiffDrawing(newDiagram, oldDiagram, results)
        print 'updating diagram diff'
        diffDrawing.Paint(area)
        area.connect('configure-event', self.drawingareaconfigure, diffDrawing)
        area.connect('expose-event', self.drawingareaexpose, diffDrawing)
    
    def __UpdateProjectTreeDiffTreeStore(self, results, projectNew, projectOld):
        oldTreeRoot = projectOld.GetProjectTreeRoot()
        newTreeRoot = projectNew.GetProjectTreeRoot()
        treeModel = self.wTree.get_object('projectTreeTreeStore')
        treeModel.clear()
        self.__InsertNodes(oldTreeRoot, treeModel, None)
        self.__InsertNodes(newTreeRoot, treeModel, None)
        self.wTree.get_object('projectTreeTreeView').connect('cursor-changed', self.on_project_tree_view_cursor_changed, projectNew, projectOld, results)
        
        
    def __InsertNodes(self, node, model, iter):
        iter = model.append(iter, [node.GetObject().GetName(), node])
        for child in node.GetChildsOrdered():
            self.__InsertNodes(child, model, iter)
            
    def on_project_tree_view_cursor_changed(self, treeView, projectNew, projectOld, results):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        node = model.get_value(iter, 1)
        print 'cursor changed'
        if isinstance(node.GetObject(), CDiagram):
            
            newDiagram = projectNew.GetById(node.GetId())
            
            oldDiagram = projectOld.GetById(node.GetId())
            
            self.__UpdateDiagramDiffDrawingArea(newDiagram, oldDiagram, results)
    
    def drawingareaconfigure(self, widget, event, diffDrawing):
        print 'drawin area configure'
        diffDrawing.Paint(widget)
        return True
    
    def drawingareaexpose(self, widget, event, diffDrawing):
        print 'drawin area expose'
        diffDrawing.Paint(widget)
        return False
    
    def __draw(self, widget, context):
        rect = widget.get_allocation()
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        
        radius = min(rect.width / 2, rect.height / 2) - 5
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.stroke()
        
    def ConflictSolvingDialog(self, conflictSolver):
        wid = self.wTree.get_object('conflictSolvingDlg')
        self.__UpdateConflictsTreeView(conflictSolver)
        self.wTree.get_object('acceptMineBtn').connect('clicked', self.on_accept_mine_btn_clicked, conflictSolver)
        self.wTree.get_object('acceptTheirsBtn').connect('clicked', self.on_accept_theirs_btn_clicked, conflictSolver)
        while 1:
            response = wid.run()
            if response == 0:
                if len(conflictSolver.GetUnresolvedConflicts()) > 0:
                    self.ShowError(wid, 'You must resolve all conflicts')
                else:
                    wid.hide()
                    return True
                    
            else:
                wid.hide()
                return False
    
    
            
    def CheckoutDialog(self, implementations):
        wid = self.wTree.get_object('checkoutDlg')
        implementationListStore = self.wTree.get_object('implementationListStore')
        implementationListStore.clear()
        for impl in implementations:
            implementationListStore.append([impl.description])
        implComboBox = self.wTree.get_object('implementationComboBox')

        
        
        response = wid.run()
        wid.hide()
        if response == 0:
            impl = implementations[implComboBox.get_active()]
            url = self.wTree.get_object('checkoutRepoTxt').get_text()
            directory = self.wTree.get_object('checkoutDirChooser').get_filename()
            checkRevision = self.wTree.get_object('specifyRevisionCheck').get_active()
            if checkRevision:
                revision = self.wTree.get_object('checkoutRevisionTxt').get_text()
            else:
                revision = None
            return (impl, url, directory, revision)
        else:
            return None
        
    def OpenConflictProjectDialog(self):
        dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)


        filter = gtk.FileFilter()
        filter.set_name("UML .FRI Clear XML Projects")
        filter.add_pattern('*'+PROJECT_CLEARXML_EXTENSION)
        dialog.add_filter(filter)
        
        
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        
        
        response = dialog.run()
        result = None
        if response == gtk.RESPONSE_OK:
            result = dialog.get_filename()
        
        dialog.destroy()
        return result
    
    def ChooseRevisionDialog(self):
        wid = self.wTree.get_object('chooseRevisionDlg')
        response = wid.run()
        wid.hide()
        if response == 0:
            specifyRevision = self.wTree.get_object('specifyRevisionRadioBtn').get_active()
            if specifyRevision:
                revision = self.wTree.get_object('revisionTxt').get_text()
            else:
                revision = 'HEAD'
            return revision
        else:
            return None
    
    def AuthDialog(self):
        wid = self.wTree.get_object('authDlg')
        response = wid.run()
        wid.hide()
        if response == 0:
            username = self.wTree.get_object('usernameTxt').get_text()
            password = self.wTree.get_object('passwordTxt').get_text()
            return username, password
        else:
            return None, None
    
    def LogsDialog(self, logs):
        wid = self.wTree.get_object('logsDlg')
        logsListStore = self.wTree.get_object('logsListStore')
        logsListStore.clear()
        logsTreeView = self.wTree.get_object('logsTreeView')
        logsTreeView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        for log in logs:
            logsListStore.append([log['revision'], log['author'], log['date'], log['message']])
        response = wid.run()
        wid.hide()
    
    
    def on_accept_mine_btn_clicked(self, wid, conflictSolver):
        print 'accepting mine'
        self.__AcceptChanges(CConflictSolver.ACCEPT_MINE, conflictSolver)
                
    def on_accept_theirs_btn_clicked(self, wid, conflictSolver):
        print 'acceptin theirs'
        self.__AcceptChanges(CConflictSolver.ACCEPT_THEIRS, conflictSolver)
    
    def on_revisionTxt_grab_focus(self, arg):
        print 'grab focus'
        radio  = self.wTree.get_object('specifyRevisionRadioBtn')
        radio.set_active(True)
    
    def on_logsTreeView_button_press_event(self, widget, event):
        if event.button == 3:
            logsPopupMenu = self.wTree.get_object('logsPopupMenu')
            logsPopupMenu.popup(None, None, None, event.button, event.time, None)
            return True
    
    def on_diffRevisionsMenu_activate(self, arg):
        logsTreeView = self.wTree.get_object('logsTreeView')
        selection = logsTreeView.get_selection()
        (model, pathlist) = selection.get_selected_rows()
        if len(pathlist) == 2:
            iter1 = model.get_iter(pathlist[0])
            iter2 = model.get_iter(pathlist[1])
            rev1 = model.get_value(iter1, 0)
            rev2 = model.get_value(iter2, 0)
            
            project1 = self.plugin.LoadProject(rev1)
            project2 = self.plugin.LoadProject(rev2)
            self.plugin.DiffProjects(project1, project2)
        
    
    def __AcceptChanges(self, solution, conflictSolver):
        if conflictSolver is not None:
            conflictsTreeView = self.wTree.get_object('conflictsTreeView')
            treeselection = conflictsTreeView.get_selection()
            (model, iter) = treeselection.get_selected()
            if iter is not None:
                conflict = model.get_value(iter, 1)
                conflictSolver.ResolveConflict(conflict, solution)
                self.__UpdateConflictsTreeView(conflictSolver)
                
    def __UpdateConflictsTreeView(self, conflictSolver):
        if conflictSolver is not None:
            conflictsListStore = self.wTree.get_object('conflictsListStore')
            conflictsListStore.clear()
            
            for conflict in conflictSolver.GetUnresolvedConflicts():
                conflictsListStore.append([str(conflict), conflict])
    
    def ShowError(self, parent, message):
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()