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
        
        
        #pockaj, kym sa nacita projekt
        while not self.__canRunPlugin():
            time.sleep(5)
        # vyber implementaciu (svn, cvs, git, z dostupnych pluginov)
        self.interface.StartAutocommit()
        self.gui = Gui()
        self.implementation = self.__chooseCorrectImplementation()
        try:
            # add menu
            self.interface.GetAdapter().GetMainMenu().AddMenuItem(None, (len(self.interface.GetAdapter().GetMainMenu().GetItems())-1),'Team',None,None)
            
            #position in menu
            self.mp = (len(self.interface.GetAdapter().GetMainMenu().GetItems())-2)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].AddSubmenu()                    
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddMenuItem(self.DiffProject,0,'Diff project',None,None)
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddMenuItem(self.Update,1,'Update',None,None)
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddMenuItem(self.Checkin,2,'Checkin',None,None)
#            
        except PluginInvalidParameter:
            pass
        
    def __canRunPlugin(self):
        p = self.__LoadProject()
        if p is None:
            return False
        else:
            return not is_zipfile(p.GetFileName())
        
    def __chooseCorrectImplementation(self):
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
    
    
    def DiffProject(self, *args):
        
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        
        myProject1 = CProject(project)
        fileData = self.implementation.GetFileData()
        myProject2 = CProject(None, fileData)
        
        differ = CDiffer(myProject2, myProject1)
        res = differ.diffProjects()
        for dr in res.values():
            for d in dr:
                self.interface.DisplayWarning(d)
        
            
                
    def DiffDiagram(self, *args):
        pass
        
    def DiffElement(self, *args):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        fileData = self.implementation.GetFileData()
        myProject1 = CProject(project)
        myProject2 = CProject(None, fileData)
        
        
          
        
        differ = CDiffer(myProject2, myProject1)
        diag = self.interface.GetAdapter().GetCurrentDiagram()
        selected = diag.GetSelected()
        for sel in selected:
            elView1 = myProject1.GetById(diag.GetId()).GetViewById(sel.GetObject().GetId())
            elView2 = myProject2.GetById(diag.GetId()).GetViewById(sel.GetObject().GetId())
            res = differ.diffElementsVisual(elView2, elView1)
            for dr in res:
                self.interface.DisplayWarning(dr)
        
    def DiffProjectTree(self, *args):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        fileData = self.implementation.GetFileData()
        
        myProject1 = CProject(project)
        myProject2 = CProject(None, fileData)
        
        
          
        
        differ = CDiffer(myProject2, myProject1)
        res = differ.diffProjectTree()
        for dr in res:
            self.interface.DisplayWarning(dr)
            
    def Update(self, *args):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        
        self.implementation.Update()
#        wcProject = CProject(project)
#        fileData = self.implementation.GetFileData()
#        coProject = CProject(None, fileData)
#        fileData2 = self.implementation.GetFileData2()
#        upProject = CProject(None, fileData2)
#        updater = CUpdater(coProject, wcProject, upProject)
    
    def Checkin(self, *args):
        project = self.__LoadProject()
        if project is None:
            self.interface.DisplayWarning('No project loaded')
            return
        msg = self.gui.CheckinMessageDialog()
        if msg is not None:
            self.implementation.Checkin(msg)
        
            
# select plugin main object
pluginMain = Plugin