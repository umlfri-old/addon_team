'''
Created on 27.2.2010

@author: Peterko
'''

from gui import Gui

from structure import *
from support import *
from zipfile import is_zipfile, ZIP_DEFLATED, ZipFile
import uuid
from cStringIO import StringIO

class Plugin(object):
    '''
    Team plugin for UML .FRI
    '''
    
    incompatibleText = 'Project is under version control, but is incompatible with Team plugin. Would you like to make it compatible? (There will be no physical changes to project file)'
    
    def __init__(self, interface):
        '''
        Constructor for Team plugin, initialize all notifications and menus
        @type interface: CInterface
        @param interface: Plugin system interface  
        '''
        # load interface
        self.interface = interface
        self.interface.SetGtkMainloop()
        
        self.pluginAdapter = self.interface.GetAdapter()
        self.pluginGuiManager = self.pluginAdapter.GetGuiManager()
        
        
        self.receivedFileData = {}
        self.implementations = {}
        
        
        self.gui = Gui(self)
        
        
        self.interface.StartAutocommit()
        
        self.pluginAdapter.AddNotification('project-opened', self.ProjectOpened)
        
        self.pluginAdapter.AddNotification('team-exception', self.TeamException)
        
        self.pluginAdapter.AddNotification('team-send-supported', self.ReceiveSupported)
        
        self.pluginAdapter.AddNotification('team-send-log', self.ReceiveLog)
        self.pluginAdapter.AddNotification('team-send-file-data', self.ReceiveFileData)
        self.pluginAdapter.AddNotification('team-continue-diff-project', self.ContinueDiffProject)
        self.pluginAdapter.AddNotification('team-continue-diff-revisions', self.ContinueDiffRevisions)
        
        self.pluginAdapter.AddNotification('team-get-authorization', self.GetAuthorization)
        self.pluginAdapter.AddNotification('team-send-result', self.ReceiveResult)
        self.pluginAdapter.AddNotification('team-solve-conflicts', self.SolveConflicts)
        self.pluginAdapter.AddNotification('team-send-register-implementation-for-checkout', self.RegisterImplementationForCheckout)
        self.pluginAdapter.AddNotification('team-ask-compatible', self.AskCompatible)
        self.pluginAdapter.AddNotification('team-load-project', self.LoadProjectFile)
        self.pluginAdapter.AddNotification('team-ask-server-cert', self.AskServerCert)
        
        self.pluginAdapter.Notify('team-register-for-checkout')
        
        
        # add menu
        self.teamMenuRoot = self.pluginGuiManager.GetMainMenu().AddMenuItem(str(uuid.uuid1()) ,None, -2,'Team',None,None)
        #add submenu
        self.teamMenuRoot.AddSubmenu()
        self.teamMenuSubmenu = self.teamMenuRoot.GetSubmenu()
        
        self.diffMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.DiffProject,0,'Diff project',None,None)
        self.updateMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Update,1,'Update',None,None)
        self.checkinMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkin,2,'Checkin',None,None)
        self.revertMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Revert,3,'Revert',None,None)
        self.solveConflictsMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.SolveConflictsInOpenedProject ,4,'Solve conflicts',None,None)
        self.checkoutMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.Checkout,5,'Checkout',None,None)
        self.logsMenu = self.teamMenuSubmenu.AddMenuItem(str(uuid.uuid1()),self.ShowLogs,6,'Show logs',None,None)
        
        self.__ResetMenuSensitivity()
        self.ProjectOpened()

                    
    def LoadProjectFile(self, fileName):
        '''
        Loads project with filename in application
        @type fileName: string
        @param fileName: path to file  
        '''
        self.pluginAdapter.LoadProject(fileName)
       
    def AskCompatible(self):    
        '''
        Asks user if he wants to make project file compatible with version system. Notify implementations.
        '''
        response = self.gui.ShowQuestion(self.incompatibleText)
        if response:
            self.pluginAdapter.Notify('team-make-compatible')
      
    def ProjectOpened(self):
        '''
        Hook executed when project file is opened. Checks if plugin can run, resets menu sensitivity, notify implementations.
        '''
        self.__ResetMenuSensitivity()
        
        if self.__CanRunPlugin():
            fileName = self.__LoadApplicationProject().GetFileName()
            
            self.pluginAdapter.Notify('team-project-opened', fileName)
            self.pluginAdapter.Notify('team-get-supported')
        
            
    
    
    def ReceiveResult(self, result):
        '''
        Hook executed when receiving result from implementations. Displays dialog with result
        @type result: string
        @param result: String to be displayed 
        '''
        self.pluginGuiManager.DisplayWarning(result)
    
    
    def TeamException(self, exc):
        '''
        Hook executed when receiving exception from implementations. Displays dialog with exception
        @type exc: Exception
        @param exc: Exception instance  
        '''
        self.pluginGuiManager.DisplayWarning(str(exc))
            
            
    def ReceiveLog(self, logs):
        '''
        Hook executed when receiving logs. Displays logs window.
        @type logs: list
        @param logs: list with log information 
        '''        
        self.gui.LogsDialog(logs)
        
    def AskServerCert(self, actionId, message, *param):
        '''
        Hook executed when implementation asks for accepting server certificate. Notify back actionId if response is positive
        @type actionId: string
        @param actionId: Identifier of hook that executes action in implementation.
        @type message: string
        @param message: Message to display in dialog
        @param *param: additional parameters, will be send back in notify 
        '''
        response = self.gui.ShowQuestion(message+'\nAccept server certificate?')
        if response:
            self.pluginAdapter.Notify(actionId, None, None, response, *param)
    
    def ReceiveSupported(self, supported): 
        '''
        Hook executed when receiving supported operations in implementation. Updates menu sensitivity
        @type supported: list
        @param supported: list with supported methods in implementation
        '''
        
        self.diffMenu.SetSensitive('diff' in supported)
        self.updateMenu.SetSensitive('update' in supported)
        self.checkinMenu.SetSensitive('checkin' in supported)
        self.revertMenu.SetSensitive('revert' in supported)
        self.logsMenu.SetSensitive('log' in supported)  
        
        self.solveConflictsMenu.SetSensitive('resolve' in supported) 
    
    
    def ReceiveFileData(self, data, idData):
        '''
        Hook executed when receiving file data from implementation
        @type data: string
        @param data: String with file data
        @type idData: string
        @param idData: identifier of data received, used later
        '''
        self.receivedFileData[idData] = data
    
    
    def __ResetMenuSensitivity(self):
        '''
        Resets menu sensitivity
        '''
        self.diffMenu.SetSensitive(False)
        self.updateMenu.SetSensitive(False)
        self.checkinMenu.SetSensitive(False)
        self.revertMenu.SetSensitive(False)
        self.solveConflictsMenu.SetSensitive(False)
        self.checkoutMenu.SetSensitive(False or self.implementations != {})
        self.logsMenu.SetSensitive(False)
        
    def __CanRunPlugin(self):
        '''
        Checks if plugin can run
        @rtype: bool
        @return: True if plugin can run, False otherwise
        '''
        p = self.__LoadApplicationProject()
        if p is None:
            return False
        elif p.GetFileName() is None:
            return False
        else:
            return True
    
    def __SaveProjectXmlToExistingFile(self, xml, fileName):
        '''
        Saves project filedata in existing file, checks if file is zipped
        @type xml: string
        @param xml: file data
        @type fileName: string
        @param fileName: path to existing file
        '''
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
        '''
        Gets project xml from file specified with filename
        @type fileName: string
        @param fileName: path to file 
        @rtype: string
        @return: string with xml project data
        '''
        if is_zipfile(fileName):
            f = ZipFile(fileName,'r')
            result = f.read('content.xml')
        else:
            f = open(fileName)
            result = f.read()
            f.close()
        return result
    
    def __GetProjectXmlFromFileData(self, fd):
        '''
        Gets project xml from file data. File data can be read zipped file.
        @type fd: string
        @param fd: file data
        @rtype: string
        @return: string with xml project data
        '''
        result = ''
        try:
            fileLikeObject = StringIO(fd)
            zf = ZipFile(fileLikeObject, 'r')
            result = zf.read('content.xml')
        except:
            result = fd
        return result
    
    
    def __LoadApplicationProject(self):
        '''
        Gets project
        @rtype: IProject
        @return: Project
        '''
        return self.pluginAdapter.GetProject()
    
    
    def DiffProject(self, arg):
        '''
        Executes diff of two project, notify implementation to get file data
        '''
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return

        self.pluginAdapter.Notify('team-get-file-data', None, None, False, 'diff-project', 'diff-project')
        
        
    def ContinueDiffProject(self):
        '''
        Continues diffing
        '''
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        myProject1 = CProject(project)
        fileData = self.receivedFileData['diff-project']
        myProject2 = CProject(None, self.__GetProjectXmlFromFileData(fileData))
        
        self.DiffProjects(myProject1, myProject2)
        self.receivedFileData.pop('diff-project')
        
