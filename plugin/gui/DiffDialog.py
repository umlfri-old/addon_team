'''
Created on 13.4.2010

@author: Peterko
'''
from imports.gtk2 import gtk
from structure import *
from DiagramDrawing import CDiagramDrawing
from DiffDrawing import CDiffDrawing
from ProjectTreeDiffTreeView import CProjectTreeDiffTreeView
from DataDiffTreeView import CDataDiffTreeView
import os.path

class CDiffDialog(object):
    '''
    classdocs
    '''


    def __init__(self, wTree, differ, conflicts = None):
        '''
        Constructor
        '''
        
        
        
        self.wTree = wTree
        self.differ = differ
        self.conflicts = conflicts
#        self.results = results
#        self.projectNew = projectNew
#        self.projectOld = projectOld
        self.dialog = self.wTree.get_object('diffResultsDlg')
        self.drawingArea =self.wTree.get_object('diagramDiffDrawingArea')
        self.newDiagram = None
        self.oldDiagram = None
        self.pixmap = None
        self.__UpdateProjectTreeDiffTreeStore()
        
        
        id1 = self.wTree.get_object('projectTreeTreeView').connect('cursor-changed', self.on_project_tree_view_cursor_changed)
        
        id2 = self.drawingArea.connect('configure-event', self.drawingareaconfigure)
        id3 = self.drawingArea.connect('expose-event', self.drawingareaexpose)
        self.wTree.get_object('dataDiffTreeStore').clear()
        
        
        
        
        
        self.dialog.run()
        self.dialog.hide()
        
        #self.wTree.get_object('projectTreeTreeView').disconnect(id1)
        #self.drawingArea.disconnect(id2)
        #self.drawingArea.disconnect(id3)
        
        
    def __UpdateDiagramDiffDrawingArea(self):
        
        x, y, width, height = self.drawingArea.get_allocation()
        self.pixmap = gtk.gdk.Pixmap(self.drawingArea.window, width, height)
        self.context = self.pixmap.cairo_create()
        
        self.context.set_source_rgb(1,1,1)
        self.context.rectangle(x,y,width,height)
        self.context.fill()
        oldDiagramDrawing = CDiagramDrawing(self.oldDiagram)
        oldDiagramDrawing.Paint(self.context)
        newDiagramDrawing = CDiagramDrawing(self.newDiagram)
        newDiagramDrawing.Paint(self.context)
        newDiagramSize = newDiagramDrawing.GetSize()
        oldDiagramSize = oldDiagramDrawing.GetSize()

        size = (newDiagramSize[0] if newDiagramSize[0] > oldDiagramSize[0] else oldDiagramSize[0]
                ,newDiagramSize[1] if newDiagramSize[1] > oldDiagramSize[1] else oldDiagramSize[1])
        for r in self.differ.visualDiff:
            if (self.oldDiagram or self.newDiagram) is not None:
                if r.GetElement().GetParentDiagram() == (self.oldDiagram or self.newDiagram):
                    diffDrawing = CDiffDrawing(self.context, r, self.oldDiagram, self.newDiagram)
                    print 'drawing diff'
                    diffDrawing.Paint()
        
        self.drawingArea.set_size_request(int(size[0]), int(size[1]))
        self.drawingArea.window.draw_drawable(self.drawingArea.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
    
    def drawingareaconfigure(self, widget, event):
        
        self.__UpdateDiagramDiffDrawingArea()
        
        self.drawingArea.connect('size-request', self.drawingareasizerequest)
        
        return True
    
    def drawingareaexpose(self, widget, event):
        if self.pixmap is None:
            self.__UpdateDiagramDiffDrawingArea()
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
        return False
    
    def drawingareasizerequest(self, widget, event):
        
        self.__UpdateDiagramDiffDrawingArea()
        
    def __UpdateProjectTreeDiffTreeStore(self):
        treeModel = self.wTree.get_object('projectTreeTreeStore')
        ptdtv = CProjectTreeDiffTreeView(self.differ, treeModel, self.conflicts)
        
        
        
        
    
    def __UpdateDataDiffTreeView(self, oldObj, newObj):
        print 'updating data diff tree view'
        treeModel = self.wTree.get_object('dataDiffTreeStore')
        ddtv = CDataDiffTreeView(oldObj, newObj, self.differ, treeModel)
        
    
            
    def on_project_tree_view_cursor_changed(self, treeView):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        node = model.get_value(iter, 3)
        print 'cursor changed'
        if node is not None:
            if isinstance(node.GetObject(), CDiagram):
                
                self.newDiagram = self.differ.GetNewProject().GetById(node.GetId())
                
                self.oldDiagram = self.differ.GetOldProject().GetById(node.GetId())
                
                self.__UpdateDiagramDiffDrawingArea()
        
            obj = node.GetObject()
            oldObj = self.differ.GetOldProject().GetById(obj.GetId())
            newObj = self.differ.GetNewProject().GetById(obj.GetId())
            self.__UpdateDataDiffTreeView(oldObj, newObj)
        
        
        