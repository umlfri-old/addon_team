'''
Created on 27.2.2010

@author: Peterko
'''

from lib.Addons.Plugin.Client.Interface import CInterface
from gui import Gui
import os
from structure import *
from support import *
from zipfile import is_zipfile
import implementation
import inspect
import uuid
import time
from teamExceptions import *

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
        
        
        self.implementation = None
        
        self.gui = Gui(self)
        
        
        
        self.interface.StartAutocommit()
        self.pluginAdapter.AddNotification('project-opened', self.ProjectOpened)
        
        
        # add menu
        
        self.teamMenuRoot = self.pluginGuiManager.GetMainMenu().AddMenuItem(str(uuid.uuid1()) ,None, -2,'Team',None,None)
        
        
        
        #add submenu
        self.teamMenuRoot.AddSubmenu()
        self.teamMenuSubmenu = self.teamMenuRoot.GetSubmenu()
        
        self.diffMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.DiffProject,0,'Diff project',None,None)
        
        
        self.updateMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Update,1,'Update',None,None)
        
        
        self.checkinMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkin,2,'Checkin',None,None)
        
        
        self.revertMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Revert,3,'Revert',None,None)
        
                            
        self.solveConflictsMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.SolveConflicts ,4,'Solve conflicts',None,None)
        
        
        self.checkoutMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkout,5,'Checkout',None,None)
        
        
        self.logsMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.ShowLogs,6,'Show logs',None,None)
        
        
        self.ProjectOpened()
                    
       
        
      
      
    def ProjectOpened(self):

        if self.__CanRunPlugin():
            fileName = self.__LoadApplicationProject().GetFileName()
            # vyber implementaciu (svn, cvs, git, z dostupnych pluginov)
            self.implementation = self.__ChooseCorrectImplementation(fileName)
            
            self.diffMenu.SetSensitive('diff' in self.implementation.supported)
            self.updateMenu.SetSensitive('update' in self.implementation.supported)
            self.checkinMenu.SetSensitive('checkin' in self.implementation.supported)
            self.revertMenu.SetSensitive('revert' in self.implementation.supported)
            self.logsMenu.SetSensitive('log' in self.implementation.supported)
        else:
            self.__ResetMenuSensitivity()
    
    def __ResetMenuSensitivity(self):
        self.diffMenu.SetSensitive(False)
        self.updateMenu.SetSensitive(False)
        self.checkinMenu.SetSensitive(False)
        self.revertMenu.SetSensitive(False)
        self.solveConflictsMenu.SetSensitive(True)
        self.checkoutMenu.SetSensitive(True)
        self.logsMenu.SetSensitive(False)
        
    def __CanRunPlugin(self):
        p = self.__LoadApplicationProject()
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
    
    
    def __LoadApplicationProject(self):
        '''
        Load project
        '''
        return self.pluginAdapter.GetProject()
    
    
    def DiffProject(self, arg):
        
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        
        myProject1 = CProject(project)
        fileData = self.implementation.GetFileData()
        myProject2 = CProject(None, fileData)
        
        self.DiffProjects(myProject1, myProject2)
        
