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
        self.diffTxt = self.wTree.get_object('diffTxt')
        
        
        
        
        
        
        self.selection = None
        
        self.wTree.get_object('projectTreeTreeView').connect('cursor-changed', self.on_project_tree_view_cursor_changed)
        self.wTree.get_object('dataDiffTreeView').connect('cursor-changed', self.on_data_diff_view_cursor_changed)
        
        self.drawingArea.connect('configure-event', self.drawingareaconfigure)
        self.drawingArea.connect('expose-event', self.drawingareaexpose)
        self.drawingArea.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.drawingArea.connect('button-press-event', self.drawingareaclick)
        self.wTree.get_object('dataDiffTreeStore').clear()
        
        
        
        
        
        
        
      
    def Run(self):
        self.__UpdateProjectTreeDiffTreeStore()
        
        self.__UpdateDataDiffTreeView(None, None)
        
        self.newDiagram = None
        self.oldDiagram = None
        self.pixmap = None
        self.selection = None
        
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
        self.oldDiagramDrawing = CDiagramDrawing(self.oldDiagram)
        self.oldDiagramDrawing.Paint(self.context)
        self.newDiagramDrawing = CDiagramDrawing(self.newDiagram)
        self.newDiagramDrawing.Paint(self.context)
        newDiagramSize = self.newDiagramDrawing.GetSize()
        oldDiagramSize = self.oldDiagramDrawing.GetSize()

        size = (newDiagramSize[0] if newDiagramSize[0] > oldDiagramSize[0] else oldDiagramSize[0]
                ,newDiagramSize[1] if newDiagramSize[1] > oldDiagramSize[1] else oldDiagramSize[1])
        for r in self.differ.visualDiff:
            if (self.oldDiagram or self.newDiagram) is not None:
                if r.GetElement().GetParentDiagram() == (self.oldDiagram or self.newDiagram):
                    diffDrawing = CDiffDrawing(self.context, r, self.oldDiagram, self.newDiagram)
                    
                    diffDrawing.Paint()
        
        
        
        if self.selection is not None and self.selection != []:
            print 'selection', len(self.selection), self.selection
            for sel in self.selection:
                if sel is not None:
                    self.context.new_path()
                    self.context.set_dash((5,5))
                    self.context.set_source_rgb(0,0,0)
                    self.context.append_path(sel)
                    self.context.stroke()
            
        
        self.drawingArea.set_size_request(int(size[0]) + 20, int(size[1]))
        self.drawingArea.window.draw_drawable(self.drawingArea.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
        
    def drawingareaclick(self, widget, event):
        
        if event.button == 1:
            self.selection = [None]
            el = None
            
            if self.newDiagramDrawing is not None:
                elNew = self.newDiagramDrawing.GetViewAtPoint((event.x, event.y))
            if self.oldDiagramDrawing is not None:
                elOld = self.oldDiagramDrawing.GetViewAtPoint((event.x, event.y))
            
            el = elNew or elOld
            sel1 = self.oldDiagramDrawing.GetSelectionOfView(el)
            sel2 = self.newDiagramDrawing.GetSelectionOfView(el)
            self.selection = [sel1, sel2]
                
            
            
            
            foundDiffs = []
            if el is not None:
                for diff in self.differ.visualDiff:
                    if diff.GetElement() == el:
                        foundDiffs.append(diff)
            self.__ShowDiffs(foundDiffs)
            self.__UpdateDiagramDiffDrawingArea()
    
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
#        if diff is not None:
        self.__ShowDiffs([diff])
#        else:
#            self.diffLabel.set_text('')
    
    def __ShowDiffs(self, diffs):
        self.diffTxt.get_buffer().set_text('')
        text = ''
        for diff in diffs:
            text += str(diff)+'\n---\n'
        self.diffTxt.get_buffer().set_text(text)
        
    def on_data_diff_view_cursor_changed(self, treeView):
        sel = treeView.get_selection()
        (model, iter) = sel.get_selected()
        diff = model.get_value(iter, 4)
#        if diff is not None:
        self.diffLabel.set_text([diff])
#        else:
#            self.diffLabel.set_text('')
        
        