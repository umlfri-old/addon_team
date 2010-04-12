'''
Created on 28.3.2010

@author: Peterko
'''

from lib.Depend.gtk2 import gtk, gobject
from lib.Depend.gtk2 import pygtk
from lib.consts import PROJECT_CLEARXML_EXTENSION
from support import CConflictSolver

class Gui(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.__conflictSolver = None
        #print 'constructing'
        self.wTree = gtk.Builder()
        self.wTree.add_from_file( "./share/addons/team/plugin/Gui/gui.glade" )
        
        dic = { 
            'on_accept_mine_btn_clicked': self.on_accept_mine_btn_clicked,
            'on_accept_theirs_btn_clicked': self.on_accept_theirs_btn_clicked,
            'on_revisionTxt_grab_focus': self.on_revisionTxt_grab_focus
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
        
        
    
    def DiffResultsDialog(self, results):
        wid = self.wTree.get_object('diffResultsDlg')

        diffsListStore = self.wTree.get_object('diffsListStore')
        diffsListStore.clear()
        for diff in results:
            diffsListStore.append([str(diff)])
        response = wid.run()
        
        wid.hide()
        
        
    def ConflictSolvingDialog(self, conflictSolver):
        self.__conflictSolver = conflictSolver
        wid = self.wTree.get_object('conflictSolvingDlg')
        self.__UpdateConflictsTreeView()
        while 1:
            response = wid.run()
            if response == 0:
                if len(self.__conflictSolver.GetUnresolvedConflicts()) > 0:
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
    
    
    def on_accept_mine_btn_clicked(self, arg):
        self.__AcceptChanges(CConflictSolver.ACCEPT_MINE)
                
    def on_accept_theirs_btn_clicked(self, arg):
        self.__AcceptChanges(CConflictSolver.ACCEPT_THEIRS)
    
    def on_revisionTxt_grab_focus(self, arg):
        print 'grab focus'
        radio  = self.wTree.get_object('specifyRevisionRadioBtn')
        radio.set_active(True)
    
    def __AcceptChanges(self, solution):
        if self.__conflictSolver is not None:
            conflictsTreeView = self.wTree.get_object('conflictsTreeView')
            treeselection = conflictsTreeView.get_selection()
            (model, iter) = treeselection.get_selected()
            if iter is not None:
                conflict = model.get_value(iter, 1)
                self.__conflictSolver.ResolveConflict(conflict, solution)
                self.__UpdateConflictsTreeView()
                
    def __UpdateConflictsTreeView(self):
        if self.__conflictSolver is not None:
            conflictsListStore = self.wTree.get_object('conflictsListStore')
            conflictsListStore.clear()
            
            for conflict in self.__conflictSolver.GetUnresolvedConflicts():
                conflictsListStore.append([str(conflict), conflict])
    
    def ShowError(self, parent, message):
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()