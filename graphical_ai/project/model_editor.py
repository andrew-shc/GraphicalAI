from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, Slot, QRectF, QPointF
from PySide6.QtGui import *

from model_view.node import FasterNode, CT, InputField, OutputField, ConstantField
from model_view.components import *
from node_graph.nodes import export, NodeExec
import errors


class NodeSideMenu(QWidget):
    sg_node_selc = Signal(str, str)
    sg_save_mdl = Signal()
    sg_del_mdl = Signal()
    sg_exec_mdl = Signal()
    sg_clear_mdl = Signal()

    def __init__(self, mdl_name, parent=None):
        super().__init__(parent=parent)

        self.mdl_name = mdl_name

        wtw_nodes_selc = QTreeWidget(parent=self)
        wtw_nodes_selc.itemDoubleClicked.connect(self.sl_node_selc)
        wtw_nodes_selc.setHeaderHidden(True)
        wtw_nodes_selc.setIndentation(10)

        for top in export:
            wx_top = QTreeWidgetItem([top])
            for inner in export[top]:
                _wx_inner = QTreeWidgetItem(wx_top, [inner])
            wtw_nodes_selc.addTopLevelItem(wx_top)

        self.wl_mdl_name = QLabel(mdl_name)

        wb_mdl_saved = QPushButton("Save Model")
        wb_mdl_saved.clicked.connect(lambda _checked: self.sl_save_mdl())
        wb_mdl_del = QPushButton("Clear Model")
        wb_mdl_del.clicked.connect(lambda _checked: self.sl_clear_mdl())
        wb_mdl_exec = QPushButton("Execute Model")
        wb_mdl_exec.clicked.connect(lambda _checked: self.sl_exec_mdl())

        lyt_main = QVBoxLayout()
        lyt_main.addWidget(self.wl_mdl_name)
        lyt_main.addWidget(wb_mdl_saved)
        lyt_main.addWidget(wb_mdl_del)
        lyt_main.addWidget(wb_mdl_exec)
        lyt_main.addWidget(wtw_nodes_selc)

        self.setLayout(lyt_main)

    @Slot(str)
    def sl_change_mdl_name(self, name):
        self.wl_mdl_name.setText(name)

    @Slot(object, int)
    def sl_node_selc(self, item, _column):
        if item.parent() is not None:  # check if item is child, not top-level
            self.sg_node_selc.emit(item.parent().text(0), item.text(0))

    @Slot()
    def sl_save_mdl(self):
        self.sg_save_mdl.emit()

    @Slot()
    def sl_del_mdl(self):
        self.sg_del_mdl.emit()

    @Slot()
    def sl_exec_mdl(self):
        self.sg_exec_mdl.emit()

    @Slot()
    def sl_clear_mdl(self):
        self.sg_clear_mdl.emit()


class ModelWorkspace(QGraphicsView):
    def __init__(self, model_name: str, parent=None):
        super().__init__(parent=parent)
        self.model_name = model_name
        self.view_size = 10000  # as large as possible
        self.exec_node_dt = []  # list of exec node class

        self.qscene = QGraphicsScene(parent=self)
        # self.qscene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.qscene.addText(model_name)
        # o = FasterNode(self.qscene, "Node Title", ["inp field A"], ["out field A", "out field B"], ["const field A"], pos=(-100,0))
        # self.qscene.addItem(o)
        # self.qscene.addItem(Connector("type", pos=(200, 200)))
        # for i in range(0,40):
        # self.qscene.addItem(Node(pos=(i*8-300,i*8-300)))
        # nd = FasterNode(
        # 	self.qscene, "Node Title",
        # 	[InputField("inp field A", CT.ANY)],
        # 	[OutputField("out field A", CT.ANY), OutputField("out field B", CT.ANY)],
        # 	[ConstantField("const field A", ComboBox())],
        # 	pos=(300, 300)  #(i*8-300,i*8-300)
        # )
        # self.qscene.addItem(nd)
        # nd.add_const_wx(self.qscene)

        self.setScene(self.qscene)

        # self = QGraphicsView(self.qscene, parent=self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSceneRect(QRectF(-self.view_size, -self.view_size, self.view_size * 2, self.view_size * 2))
        # print(self.size(), self.width(), self.height())
        # self.centerOn(QPointF(self.size().width(), self.size().height()))
        # self.view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, False)
        # self.view.setBackgroundBrush(QBrush(QColor("#101010")))
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.show()

    # self.view.fitInView(QRectF(-10, -20, 10, 20))
    # self.view.setAlignment(Qt.AlignRight)
    # self.view.centerOn(QPointF(0,0))

    # lyt_main = QHBoxLayout()
    # lyt_main.addWidget(self.view)
    #
    # self.setLayout(lyt_main)

    def add_node(self, cat, nd_name):
        # nd = FasterNode(
        # 	self.qscene, "Node Title",
        # 	[InputField("inp field A", CT.ANY)],
        # 	[OutputField("out field A", CT.ANY), OutputField("out field B", CT.ANY)],
        # 	[ConstantField("const field A", ComboBox())],
        # 	pos=(i*8-300, i*8-300)
        # )
        wx_node_cls: NodeExec = export[cat][nd_name]()  # class reference
        self.exec_node_dt.append(wx_node_cls)
        wx_node = wx_node_cls.interface(self.qscene, (0, 0))
        self.qscene.addItem(wx_node)
        wx_node.add_const_wx(self.qscene)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Shift:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def keyReleaseEvent(self, event: QKeyEvent):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Shift:
            self.setDragMode(QGraphicsView.NoDrag)


