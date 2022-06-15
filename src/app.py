import sys
from main import PaletaDeCores
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    paleta = PaletaDeCores()
    paleta.show()
    sys.exit(app.exec_())
