'''
Created on 28.3.2010

@author: Peterko
'''

from lib.Depend.gtk2 import gtk, gobject
from lib.Depend.gtk2 import pygtk
from lib.consts import PROJECT_CLEARXML_EXTENSION

class Gui(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #print 'constructing'
        self.wTree = gtk.Builder()
        self.wTree.add_from_file( "./share/addons/team/plugin/Gui/gui.glade" )
        
        dic = { 
            
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
        
        
    def ConflictSolvingDialog(self, merging, conflicts):
        wid = self.wTree.get_object('conflictSolvingDlg')
        conflictsListStore = self.wTree.get_object('conflictsListStore')
        conflictsListStore.clear()
        
        for conflict in conflicts:
            conflictsListStore.append([str(conflict)])
        response = wid.run()
        wid.hide()
            
    def CheckoutDialog(self, implementations):
        wid = self.wTree.get_object('checkoutDlg')
        implComboBox = self.wTree.get_object('implementationComboBox')
        
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
        for impl in implementations:
            model.append([impl.description, impl])
        
        
        implComboBox.set_model(model)
        
        cell = gtk.CellRendererText()
        implComboBox.pack_start(cell)
        implComboBox.add_attribute(cell,'text',0)
        implComboBox.set_active(0)
        
        
        response = wid.run()
        wid.hide()
        if response == 0:
            impl = model[implComboBox.get_active()][1]
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


#        filter = gtk.FileFilter()
#        filter.set_name("UML .FRI Clear XML Projects")
#        filter.add_pattern('*'+PROJECT_CLEARXML_EXTENSION)
#        dialog.add_filter(filter)
        
        
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