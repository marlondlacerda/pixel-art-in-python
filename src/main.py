from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

from functools import partial
from random import randint
import sys

from design.design import Ui_PaletaDeCores

default_border = "border: 1px solid black"


class PaletaDeCores(QMainWindow, Ui_PaletaDeCores):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self._color_brush = "#000000"

        self._put_random_color_on_buttons()
        self._create_connections()
        self._generate_board_size()

    def _create_connections(self):
        self.btnCreateBoard.clicked.connect(self._input_board_size)
        self.btnNewColor.clicked.connect(self._put_random_color_on_buttons)
        self.btnEraseBoard.clicked.connect(self._eraser_board)

        self.btnColorWhite.clicked.connect(
            partial(self._get_color_of_button, self.btnColorWhite)
        )

        self.btnColorBlack.clicked.connect(
            partial(self._get_color_of_button, self.btnColorBlack)
        )

        for i in range(1, 4):
            btnColorRdm = getattr(self, f"btnColorRndm{i}")
            btnColorRdm.clicked.connect(
                partial(self._get_color_of_button, btnColorRdm)
            )

    def _get_color_of_button(self, button):
        style = button.styleSheet()
        color = style[style.find("background-color:") + 18 : style.find(";")]
        self._color_brush = color

    @staticmethod
    def _generate_random_color():
        return "#%06x" % randint(0, 0xFFFFFF)

    def _input_board_size(self):
        try:
            quantity = int(self.inputBoardSize.toPlainText())
            if quantity > 50:
                quantity = 50
            elif quantity < 5:
                quantity = 5

            self._delete_all_board()
            self._generate_board_size(quantity)

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Erro ao inserir o tamanho do tabuleiro.")
            msg.setInformativeText("Valor inválido!")
            msg.setWindowTitle("Warning")
            msg.exec_()

    def _check_quantity(self, quantity):
        if quantity > 25:
            if 400 % quantity == 0:
                size = round(400 / quantity)
                self._change_board_size(30, 230, 400)
                return size
            else:
                size = round(380 / quantity)
                new_size = size * quantity
                self._change_board_size(30, 230, new_size)
                return size
        else:
            if 200 % quantity == 0:
                size = round(200 / quantity)
                self._change_board_size(125, 235, 200)
                return size
            else:
                size = round(200 / quantity)
                new_size = size * quantity
                self._change_board_size(125, 235, new_size)
                return size

    def _generate_board_size(self, quantity=5):
        size = self._check_quantity(quantity)

        for i in range(quantity):
            for j in range(quantity):
                self._create_board(self.board, i, j, size)

    def _change_board_size(self, i, j, size=200):
        self.board.setGeometry(i, j, size, size)

    def _eraser_board(self):
        for child in self.board.children():
            child.setStyleSheet(
                f"""
        QPushButton {{
            background-color: white;
            {default_border};
        }}
    """
            )

    def _create_board(self, board, i, j, size):
        btn = QPushButton(board)
        btn.setStyleSheet(
            f"""
        QPushButton {{
            background-color: white;
            {default_border};
        }}
    """
        )
        btn.setGeometry(i * size, j * size, size, size)
        btn.clicked.connect(partial(self._paint_board, btn))
        btn.show()

    def _delete_all_board(self):
        for child in self.board.children():
            child.deleteLater()

    def _paint_board(self, btn):
        btn.setStyleSheet(
            f"""
        QPushButton {{
            background-color: {self._color_brush};
            {default_border};
        }}
    """
        )

    def _put_random_color_on_buttons(self):
        for i in range(1, 4):
            btnColorRdm = getattr(self, f"btnColorRndm{i}")
            btnColorRdm.setStyleSheet(
                f"""
        QPushButton {{
            background-color: {self._generate_random_color()};
            {default_border};
        }}
        QPushButton:hover {{
            border: 2px solid rgb(255, 85, 85);
        }}
    """
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    paleta = PaletaDeCores()
    paleta.show()
    app.exec_()
