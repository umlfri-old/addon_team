'''
Created on 28.3.2010

@author: Peterko
'''

from imports.gtk2 import gtk, cairo
from imports.gtk2 import pygtk

from structure import *

import os.path
from DiffDialog import CDiffDialog
from ConflictsDialog import CConflictsDialog

class Gui:
    '''
    Class with graphical user interface
    '''
    

    def __init__(self, plugin):
        '''
        Constructor
        @type plugin: Plugin
        @param plugin: team plugin instance
        '''
        self.plugin = plugin
        
        self.wTree = gtk.Builder()
        gladeFile = os.path.join(os.path.dirname(__file__), "gui.glade")
        self.wTree.add_from_file( gladeFile )
        self.diffDialog = None
        self.conflictSolvingDialog = None
        
        dic = { 
            
            'on_revisionTxt_grab_focus': self.on_revisionTxt_grab_focus,
            'on_logsTreeView_button_press_event' : self.on_logsTreeView_button_press_event,
            'on_diffRevisionsMenu_activate' : self.on_diffRevisionsMenu_activate
        }
        
        
        
        self.wTree.connect_signals( dic )
        


    def CheckinMessageDialog(self):
        '''
        Runs checkin message dialog
        @rtype: string
        @return: message inserted or None
        '''
        wid = self.wTree.get_object('checkinMessageDlg')
        text = self.wTree.get_object('checkinMessageTxt')
        buf = text.get_buffer()
        buf.set_text(_('<Checkin message>'))
        response = wid.run()
        wid.hide()
        if response == 0:
            buf = text.get_buffer()
            (start,end) = buf.get_bounds()
            return buf.get_text(start, end)
        else:
            return None
        
        
    
    def DiffResultsDialog(self, differ):
        '''
        runs diff dialog
        @type differ: CDiffer
        @param differ: differ that holds displayed diffs
        '''
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        self.diffDialog.SetDiffer(differ)
        self.diffDialog.Run()
        
        
    
    
        
    def ConflictSolvingDialog(self, conflictSolver, baseWorkDiffer, baseNewDiffer):
        '''
        Runs conflict solving dialog
        @type conflictSolver: CConflictSolver
        @param conflictSolver: conflict solver instance
        @type baseWorkDiffer: CDiffer
        @param baseWorkDiffer: differ from base to work project
        @type baseNewDiffer: CDiffer
        @param baseNewDiffer: differ from base to new project
        @rtype: bool
        @return: Returns True if dialog was ended with OK, False otherwise
        '''
        if self.diffDialog is None:
            self.diffDialog = CDiffDialog(self.wTree)
        if self.conflictSolvingDialog is None:
            self.conflictSolvingDialog = CConflictsDialog(self.wTree)
        self.conflictSolvingDialog.SetAttributes(conflictSolver, baseWorkDiffer, baseNewDiffer, self.diffDialog)
        self.conflictSolvingDialog.Run()
        return self.conflictSolvingDialog.Response()
    
    
            
    def CheckoutDialog(self, implementations):
        '''
        Runs checkout dialog
        @type implementations: list
        @param implementations: list of description and identification of implementations
        @rtype: tuple
        @return: tuple with (selected implementation id, url of repository, checkout directory, selected revision or None) or None
        '''
        wid = self.wTree.get_object('checkoutDlg')
        implementationListStore = self.wTree.get_object('implementationListStore')
        implementationListStore.clear()
        for ID, desc in implementations.items():
            implementationListStore.append([desc, ID])
        implComboBox = self.wTree.get_object('implementationComboBox')

        
        
        response = wid.run()
        wid.hide()
        if response == 0:
            implId = implementationListStore.get_value(implComboBox.get_active_iter(), 1)
            url = self.wTree.get_object('checkoutRepoTxt').get_text()
            directory = self.wTree.get_object('checkoutDirChooser').get_filename()
            checkRevision = self.wTree.get_object('specifyRevisionCheck').get_active()
            if checkRevision:
                revision = self.wTree.get_object('checkoutRevisionTxt').get_text()
            else:
                revision = None
            return (implId, url, directory, revision)
        else:
            return None
        
    
    def ChooseRevisionDialog(self):
        '''
        Runs dialog for choosing revision
        @rtype: string
        @return: string with chosen revision or None
        '''
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
        '''
        Runs authorization dialog
        @rtype: string, string
        @return: username, password or None, None
        '''
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
        '''
        Runs log dialog
        @type logs: list
        @param logs: Logs to be displayed
        '''
        wid = self.wTree.get_object('logsDlg')
        logsListStore = self.wTree.get_object('logsListStore')
        logsListStore.clear()
        logsTreeView = self.wTree.get_object('logsTreeView')
        logsTreeView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        for log in logs:
            logsListStore.append([log['revision'], log['author'], log['date'], log['message']])
        response = wid.run()
        wid.hide()
    
    
    
    
    def on_revisionTxt_grab_focus(self, arg):
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
            

            self.plugin.DiffRevisions(rev1, rev2)
        
    
    
    
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
        
    def ShowQuestion(self, question):
        '''
        Shows question dialog
        @type question: string
        @param question: question to be displayed
        @rtype: bool
        @return: True if answer is Yes, False otherwise
        '''
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, question)
        response = md.run()
        md.destroy()
        return response == gtk.RESPONSE_YES
    
    