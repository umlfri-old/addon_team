'''
Created on 27.2.2010

@author: Peterko
'''

from lib.Addons.Plugin.Client.Interface import CInterface
from gui import Gui
import os
from structure import *
from support import *
from zipfile import is_zipfile, ZIP_DEFLATED, ZipFile
import implementation
import inspect
import uuid
import time
from teamExceptions import *
from cStringIO import StringIO

class Plugin(object):
    '''
    classdocs
    '''
    
    incompatibleText = 'Project is under version control, but is incompatible with Team plugin. Would you like to make it compatible? (There will be no physical changes to project file)'
    
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
            
            if self.implementation.IsInConflict():
                self.SolveConflicts(None, fileName)
            
            
            if not self.implementation.IsCompatible():
                response = self.gui.ShowQuestion(self.incompatibleText)
                if response:
                    self.implementation.MakeCompatible()
                else:
                    self.__ResetMenuSensitivity()
            else:
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
            return True
    
    def __SaveProjectXmlToExistingFile(self, xml, fileName):
        if is_zipfile(fileName):
            # uloz zipko
            fZip = ZipFile(fileName, 'w', ZIP_DEFLATED)
            fZip.writestr('content.xml', xml)
            fZip.close()
        else:
            f = open(fileName, 'w')
            f.write(xml)
            f.close()
    
    def __GetProjectXmlFromFile(self, fileName):
        if is_zipfile(fileName):
            f = ZipFile(fileName,'r')
            result = f.read('content.xml')
        else:
            f = open(fileName)
            result = f.read()
            f.close()
        return result
    
    def __GetProjectXmlFromFileData(self, fd):
        
        result = ''
        try:
            fileLikeObject = StringIO(fd)
            zf = ZipFile(fileLikeObject, 'r')
            result = zf.read('content.xml')
        except:
            result = fd
        return result
    
    
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
        myProject2 = CProject(None, self.__GetProjectXmlFromFileData(fileData))
        
        self.DiffProjects(myProject1, myProject2)
        
#       

    def LoadProject(self, rev = None):
        fd = self.implementation.GetFileData(rev)
        project = CProject(None, self.__GetProjectXmlFromFileData(fd))
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
                
            result = self.implementation.Update(revision)
            if self.implementation.IsInConflict():
                ct = self.implementation.GetConflictingFiles()
                if ct is not None:
                # nastal konflikt svn mi vratilo nazvy suborov (mine, base, upd)
                    mine = self.__GetProjectXmlFromFile(ct['mine'])
                    base = self.__GetProjectXmlFromFile(ct['base'])
                    upd = self.__GetProjectXmlFromFile(ct['new'])
                    updater = CUpdater(mine, base, upd)
                    if updater.IsInConflict():
                        
                        self.SolveConflicts(arg, self.implementation.GetFileName())
                    
                    else:
                        self.__SaveProjectXmlToExistingFile(updater.GetNewXml(), self.implementation.GetFileName())
                        self.implementation.Resolve()
                        self.pluginGuiManager.DisplayWarning(result)
                        self.pluginAdapter.LoadProject(self.implementation.GetFileName())
            
            
            else:
                
                self.pluginGuiManager.DisplayWarning(result)
                self.pluginAdapter.LoadProject(self.implementation.GetFileName())
            
            
                
                
                
            
    
    def Checkin(self, arg):
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        
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
            
            triple = self.implementation.GetConflictingFiles()
            
            
            
            resolved, newXml = self.SolveConflictTriple(triple)
            print 'resolved',resolved
            if resolved:
                self.__SaveProjectXmlToExistingFile(newXml, prFile)
                self.implementation.Resolve()
                self.pluginAdapter.LoadProject(self.implementation.GetFileName())
                
            else:
                pass
                
                
     
    def ShowLogs(self, arg):
        project = self.__LoadApplicationProject()
        if project is None:
            self.interface.GetAdapter().DisplayWarning('No project loaded')
            return
        
        
        logs = self.implementation.Log()
        self.gui.LogsDialog(logs)
        
        
    def SolveConflictTriple(self, triple):    
        if triple is not None:
            upd = self.__GetProjectXmlFromFile(triple['new'])
            base = self.__GetProjectXmlFromFile(triple['base'])
            mine = self.__GetProjectXmlFromFile(triple['mine'])
            
            updater = CUpdater(mine, base, upd)
            
            conflicter = updater.GetConflicter()
            
            merger = updater.GetMerger()
            
            conflictSolver = CConflictSolver(conflicter.GetConflicting(), merger)
            return self.gui.ConflictSolvingDialog(conflictSolver, conflicter.GetBaseWorkDiffer(), conflicter.GetBaseNewDiffer()), merger.GetProject().GetSaveXml()
                
    
        
# select plugin main object
pluginMain = Plugin