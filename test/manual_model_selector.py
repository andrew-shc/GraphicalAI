from test.prelude import GUICentral

from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from src.widgets import ModelWorkspaceSelector

class A:
    def __init__(self, s):
        self.name=s

class _TestSelector(GUICentral):
    def __init__(self):
        super().__init__()
        lt = [A("ab"), A("abc"), A("noo")]
        mdl = ModelWorkspaceSelector(lt)

        b_ind = QPushButton("Index")
        b_ind.clicked.connect(lambda x: print("CLICKED", mdl.currentIndex(), ))

        def incr():
            lt.append(A(str(len(lt))))
            print("NEW", mdl._update_list(lt))

        b_new = QPushButton("New")
        b_new.clicked.connect(lambda x: incr())

        self.layout = QVBoxLayout()
        self.layout.addWidget(mdl)
        self.layout.addWidget(b_ind)
        self.layout.addWidget(b_new)


if __name__ == '__main__':
    x = _TestSelector()
    x.run()