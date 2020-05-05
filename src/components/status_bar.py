from PyQt5.QtWidgets import QStatusBar, QLabel, QPushButton


# changes for each different page
class CustomStatus(QStatusBar):
    def __init__(self):
        super().__init__()

        self.addPermanentWidget(QLabel("v0.16.1"))
        # self.addWidget(QLabel("Status 2"))
        # p = QPushButton("Show ABC's")
        # self.addWidget(p)
        # p.clicked.connect(lambda checked: self.showMessage("abc", 5 * 1000))
        # p.clicked.connect(lambda checked: self.showMessage("two", 5 * 1000))

