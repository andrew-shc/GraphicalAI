"""
Widgets that requires context of project info/data/meta to design the whole project workspace
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, Slot, QMargins
from PySide6.QtGui import QPalette, QColor

from project.project_home import ProjectHomepage
from project.model_editor import ModelPage
from project.model_execution import ExecutionPage
from project.model_deployment import DeploymentPage
from file_handler import ProjectFileHandler, ReferencedFileHandler


class Project(QWidget):
    def __init__(self, fhndl: ProjectFileHandler, lfhndl: ReferencedFileHandler, parent=None):
        super().__init__(parent)

        self.fhndl = fhndl
        self.lfhndl = lfhndl
        self.pages = QStackedLayout()
        self.pages.addWidget(ProjectHomepage(self.fhndl, parent=self))
        self.pages.addWidget(ModelPage(self.fhndl, parent=self))
        self.pages.addWidget(ExecutionPage(parent=self))
        self.pages.addWidget(DeploymentPage(parent=self))

        self.wx_proj_tab = ProjectTabs()
        self.wx_proj_tab.sg_prj_page_selc.connect(self.pages.setCurrentIndex)
        self.wx_proj_tab.sg_prj_save.connect(lambda: self.fhndl.save_project())

        self.lyt_main = QVBoxLayout()
        self.lyt_main.setMenuBar(self.wx_proj_tab)
        self.lyt_main.addLayout(self.pages)

        self.setLayout(self.lyt_main)

    # print(lyt_main.menuBar())

    def __del__(self):  # adds auto-save before the project object gets deleted
        # TODO: save project must be before you add project for new projects, because it root_file attr will be None
        self.fhndl.save_project()
        print("project (in future) saved")
        if not self.lfhndl.ref_proj_existed(self.fhndl.path):
            self.lfhndl.add_project(self.fhndl.name, self.fhndl.root_file)
        self.lfhndl.save()
        print("project auto-referenced before exit")
        print("object deleted")


class ProjectTabs(QWidget):
    sg_prj_page_selc = Signal(int)  # int: page number
    sg_prj_save = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(247, 247, 247))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        wcb_page_selc = QComboBox()
        wcb_page_selc.currentTextChanged.connect(self._sl_page_selc_change)
        wcb_page_selc.addItem("Home")
        wcb_page_selc.addItem("Models")
        wcb_page_selc.addItem("Execution")
        wcb_page_selc.addItem("Deployment")

        lyt_main = QHBoxLayout()
        lyt_main.addWidget(wcb_page_selc)
        wb_save_proj = QPushButton("Save Project")
        wb_save_proj.clicked.connect(self._sl_proj_save_click)
        lyt_main.addWidget(wb_save_proj)
        lyt_main.addWidget(QPushButton("Press me! (Does nothing)"))

        self.setLayout(lyt_main)

        margin = lyt_main.contentsMargins()
        margin.setTop(3)
        margin.setBottom(3)
        lyt_main.setContentsMargins(margin)

    @Slot(str)
    def _sl_page_selc_change(self, text):
        try:
            page_no = {"Home": 0, "Models": 1, "Execution": 2, "Deployment": 3}[text]
        except KeyError:
            print(f"error: <{text}> page not implemented")
            page_no = 0

        self.sg_prj_page_selc.emit(page_no)

    @Slot(bool)
    def _sl_proj_save_click(self, _checked):
        self.sg_prj_save.emit()