#       

    def LoadProject(self, rev = None):
        data = self.implementation.GetFileData(rev)
        project = CProject(None, data)
        return project

    def DiffProjects(self, project1, project2):
        differ = CDiffer(project2, project1)
        res = differ.projectTreeDiff + differ.visualDiff + differ.dataDiff
        print 'DIFFFFFFFFFS'
        for r in res:
            print r
        print '------------'
        self.gui.DiffResultsDialog(differ)
            
    def Update(self, arg):
        project = self.__LoadApplicationProject()
        
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        
        updateToRevision = self.gui.ChooseRevisionDialog()
        if updateToRevision is not None:
            if updateToRevision == 'HEAD':
                revision = None
            else:
                revision = updateToRevision
                
            mine, base, upd = self.implementation.BeforeUpdate(revision)
            updater = CUpdater(mine, base, upd, self.implementation.GetFileName())
            
            
            
            
            
            
            newFileData = updater.GetNewXml()
            rev = self.implementation.Update(newFileData, revision)
            self.pluginAdapter.LoadProject(self.implementation.GetFileName())
            
            if updater.GetConflictFileName() is not None:
                
                self.SolveConflicts(arg, self.implementation.GetFileName())
                
            else:
                
                self.pluginGuiManager.DisplayWarning('Updated to revision: '+str(rev))
    
    def Checkin(self, arg):
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        if self.GetProjectConflictingTriple(self.implementation.GetFileName()) is not None:
            self.pluginGuiManager.DisplayWarning('Unable to checkin: Project remains in conflict')
        else:
            msg = self.gui.CheckinMessageDialog()
            result = self.__Checkin(msg)
            print 'OUT RESULT',result
            self.pluginGuiManager.DisplayWarning(result)
    
    def __Checkin(self, msg):
        if msg is not None:
            username = None
            password = None
            repeats = 0
            while 1:
                repeats += 1
                try:
                    result = self.implementation.Checkin(msg, username, password)
                    print result
                    return result
                except AuthorizationError, e:
                    if repeats > 3:
                        return 'Authorization failed'
                    username, password = self.gui.AuthDialog()
                    if username is None or password is None:
                        return 'Authorization failed'
                     
            
        else:
            return 'Message cannot be None'
            
                        
            
    def Revert(self, arg):
        project = self.__LoadApplicationProject()
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
                try:
                    if 'checkout' in obj.supported:
                        impls.append(obj)
                except:
                    pass
                        
        
        # otvor checkout dialog
        result = self.gui.CheckoutDialog(impls)
        if result is not None:
            # vyber implementaciu
            self.implementation = result[0]
            # sprav checkout
            result = self.implementation.Checkout(result[1], result[2], result[3])
            self.pluginGuiManager.DisplayWarning(result)
            
            
    def SolveConflicts(self, arg, fileName = None):
        if fileName is None:
            prFile = self.gui.OpenConflictProjectDialog()
        else:
            prFile = fileName
        if prFile is not None:
            
            self.implementation = self.__ChooseCorrectImplementation(prFile)
            
            triple = self.GetProjectConflictingTriple(prFile)
            
            mergedProject = CProject(None, open(prFile).read())
            
            resolved = self.SolveConflictTriple(triple, mergedProject)
            print 'resolved',resolved
            if resolved:
                self.__Resolve(prFile, mergedProject.GetSaveXml())
            else:
                pass
                
                
     
    def ShowLogs(self, arg):
        project = self.__LoadApplicationProject()
        if project is None:
            self.interface.GetAdapter().DisplayWarning('No project loaded')
            return
        
        
        logs = self.implementation.Log()
        self.gui.LogsDialog(logs)
        
        
    def SolveConflictTriple(self, triple, mergedProject):    
        if triple is not None:
            newProject = CProject(None, triple[0])
            oldProject = CProject(None, triple[1])
            workProject = CProject(None, triple[2])
            conflicter = CConflicter(newProject, oldProject, workProject)
            merger = CMerger(mergedProject)
            conflictSolver = CConflictSolver(conflicter.GetConflicting(), merger)
            return self.gui.ConflictSolvingDialog(conflictSolver)
                
    def GetProjectConflictingTriple(self, fileName):
        conflictNewFileName = fileName+'.frinew'
        conflictOldFileName = fileName+'.fribase'
        conflictWorkFileName = fileName+'.friwork'
        if os.path.isfile(conflictNewFileName) and os.path.isfile(conflictOldFileName) and os.path.isfile(conflictWorkFileName):
            result = (open(conflictNewFileName).read(), open(conflictOldFileName).read(), open(conflictWorkFileName).read())
        else:
            result = None
        return result
    
    def __Resolve(self, fileName, content):
        conflictNewFileName = fileName+'.frinew'
        conflictOldFileName = fileName+'.fribase'
        conflictWorkFileName = fileName+'.friwork'
        if os.path.isfile(conflictNewFileName) and os.path.isfile(conflictOldFileName) and os.path.isfile(conflictWorkFileName):
            os.remove(conflictNewFileName)
            os.remove(conflictOldFileName)
            os.remove(conflictWorkFileName)
        f = open(fileName, 'w')
        f.write(content)
        f.close()
        self.pluginAdapter.LoadProject(fileName)
        
# select plugin main object
pluginMain = Plugin