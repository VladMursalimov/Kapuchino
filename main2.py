import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mai12n.ui', self)
        self.updatebtn.clicked.connect(self.update1)
        self.con = sqlite3.connect('coffee.sqlite')
        self.edit_btn.clicked.connect(self.add_and_edit)
        self.cur = self.con.cursor()
        self.title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                      'описание вкуса', 'цена', 'объем упаковки']
        self.result = self.cur.execute("Select * FROM coffe").fetchall()
        print(self.result)
        self.coffeetable.setRowCount(0)
        self.coffeetable.setColumnCount(len(self.title))
        self.coffeetable.setHorizontalHeaderLabels(self.title)
        n = 0
        for i, j in enumerate(self.result):
            self.coffeetable.setRowCount(self.coffeetable.rowCount() + 1)
            for x in range(7):
                self.coffeetable.setItem(n, x, QTableWidgetItem(str(j[x])))
            n += 1
        self.coffeetable.resizeColumnsToContents()

    def add_and_edit(self):
        self.menu = EditMenu()
        self.menu.show()

    def update1(self):
        n = 0
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.coffeetable.setRowCount(0)
        self.result = self.cur.execute("Select * FROM coffe").fetchall()
        for i, j in enumerate(self.result):
            self.coffeetable.setRowCount(self.coffeetable.rowCount() + 1)
            for x in range(7):
                self.coffeetable.setItem(n, x, QTableWidgetItem(str(j[x])))
            n += 1
        self.coffeetable.resizeColumnsToContents()


class EditMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeFor12m.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.s = self.con.cursor().execute("Select * FROM coffe").fetchall()

        self.confirm_button.clicked.connect(self.editing)

    def editing(self):
        if len(self.s) >= int(self.id_input.text()):
            self.con.cursor().execute(
                f"UPDATE coffe SET\nsort='{self.name_input.text()}'\nWHERE id='{self.id_input.text()}'")
            self.con.cursor().execute(
                f"UPDATE coffe SET\nroasting='{self.frying_input.text()}'\nWHERE id='{self.id_input.text()}'")
            self.con.cursor().execute(
                f"UPDATE coffe SET\nground='{self.state_input.text()}'\nWHERE id='{self.id_input.text()}'")
            self.con.cursor().execute(
                f"UPDATE coffe SET\ntaste='{self.decribe_input.toPlainText()}'\nWHERE id='{self.id_input.text()}'")
            self.con.cursor().execute(
                f"UPDATE coffe SET\nprice='{self.price_input.text()}'\nWHERE id='{self.id_input.text()}'")
            self.con.cursor().execute(
                f"UPDATE coffe SET\nvolume='{self.volume_input.text()}'\nWHERE id='{self.id_input.text()}'")
            self.con.commit()
        else:
            s = f"""INSERT INTO coffe 
            VALUES ({int(self.id_input.text())}, '{self.name_input.text()}', {int(self.frying_input.text())},
                         {int(self.state_input.text())}, '{self.decribe_input.toPlainText()}',
                        '{self.price_input.text()} ₽','{self.volume_input.text()} г')"""
            self.con.cursor().execute(s)
            self.con.commit()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    exit(app.exec())
