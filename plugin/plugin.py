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
        self.pluginAdapter = self.interface.GetAdapter()
        self.pluginGuiManager = self.pluginAdapter.GetGuiManager()
        
        self.gui = Gui()
        
        
        
        self.interface.StartAutocommit()
        self.pluginAdapter.AddNotification('project-opened', self.ProjectOpened)
        
        try:
            # add menu
            
            self.teamMenuRoot = self.pluginGuiManager.GetMainMenu().AddMenuItem(str(uuid.uuid1()) ,None, -2,'Team',None,None)
            
            
            
            #add submenu
            self.teamMenuRoot.AddSubmenu()
            self.teamMenuSubmenu = self.teamMenuRoot.GetSubmenu()
            
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.DiffProject,0,'Diff project',None,None)
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Update,1,'Update',None,None)
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkin,2,'Checkin',None,None)
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Revert,3,'Revert',None,None)                    
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.SolveConflicts ,4,'Solve conflicts',None,None)
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkout,5,'Checkout',None,None)
            self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.ShowLogs,6,'Show logs',None,None)
            
            self.ProjectOpened()
                    
            
        except PluginInvalidParameter:
            pass
        
      
      
    def ProjectOpened(self):
        #self.pluginAdapter = self.interface.GetAdapter()
        #self.pluginGuiManager = self.pluginAdapter.GetGuiManager()
        if self.__CanRunPlugin():
            fileName = self.__LoadProject().GetFileName()
            # vyber implementaciu (svn, cvs, git, z dostupnych pluginov)
            self.implementation = self.__ChooseCorrectImplementation(fileName)
  
      
          
    def __CanRunPlugin(self):
        p = self.__LoadProject()
        if p is None:
            return False
        elif p.GetFileName() is None:
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
        return self.pluginAdapter.GetProject()
    
    
    def DiffProject(self, arg):
        
        project = self.__LoadProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
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
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        mine, base, upd = self.implementation.BeforeUpdate()
        updater = CUpdater(mine, base, upd, self.implementation.GetFileName())
        
        
        
        newFileData = updater.GetNewXml()
        #print newFileData
        
        rev = self.implementation.Update(newFileData)
        self.pluginAdapter.LoadProject(self.implementation.GetFileName())
        
        if updater.GetConflictFileName() is not None:
            triple = self.GetProjectConflictingTriple(updater.GetConflictFileName())
            self.SolveConflictTriple(triple)
        else:
            self.pluginGuiManager.DisplayWarning('Updated to revision: '+str(rev))
    
    def Checkin(self, arg):
        project = self.__LoadProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        if self.GetProjectConflictingTriple(self.implementation.GetFileName()) is not None:
            self.pluginGuiManager.DisplayWarning('Unable to checkin: Project remains in conflict')
        else:
            msg = self.gui.CheckinMessageDialog()
            if msg is not None:
                result, rev = self.implementation.Checkin(msg)
                if result=='ok':
                    self.pluginGuiManager.DisplayWarning('Checked in revision: '+str(rev))
                else:
                    self.pluginGuiManager.DisplayWarning(str(rev))
            
    def Revert(self, arg):
        project = self.__LoadProject()
        if project is None:
            self.interface.GetAdapter().DisplayWarning('No project loaded')
            return
        
        
        self.implementation.Revert()
        self.pluginAdapter.LoadProject(self.implementation.GetFileName())
        
        
    def Checkout(self, arg):
        # najdi vsetky implementacie
        impls = []
        for name in dir(implementation):
            obj = getattr(implementation, name)
            if inspect.isclass(obj):
                impls.append(obj)
        
        # otvor checkout dialog
        result = self.gui.CheckoutDialog(impls)
        if result is not None:
            # vyber implementaciu
            self.implementation = result[0]
            # sprav checkout
            self.implementation.Checkout(result[1], result[2], result[3])
            
            
    def SolveConflicts(self, arg):
        prFile = self.gui.OpenConflictProjectDialog()
        if prFile is not None:
            self.implementation = self.__ChooseCorrectImplementation(prFile)
            triple = self.GetProjectConflictingTriple(prFile)
            self.SolveConflictTriple(triple)
                
     
    def ShowLogs(self, arg):
        pass
        
        
    def SolveConflictTriple(self, triple):    
        if triple is not None:
            newProject = CProject(None, triple[0])
            oldProject = CProject(None, triple[1])
            workProject = CProject(None, triple[2])
            conflicter = CConflicter(newProject, oldProject, workProject)
            self.gui.ConflictSolvingDialog(conflicter.merging, conflicter.conflicting)
                
    def GetProjectConflictingTriple(self, fileName):
        conflictNewFileName = fileName+'.frinew'
        conflictOldFileName = fileName+'.fribase'
        conflictWorkFileName = fileName+'.friwork'
        if os.path.isfile(conflictNewFileName) and os.path.isfile(conflictOldFileName) and os.path.isfile(conflictWorkFileName):
            result = (open(conflictNewFileName).read(), open(conflictOldFileName).read(), open(conflictWorkFileName).read())
        else:
            result = None
        return result
    
    
# select plugin main object
pluginMain = Plugin