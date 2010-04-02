'''
Created on 28.3.2010

@author: Peterko
'''

from lib.Depend.gtk2 import gtk
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
        
    def CheckoutDialog(self):
        wid = self.wTree.get_widget('checkoutDlg')
        response = wid.run()
        wid.hide()
        if response == 0:
            url = self.wTree.get_widget('checkoutRepoTxt').get_text()
            directory = self.wTree.get_widget('checkoutDirChooser').get_filename()
            checkRevision = self.wTree.get_widget('specifyRevisionCheck').get_active()
            if checkRevision:
                revision = self.wTree.get_widget('checkoutRevisionTxt').get_text()
            else:
                revision = None
            return (url, directory, revision)
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
        if response == gtk.RESPONSE_OK:
            result = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            result = None
        dialog.destroy()
        return result