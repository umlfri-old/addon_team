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
        if response == 0:
            buf = text.get_buffer()
            (start,end) = buf.get_bounds()
            return buf.get_text(start, end)
        else:
            return None
        wid.hide()
        
    
    def quit(self, widget, data = None):
#        widget.hide()
        return True