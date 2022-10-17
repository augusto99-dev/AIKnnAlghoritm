from main_view import *
from Graphics2D import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
import csv
import numpy as np

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.actionAbrir.triggered.connect(self.abrir)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,100) 
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(("X","Y","CLASE"))
        self.grafica = Canvas_grafica()
        self.grafico_1 = Canvas_grafica2()
        self.grafico1.addWidget(self.grafica)

    def open_file(self,archivo):
        with open(archivo[0], 'r') as file:
            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)
            rows = [] 
            n=0
            item=0
            self.tableWidget.setRowCount(600)
            for row in csvreader:
               self.tableWidget.setItem(n,item,QTableWidgetItem(row[0]))
               item+=1
               self.tableWidget.setItem(n,item,QTableWidgetItem(row[1]))
               item+=1
               self.tableWidget.setItem(n,item,QTableWidgetItem(row[2]))
               item+=1
               n+=1
               item=0
            data = np.array(rows)
            return data

    def abrir(self):
        archivo = QFileDialog.getOpenFileName(self,'abrir archivo','C:\\')
        if archivo[0]:
            data = self.open_file(archivo)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()