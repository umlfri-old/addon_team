'''
Created on 27.2.2010

@author: Peterko
'''

from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from lib.Depend.gtk2 import gtk
from structure import *
from support import *
from zipfile import ZipFile, is_zipfile

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
        self.interface.StartAutocommit()
        try:
            # add menu
            self.interface.AddMenu('MenuItem', 'mnuMenubar', 'team', None, text = 'Team')
            self.interface.AddMenu('submenu', 'mnuMenubar/team', None, None)
            self.interface.AddMenu('MenuItem', 'mnuMenubar/team', 'DiffProject', self.DiffProject, text = 'Diff project')
            self.interface.AddMenu('MenuItem', 'mnuMenubar/team', 'DiffDiagram', self.DiffDiagram, text = 'Diff diagram')
            self.interface.AddMenu('MenuItem', 'mnuMenubar/team', 'DiffElement', self.DiffElement, text = 'Diff element')
        except PluginInvalidParameter:
            pass
        
    
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
        
        prFile = project.GetFileName()
        if (is_zipfile(prFile)):
            file = ZipFile(prFile,'r')
            fileData = file.read('content.xml')
        else :
            file = open(prFile, 'r')
            fileData = file.read()
        myProject1 = CProject(project)
        myProject2 = CProject(None, fileData)
        self.interface.DisplayWarning(str(myProject1))
        self.interface.DisplayWarning(str(myProject2))
        differ = CDiffer(myProject2, myProject1)
        differ.diffProjects()
        
            
                
    def DiffDiagram(self, *args):
        pass
        
    def DiffElement(self, *args):
        pass    
        
        
# select plugin main object
pluginMain = Plugin