class GUICentral:
    def __init__(self):
        from PyQt5.QtWidgets import QApplication, QMainWindow
        import sys

        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setWindowTitle("GUI TESTING")
        self.win.setGeometry(0, 0, 1920, 1080)

        self.layout = None  # set the layout and the child widgets to visualize via `run()`

    def run(self):
        if self.layout is None:
            print("Error: Layout is not set")
            return None

        from PyQt5.QtWidgets import QWidget
        import sys

        w = QWidget()
        w.setLayout(self.layout)
        self.win.setCentralWidget(w)

        self.win.show()
        sys.exit(self.app.exec_())
