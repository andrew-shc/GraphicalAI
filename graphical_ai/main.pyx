import sys
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

import main_window

"""
Library Import:

PySide6 - GUI
Numpy - Basic data operation / Simple models
Tensorflow - AI & ML models / Complex models
Matplotlib - Data visualization
Missingno - Missing Data visualization
Pandas - Large dataset management
"""

cdef void main():
    app = QApplication(sys.argv)
    app.setApplicationName("GraphicalAI-II")
    a_font = app.font()
    a_font.setPointSize(9)  # using PointSize to prevent automatically change the text (in this case, too small)
    app.setFont(a_font)

    win = main_window.MainWindow("GraphicalAI")

    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
else:
    main()
