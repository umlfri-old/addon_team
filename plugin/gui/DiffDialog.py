'''
Created on 13.4.2010

@author: Peterko
'''
from imports.gtk2 import gtk
from structure import *
from DiagramDrawing import CDiagramDrawing
from DiffDrawing import CDiffDrawing
from ProjectTreeDiffTreeView import CProjectTreeDiffTreeView
import os.path

class CDiffDialog(object):
    '''
    classdocs
    '''


    def __init__(self, wTree, results, projectNew, projectOld):
        '''
        Constructor
        '''
        self.wTree = wTree
        self.results = results
        self.projectNew = projectNew
        self.projectOld = projectOld
        self.dialog = self.wTree.get_object('diffResultsDlg')
        self.drawingArea =self.wTree.get_object('diagramDiffDrawingArea')
        self.newDiagram = None
        self.oldDiagram = None
        self.pixmap = None
        self.__UpdateProjectTreeDiffTreeStore()
        
        self.drawingArea.connect('configure-event', self.drawingareaconfigure)
        self.drawingArea.connect('expose-event', self.drawingareaexpose)
        
        
        
        
        
        self.dialog.run()
        self.dialog.hide()
        
        
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
        for r in self.results:
            if isinstance(r.GetElement(), CBaseView):
                if (self.oldDiagram or self.newDiagram) is not None:
                    if r.GetElement().GetParentDiagram() == (self.oldDiagram or self.newDiagram):
                        diffDrawing = CDiffDrawing(self.context, r, self.oldDiagram, self.newDiagram)
                        print 'drawing diff'
                        diffDrawing.Paint()
        
        
        self.drawingArea.window.draw_drawable(self.drawingArea.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
    
    def drawingareaconfigure(self, widget, event):
        print 'drawin area configure'
        self.__UpdateDiagramDiffDrawingArea()
        
        self.drawingArea.connect('size-request', self.drawingareasizerequest)
        
        return True
    
    def drawingareaexpose(self, widget, event):
        print 'drawing area exposing'
        if self.pixmap is None:
            self.__UpdateDiagramDiffDrawingArea()
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
        return False
    
    def drawingareasizerequest(self, widget, event):
        print 'drawing area size request'
        self.__UpdateDiagramDiffDrawingArea()
        
    def __UpdateProjectTreeDiffTreeStore(self):
        treeModel = self.wTree.get_object('projectTreeTreeStore')
        ptdtv = CProjectTreeDiffTreeView(self.projectOld, self.projectNew, self.results, treeModel)
        
        
        self.wTree.get_object('projectTreeTreeView').connect('cursor-changed', self.on_project_tree_view_cursor_changed)
        
        
    
            
    def on_project_tree_view_cursor_changed(self, treeView):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        node = model.get_value(iter, 2)
        print 'cursor changed'
        if isinstance(node.GetObject(), CDiagram):
            
            self.newDiagram = self.projectNew.GetById(node.GetId())
            
            self.oldDiagram = self.projectOld.GetById(node.GetId())
            
            self.__UpdateDiagramDiffDrawingArea()
    
    