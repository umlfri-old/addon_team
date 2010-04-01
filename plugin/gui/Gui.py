'''
Created on 28.3.2010

@author: Peterko
'''

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import pygtk

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
        for res in results.values():
            for r in res:
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
        
        
        
    def quit(self, widget, data = None):
#        widget.hide()
        return True