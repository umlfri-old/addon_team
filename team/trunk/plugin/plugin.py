'''
Created on 27.2.2010

@author: Peterko
'''

from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from gui import Gui
import os
from structure import *
from support import *
from zipfile import ZipFile, is_zipfile
import implementation
import time
import inspect
import uuid

class Plugin(object):
    '''
    classdocs
    '''
    
    def __init__(self, interface):
        '''
        Constructor
        '''
        # load interface
        self.interface = interface
        self.interface.SetGtkMainloop()
        
        self.gui = Gui()
        
        
        
#        self.interface.StartAutocommit()
        self.interface.GetAdapter().AddNotification('project-opened', lambda:self.ProjectOpened())
        
        try:
            # add menu
            
            self.teamMenuRoot = self.interface.GetAdapter().GetMainMenu().AddMenuItem(str(uuid.uuid1()) ,None, -2,'Team',None,None)
            
            
            
            #add submenu
            self.teamMenuRoot.AddSubmenu()
            self.teamMenuSubmenu = self.teamMenuRoot.GetSubmenu()
            #self.teamMenuRoot.GetSubmenu().AddMenuItem(str(uuid.uuid1()),self.Checkout,4,'Checkout',None,None)                    
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()), lambda x:self.SolveConflicts(x) ,5,'Solve conflicts',None,None)
            
#            
        except PluginInvalidParameter:
            pass
        
      
      
    def ProjectOpened(self):
        # vyber implementaciu (svn, cvs, git, z dostupnych pluginov)
        if self.__CanRunPlugin():
            
            self.implementation = self.__ChooseCorrectImplementation()
            
            try:
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),lambda x:self.DiffProject(x),0,'Diff project',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),lambda x:self.Update(x),1,'Update',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),lambda x:self.Checkin(x),2,'Checkin',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),lambda x:self.Revert(x),3,'Revert',None,None)
            except PluginInvalidParameter:
                pass
  
      
          
    def __CanRunPlugin(self):
        p = self.__LoadProject()
        if p is None:
            return False
        else:
            return not is_zipfile(p.GetFileName())
        
    def __ChooseCorrectImplementation(self):
        result = None
        # vyber nejaky
        for name in dir(implementation):
            obj = getattr(implementation, name)
            if inspect.isclass(obj):
                r = obj(self.__LoadProject().GetFileName())
                if r.IsProjectVersioned():
                    return r
        # ak nenajdes, zober dummy implementation
        if result is None:
            
            result = implementation.CDummyImplementation(self.__LoadProject().GetFileName())
        return result
    
    
    def __LoadProject(self):
        '''
        Load project
        '''
        return self.interface.GetAdapter().GetProject()
    
    
    def DiffProject(self, arg):
        
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        
        myProject1 = CProject(project)
        fileData = self.implementation.GetFileData()
        myProject2 = CProject(None, fileData)
        
        differ = CDiffer(myProject2, myProject1)
        res = differ.diffProjects()
        self.gui.DiffResultsDialog(res)
#        for dr in res.values():
#            for d in dr:
#                self.interface.DisplayWarning(d)
        
            
                
#    def DiffDiagram(self, *args):
#        pass
#        
#    def DiffElement(self, *args):
#        project = self.__LoadProject()
#        if project is None:
#            self.interface.DisplayWarning('No project loaded')
#            return
#        
#        fileData = self.implementation.GetFileData()
#        myProject1 = CProject(project)
#        myProject2 = CProject(None, fileData)
#        
#        
#          
#        
#        differ = CDiffer(myProject2, myProject1)
#        diag = self.interface.GetAdapter().GetCurrentDiagram()
#        selected = diag.GetSelected()
#        for sel in selected:
#            elView1 = myProject1.GetById(diag.GetId()).GetViewById(sel.GetObject().GetId())
#            elView2 = myProject2.GetById(diag.GetId()).GetViewById(sel.GetObject().GetId())
#            res = differ.diffElementsVisual(elView2, elView1)
#            for dr in res:
#                self.interface.DisplayWarning(dr)
#        
#    def DiffProjectTree(self, *args):
#        project = self.__LoadProject()
#        if project is None:
#            self.interface.DisplayWarning('No project loaded')
#            return
#        
#        fileData = self.implementation.GetFileData()
#        
#        myProject1 = CProject(project)
#        myProject2 = CProject(None, fileData)
#        
#        
#          
#        
#        differ = CDiffer(myProject2, myProject1)
#        res = differ.diffProjectTree()
#        for dr in res:
#            self.interface.DisplayWarning(dr)
            
    def Update(self, arg):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        self.implementation.Update()
    
    def Checkin(self, arg):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        msg = self.gui.CheckinMessageDialog()
        if msg is not None:
            self.implementation.Checkin(msg)
            
    def Revert(self, arg):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        
        self.implementation.Revert()
        
        
    def Checkout(self, arg):
        result = self.gui.CheckoutDialog()
        if result is not None:
            self.implementation.Checkout(result[0], result[1], result[2])
            
            
    def SolveConflicts(self, arg):
        print 'solve conflict'
        print arg
# select plugin main object
pluginMain = Plugin