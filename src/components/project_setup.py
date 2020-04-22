from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

from src.widgets import ErrorBox, NewProject, LoadProject
from src.interface.project_file_interface import ProjectFI
from src.constants import DEBUG__

from typing import Optional
import os

class ProjectSetup(QWidget):
    projectCreated = pyqtSignal(ProjectFI)  # new project
    projectLoaded = pyqtSignal(ProjectFI)  # load project

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.project: Optional[ProjectFI] = None

        self.inst_gui()

    def inst_gui(self):
        menu_left = QVBoxLayout()

        self.proj_name = QLabel("<b>undefined</b>")
        p: QPalette = self.proj_name.palette()
        p.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.proj_name.setPalette(p)

        proj_dscrp = QFormLayout()
        proj_dscrp.addRow(QLabel("Project Name: "), self.proj_name)

        proj_new = NewProject("New Project")
        proj_new.inputSelected.connect(lambda nm, dir: self.new_proj(nm, dir))

        proj_ld = LoadProject("Load Project")
        proj_ld.inputSelected.connect(lambda dir: self.load_project(dir))

        proj_save = QPushButton("Save Project")
        proj_save.clicked.connect(lambda checked: self.save_proj())

        menu_left.addLayout(proj_dscrp)
        menu_left.addWidget(proj_new)
        menu_left.addWidget(proj_ld)
        menu_left.addWidget(proj_save)
        menu_left.addStretch()

        base = QHBoxLayout()
        base.addLayout(menu_left)
        base.addStretch(2)

        self.setLayout(base)

    def new_proj(self, name: str, path: str):
        self.project = ProjectFI(name=name, path=path)
        self.projectCreated.emit(self.project)

        self.proj_name.setText("<b>"+name+"</b>")
        p: QPalette = self.proj_name.palette()
        p.setColor(QPalette.WindowText, QColor(0, 0, 200))
        self.proj_name.setPalette(p)

    def load_project(self, dir: str):
        try:
            self.project = ProjectFI.load(dir)
        except:
            ErrorBox(**ErrorBox.E007).exec()
            self.project = None
            if DEBUG__: raise

        if self.project is not None:
            self.projectLoaded.emit(self.project)

            self.proj_name.setText("<b>"+os.path.split(os.path.split(dir)[0])[1]+"</b>")
            p: QPalette = self.proj_name.palette()
            p.setColor(QPalette.WindowText, QColor(0, 0, 200))
            self.proj_name.setPalette(p)
        else:
            ErrorBox(**ErrorBox.E003).exec()

    def save_proj(self):
        if self.project is not None:
            self.project.save()
        else:
            ErrorBox(**ErrorBox.E001).exec()

