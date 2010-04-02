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
from zipfile import is_zipfile
import implementation
import inspect
import uuid
import time

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
        self.interface.GetAdapter().AddNotification('project-opened', self.ProjectOpened)
        
        try:
            # add menu
            
            self.teamMenuRoot = self.interface.GetAdapter().GetMainMenu().AddMenuItem(str(uuid.uuid1()) ,None, -2,'Team',None,None)
            
            
            
            #add submenu
            self.teamMenuRoot.AddSubmenu()
            self.teamMenuSubmenu = self.teamMenuRoot.GetSubmenu()
            #self.teamMenuRoot.GetSubmenu().AddMenuItem(str(uuid.uuid1()),self.Checkout,4,'Checkout',None,None)                    
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()), self.SolveConflicts ,5,'Solve conflicts',None,None)
            
        except PluginInvalidParameter:
            pass
        
      
      
    def ProjectOpened(self):
        
        if self.__CanRunPlugin():
            fileName = self.__LoadProject().GetFileName()
            # vyber implementaciu (svn, cvs, git, z dostupnych pluginov)
            self.implementation = self.__ChooseCorrectImplementation(fileName)
            
            try:
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.DiffProject,0,'Diff project',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Update,1,'Update',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkin,2,'Checkin',None,None)
                self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Revert,3,'Revert',None,None)
            except PluginInvalidParameter:
                pass
  
      
          
    def __CanRunPlugin(self):
        p = self.__LoadProject()
        if p is None:
            return False
        else:
            return not is_zipfile(p.GetFileName())
        
    def __ChooseCorrectImplementation(self, fileName):
        result = None
        # vyber nejaky
        for name in dir(implementation):
            obj = getattr(implementation, name)
            if inspect.isclass(obj):
                r = obj(fileName)
                if r.IsProjectVersioned():
                    return r
        # ak nenajdes, zober dummy implementation
        if result is None:
            
            result = implementation.CDummyImplementation(fileName)
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
        res = differ.projectTreeDiff + differ.visualDiff + differ.dataDiff
        self.gui.DiffResultsDialog(res)
#       
            
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
        prFile = self.gui.OpenConflictProjectDialog()
        if prFile is not None:
            self.implementation = self.__ChooseCorrectImplementation(prFile)
            triple = self.implementation.GetConflictTriple()
            if triple is not None:
                newProject = CProject(None, triple[0])
                oldProject = CProject(None, triple[1])
                workProject = CProject(None, triple[2])
                conflicter = CConflicter(newProject, oldProject, workProject)
                
        
        
# select plugin main object
pluginMain = Plugin