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
        self.wTree = gtk.glade.XML( "./share/addons/team/plugin/Gui/gui.glade" )
        
        dic = { 
            
        }
        
        self.wTree.signal_autoconnect( dic )
        
        #gtk.main()


    def CheckinMessageDialog(self):
        wid = self.wTree.get_widget('checkinMessageDlg')
        text = self.wTree.get_widget('checkinMessageTxt')
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
        wid = self.wTree.get_widget('diffResultsDlg')
        text = self.wTree.get_widget('diffResultsTxt')
        buf = text.get_buffer()
        text = ''
        for r in results:
            text += str(r)+'\n'
        buf.set_text(text)
        response = wid.run()
        
        wid.hide()
        
        
    def ConflictSolvingDialog(self, merging, conflicts):
        wid = self.wTree.get_widget('conflictSolvingDlg')
        text = self.wTree.get_widget('conflictsResultsTxt')
        buf = text.get_buffer()
        text = 'MERGING CHANGES\n'
        for m in merging:
            text += str(m) +'\n'
        text += 'CONFLICTING CHANGES\n'
        for c in conflicts:
            text += str(c) +'\n'
        buf.set_text(text)
        response = wid.run()
        wid.hide()
            
    def CheckoutDialog(self, implementations):
        wid = self.wTree.get_widget('checkoutDlg')
        implComboBox = self.wTree.get_widget('implementationComboBox')
        
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
            url = self.wTree.get_widget('checkoutRepoTxt').get_text()
            directory = self.wTree.get_widget('checkoutDirChooser').get_filename()
            checkRevision = self.wTree.get_widget('specifyRevisionCheck').get_active()
            if checkRevision:
                revision = self.wTree.get_widget('checkoutRevisionTxt').get_text()
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