import sys
import sqlite3
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication,
                             QWidget, QDialog)
from PyQt5.QtGui import QPainter, QColor

class MyWidget_2(QMainWindow):
    def __init__(self, flag, dlina=''):
        super().__init__()
        self.flag = flag
        self.dlina = dlina
        self.initUI()

    def initUI(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        if not self.flag:
            self.label_7.setText('Введите название сорта кофе, который хотите изменить')
            self.pushButton.clicked.connect(self.clik)
        else:
            self.pushButton.clicked.connect(self.click)

    def click(self):
        self.label_7.setText('')
        if self.textEdit.toPlainText() and self.textEdit_2.toPlainText() and \
           self.textEdit_4.toPlainText() and self.textEdit_5.toPlainText() and \
           self.textEdit_6.toPlainText():
            zerna = ''
            if self.radioButton_2.isChecked():
                zerna = "Молотый"
            else:
                zerna = "Цельный"
            sp = (self.dlina + 1, self.textEdit.toPlainText(), self.textEdit_2.toPlainText(),
                  zerna,
                  self.textEdit_4.toPlainText(), self.textEdit_5.toPlainText(),
                  self.textEdit_6.toPlainText())
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            resul = cur.execute('''INSERT INTO cofe(id, sort, objarka, vid,
                                vcus, cena, V) VALUES(?, ?, ?, ?, ?, ?, ?);''', sp)
            con.commit()
        else:
            self.label_7.setText('Неверные данные')
            

    def clik(self):
        self.label_7.setText('Введите название сорта кофе, который хотите изменить')
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        sp = 'UPDATE cofe SET' + '\n'
        if not self.textEdit.toPlainText():
            self.label_7.setText('Неверные данные')
        if self.textEdit_2.toPlainText():
            sp += 'objarka = "' + self.textEdit_2.toPlainText() + '", '
        if self.textEdit_4.toPlainText():
            sp += 'vcus = "' + self.textEdit_4.toPlainText() + '", '
        if self.textEdit_5.toPlainText():
            sp += 'cena = "' + self.textEdit_5.toPlainText() + '", '
        if self.textEdit_6.toPlainText():
            sp += 'V = "' + self.textEdit_6.toPlainText() + '", '
        if not self.flag:
            if self.radioButton_2.isChecked():
                sp += 'vid = "Молотый"'
            else:
                sp += 'vid = "Цельный"'
            sp += 'WHERE sort = "' + self.textEdit.toPlainText() + '"'
            # Робуста
            result = cur.execute(sp)
            con.commit()
        
        
        

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM cofe WHERE id > 0""").fetchall()
        sp = ['id', 'Название сорта', 'Обжарка',
              'Молотый/Цельный', 'Вкус', 'цена', 'Объём']

        #self.tableWidget = QTableWidget(self)
        #self.tableWidget.setGeometry(180, 10, 500, 280)
        self.tableWidget.setColumnCount(len(sp))
        self.tableWidget.setHorizontalHeaderLabels(sp)
        self.tableWidget.setRowCount(len(result))
        for y in range(len(result)):
            self.tableWidget.setItem(y, 0, QTableWidgetItem(str(result[y][0])))
            self.tableWidget.setItem(y, 1, QTableWidgetItem(result[y][1]))
            self.tableWidget.setItem(y, 2, QTableWidgetItem(str(result[y][2])))
            self.tableWidget.setItem(y, 3, QTableWidgetItem(str(result[y][3])))
            self.tableWidget.setItem(y, 4, QTableWidgetItem(str(result[y][4])))
            self.tableWidget.setItem(y, 5, QTableWidgetItem(str(result[y][5])))
            self.tableWidget.setItem(y, 6, QTableWidgetItem(str(result[y][6])))
        self.pushButton_3.clicked.connect(self.clik)
        self.pushButton_2.clicked.connect(self.ope)
        self.pushButton.clicked.connect(self.izmen)
        self.dlina = len(result)

    def clik(self):
        self.tableWidget.clear()
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM cofe WHERE id > 0""").fetchall()
        sp = ['id', 'Название сорта', 'Обжарка',
              'Молотый/Цельный', 'Вкус', 'цена', 'Объём']

        #self.tableWidget = QTableWidget(self)
        #self.tableWidget.setGeometry(180, 10, 500, 280)
        self.tableWidget.setColumnCount(len(sp))
        self.tableWidget.setHorizontalHeaderLabels(sp)
        self.tableWidget.setRowCount(len(result))
        for y in range(len(result)):
            self.tableWidget.setItem(y, 0, QTableWidgetItem(str(result[y][0])))
            self.tableWidget.setItem(y, 1, QTableWidgetItem(result[y][1]))
            self.tableWidget.setItem(y, 2, QTableWidgetItem(str(result[y][2])))
            self.tableWidget.setItem(y, 3, QTableWidgetItem(str(result[y][3])))
            self.tableWidget.setItem(y, 4, QTableWidgetItem(str(result[y][4])))
            self.tableWidget.setItem(y, 5, QTableWidgetItem(str(result[y][5])))
            self.tableWidget.setItem(y, 6, QTableWidgetItem(str(result[y][6])))

    def ope(self):
        self.dialog = MyWidget_2(True, self.dlina)
        self.dialog.show()

    def izmen(self):
        self.dialog = MyWidget_2(False)
        self.dialog.show()

    def stopDialog(self):
        self.dialog.destroy()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
