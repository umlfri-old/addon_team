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


    def __init__(self, wTree):
        '''
        Constructor
        '''
        
        
        
        self.wTree = wTree
        self.differ = None
        self.conflicts = None
        
        self.dialog = self.wTree.get_object('diffResultsDlg')
        self.drawingArea =self.wTree.get_object('diagramDiffDrawingArea')
        self.diffLabel = self.wTree.get_object('diffLabel')
        
        
        
        
        
        
        
        self.wTree.get_object('projectTreeTreeView').connect('cursor-changed', self.on_project_tree_view_cursor_changed)
        self.wTree.get_object('dataDiffTreeView').connect('cursor-changed', self.on_data_diff_view_cursor_changed)
        
        self.drawingArea.connect('configure-event', self.drawingareaconfigure)
        self.drawingArea.connect('expose-event', self.drawingareaexpose)
        self.wTree.get_object('dataDiffTreeStore').clear()
        
        
        
        
        
        
        
      
    def Run(self):
        self.__UpdateProjectTreeDiffTreeStore()
        
        self.__UpdateDataDiffTreeView(None, None)
        
        self.newDiagram = None
        self.oldDiagram = None
        self.pixmap = None
        
        self.dialog.run()
        self.dialog.hide()  

    def SetDiffer(self, differ):
        self.differ = differ
        
    def SetConflicts(self, conflicts):
        self.conflicts = conflicts
        
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
        
        treeModel = self.wTree.get_object('dataDiffTreeStore')
        if oldObj is None and newObj is None:
            treeModel.clear()
        else:
            ddtv = CDataDiffTreeView(oldObj, newObj, self.differ, treeModel, self.conflicts)
        
    
            
    def on_project_tree_view_cursor_changed(self, treeView):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        node = model.get_value(iter, 3)
        
        if node is not None:
            if isinstance(node.GetObject(), CDiagram):
                
                self.newDiagram = self.differ.GetNewProject().GetById(node.GetId())
                
                self.oldDiagram = self.differ.GetOldProject().GetById(node.GetId())
                
                self.__UpdateDiagramDiffDrawingArea()
        
            obj = node.GetObject()
            oldObj = self.differ.GetOldProject().GetById(obj.GetId())
            newObj = self.differ.GetNewProject().GetById(obj.GetId())
            self.__UpdateDataDiffTreeView(oldObj, newObj)
            
        diff = model.get_value(iter, 5)
        if diff is not None:
            self.diffLabel.set_text(str(diff))
        else:
            self.diffLabel.set_text('')
        
    def on_data_diff_view_cursor_changed(self, treeView):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        diff = model.get_value(iter, 4)
        if diff is not None:
            self.diffLabel.set_text(str(diff))
        else:
            self.diffLabel.set_text('')
        
        