#       

    def DiffRevisions(self, rev1, rev2):
        '''
        Begin diff of two revision, notify implementation to get file data
        '''
        self.pluginAdapter.Notify('team-get-file-data', None, None,False,'diff-revisions1', 'diff-revisions', rev1)
        self.pluginAdapter.Notify('team-get-file-data', None, None,False,'diff-revisions2', 'diff-revisions', rev2)
        

        
    def ContinueDiffRevisions(self):
        '''
        Continues diff of two revisions
        '''
        fd1 = self.receivedFileData.get('diff-revisions1',None)
        fd2 = self.receivedFileData.get('diff-revisions2',None)
        if fd1 is None or fd2 is None:
            # este tam nie su vsetky data, pockaj si na ne
            pass
        else:
            project1 = CProject(None, self.__GetProjectXmlFromFileData(fd1))
            project2 = CProject(None, self.__GetProjectXmlFromFileData(fd2))
            self.DiffProjects(project1, project2)
            self.receivedFileData.pop('diff-revisions1')
            self.receivedFileData.pop('diff-revisions2')
        
    
    def DiffProjects(self, project1, project2):
        '''
        Diff two projects
        @type project1: CProject
        @param project1: first project to be compared
        @type project2: CPorject
        @param project2: second project to be compared
        '''
        differ = CDiffer(project2, project1)
        self.gui.DiffResultsDialog(differ)
     
     
    def GetAuthorization(self, actionId, *params):
        '''
        Hook executed when implementation asks for authorization
        @type actionId: string
        @param actionId: action identifier that will be notified back
        @param *params: additional params will be send back 
        '''    
        username, password = self.gui.AuthDialog()
        if username is not None and password is not None:
            self.pluginAdapter.Notify(actionId, username, password, *params)
        
    def Update(self, arg):
        '''
        Executes update, notify implementation about update
        '''
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
            
            self.pluginAdapter.Notify('team-update', None, None, False, revision)
            
            
                
                
                
            
    
    def Checkin(self, arg):
        '''
        Executes checkin, notify implementation
        '''
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        project.Save()
        
        msg = self.gui.CheckinMessageDialog()
        self.pluginAdapter.Notify('team-checkin', None, None, False, msg)
            
                        
            
    def Revert(self, arg):
        '''
        Executes revert, notify implementation
        '''
        project = self.__LoadApplicationProject()
        if project is None:
            self.pluginGuiManager.DisplayWarning('No project loaded')
            return
        
        self.pluginAdapter.Notify('team-revert')
        
    
        
    def Checkout(self, arg):
        '''
        Executes checkout, notify implementation
        '''
        result = self.gui.CheckoutDialog(self.implementations)
        if result is not None:
            # vyber implementaciu
            implId = result[0]
            url = result[1]
            directory = result[2]
            revision = result[3]
            self.pluginAdapter.Notify('team-checkout',None, None, False, implId, url, directory, revision)
            
      
    def SolveConflictsInOpenedProject(self, arg):
        '''
        Notify implementation about solving conflicts
        '''
        self.pluginAdapter.Notify('team-solve-conflicts-in-opened-project')      
            
    def SolveConflicts(self, triple, prFile):
        '''
        Solve conflicts
        @type triple: dic
        @param triple: dictionary with mine, base and new project files
        @type prFile: string
        @param prFile: file where resolved project will be saved
        '''
        mine = self.__GetProjectXmlFromFile(triple['mine'])
        base = self.__GetProjectXmlFromFile(triple['base'])
        upd = self.__GetProjectXmlFromFile(triple['new'])
        updater = CUpdater(mine, base, upd)
        if updater.IsInConflict():
            
            resolved, newXml = self.SolveConflictTriple(updater)
        
        
            
            
            
            if resolved:
                self.__SaveProjectXmlToExistingFile(newXml, prFile)
            
                self.pluginAdapter.Notify('team-resolve')
                
                    
        else:
            # not in conflict
            # save merged file
            self.__SaveProjectXmlToExistingFile(updater.GetNewXml(), prFile)
            self.pluginAdapter.Notify('team-resolve')
            
                
                
     
    def ShowLogs(self, arg):
        '''
        Executes showing logs
        '''
        project = self.__LoadApplicationProject()
        if project is None:
            self.interface.GetAdapter().DisplayWarning('No project loaded')
            return
        
        self.pluginAdapter.Notify('team-get-log', None, None, False)
        
    def RegisterImplementationForCheckout(self, id, description):
        '''
        Hook executed when implementation register itself for checkout
        @type id: string
        @param id: implementation identification
        @type description: string
        @param description: description of CVS
        '''
        self.implementations[id] = description
        self.__ResetMenuSensitivity()
        
        
    def SolveConflictTriple(self, updater):   
        '''
        Executes conflict solving
        @type updater: CUpdater
        @param updater: updater
        @rtype: bool, string
        @return: True if conflicts were solved, xml of solved project
        ''' 
        if updater is not None:
            if updater.IsInConflict():
                
                conflicter = updater.GetConflicter()
                
                
                
                merger = updater.GetMerger()
                
                conflictSolver = CConflictSolver(conflicter.GetConflicting(), merger)
                result = self.gui.ConflictSolvingDialog(conflictSolver, conflicter.GetBaseWorkDiffer(), conflicter.GetBaseNewDiffer())
                return result, merger.GetProject().GetSaveXml()
            else:
                return False, 'None'
        else:
            return False, 'None'
                
    
        
# select plugin main object
pluginMain = Plugin