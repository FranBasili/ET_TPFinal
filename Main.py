from PyQt5.QtWidgets import QApplication
from src.UI_Core import MyApp
import sys

app = QApplication([])
window = MyApp()
window.show()
sys.exit(app.exec_())