class ModelPage(QWidget):
    def __init__(self, fhndl, parent=None):
        super().__init__(parent=parent)

        # self.wx_models = []
        self.fhndl = fhndl

        self.wtw_mdl_tabs = QTabWidget()
        self.wtw_mdl_tabs.tabBarClicked.connect(self.sl_add_new_mdl)

        if len(self.fhndl.get_mdl_refs()) == 0:
            wx_first_mdl = ModelWorkspace("unnamed", parent=self.wtw_mdl_tabs)
            self.wtw_mdl_tabs.insertTab(0, wx_first_mdl, "unnamed")
        else:
            for mdl_id in self.fhndl.get_mdl_refs():
                model: ModelWorkspace = self.fhndl.load_model(mdl_id, parent=self.wtw_mdl_tabs)
                print(model)
                self.wtw_mdl_tabs.addTab(model, model.model_name)
        self.wtw_mdl_tabs.addTab(QLabel("Nothing to see here."), "+")

        wx_sidemenu = NodeSideMenu("unnamed")
        wx_sidemenu.sg_node_selc.connect(self.sl_add_node)  # wx_first_mdl.sl_add_node)
        wx_sidemenu.sg_save_mdl.connect(self.sl_save_cur_mdl)
        wx_sidemenu.sg_del_mdl.connect(self.sl_del_cur_mdl)
        wx_sidemenu.sg_exec_mdl.connect(self.sl_exec_cur_mdl)
        wx_sidemenu.sg_clear_mdl.connect(self.sl_clear_cur_mdl)

        lyt_main = QHBoxLayout()
        lyt_main.addWidget(wx_sidemenu, 15)
        lyt_main.addWidget(self.wtw_mdl_tabs, 70)
        lyt_main.addWidget(QLabel("Minimizable \n Inspection page"), 10)

        self.setLayout(lyt_main)

    @Slot(str, str)
    def sl_add_node(self, cat, nd_name):
        wx: ModelWorkspace = self.wtw_mdl_tabs.widget(self.wtw_mdl_tabs.currentIndex())
        wx.add_node(cat, nd_name)

    @Slot(int)
    def sl_add_new_mdl(self, index: int):
        if self.wtw_mdl_tabs.count() == index + 1:
            self.wtw_mdl_tabs.insertTab(index, ModelWorkspace("unnamed", parent=self.wtw_mdl_tabs), "unnamed")

    @Slot()
    def sl_save_cur_mdl(self):
        mdl_workspace: ModelWorkspace = self.wtw_mdl_tabs.widget(self.wtw_mdl_tabs.currentIndex())
        try:
            self.fhndl.save_model(self.fhndl.get_mdl_id(mdl_workspace.model_name), mdl_workspace)
        except errors.ProjectFileAppError as e:
            if e.code == errors.ProjectFileAppError.MDL_NAME_NON_EXISTENT:
                self.fhndl.save_model(self.fhndl.new_mdl_id(mdl_workspace.model_name), mdl_workspace)
            else:
                raise e

    @Slot()
    def sl_del_cur_mdl(self):
        print("Deleting model does nothing right now")

    @Slot()
    def sl_exec_cur_mdl(self):
        mdl_workspace: ModelWorkspace = self.wtw_mdl_tabs.widget(self.wtw_mdl_tabs.currentIndex())
        self.fhndl.execute_model(self.fhndl.get_mdl_id(mdl_workspace.model_name))

    @Slot()
    def sl_clear_cur_mdl(self):
        mdl_workspace: ModelWorkspace = self.wtw_mdl_tabs.widget(self.wtw_mdl_tabs.currentIndex())
        mdl_workspace.scene().clear()

