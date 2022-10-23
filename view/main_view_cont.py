from PyQt5 import uic
from PyQt5.QtCore import QMutex
import sys
from controller.Controller import KnnController
from main_view import *
from Graphics2D import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
import csv
import numpy as np

qt_creator_file = "main_view.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionAbrir.triggered.connect(self.abrir)
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.run_alg)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(("X", "Y", "CLASE"))
        self.k_slider.valueChanged.connect(self.label_value.setNum)
        self.label_value.setText("0")
        self.checkBox.stateChanged.connect(self.checked_item)
        self.k_slider.setEnabled(False)
        self.label_value.setEnabled(False)
        self.controller = KnnController()
        self.grafica = None
        self.dataset = None
        self.grafico_errores = None
        self.dataset_points = None
        self.mutex = QMutex()

    def checked_item(self):
        if self.k_slider.isEnabled():
            self.k_slider.setEnabled(False)
            self.label_value.setEnabled(False)
        else:
            self.k_slider.setEnabled(True)
            self.label_value.setEnabled(True)

    def run_alg(self):
        self.controller.run_algorith(self.get_file(),int(self.label_value.text()))
        self.grafica1 = Canvas_grafica(self.controller)
        self.grafico1.addWidget(self.grafica1)
        self.grafica2 = Canvas_grafica2(self.controller)
        self.grafico3.addWidget(self.grafica2)
        self.grafica3 = Canvas_grafica3(self.controller)
        self.grafico2.addWidget(self.grafica3)
        self.grafico_errores_pond = GraficoErrores(self.controller.run_algorithm_of_k_optim_ponderated(self.get_file(),4), "Errores Alg. KNN Ponderado")
        self.grafico_errores = GraficoErrores(self.controller.run_algorithm_k_optim(self.get_file(), 4),"Errores Alg. KNN")
        self.error_layout1.addWidget(self.grafico_errores)
        self.error_layout2.addWidget(self.grafico_errores_pond)
        self.k_value.setText(" "+str(self.grafica1.get_koptim()))
        self.k_value_2.setText(" "+str(self.grafica3.get_koptim()))
        if int(self.label_value.text()) != 0:
            self.grafica_k_sel_pon = Canvas_grafica_k_pond_sel(self.controller)
            self.layout_k_sel_pon.addWidget(self.grafica_k_sel_pon)
            self.grafica_k_sel = Canvas_grafica_k_sel(self.controller)
            self.layout_k_sel.addWidget(self.grafica_k_sel)
    def open_file(self, archivo):
        with open(archivo[0], 'r') as file:
            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)
            rows = []
            n = 0
            item = 0
            self.tableWidget.setRowCount(600)
            for row in csvreader:
                self.tableWidget.setItem(n, item, QTableWidgetItem(row[0]))
                item += 1
                self.tableWidget.setItem(n, item, QTableWidgetItem(row[1]))
                item += 1
                self.tableWidget.setItem(n, item, QTableWidgetItem(row[2]))
                item += 1
                n += 1
                item = 0
            file.close()
            return self.dataset

    def abrir(self):
        filters = "Text files (*.csv);;"
        self.dataset = QFileDialog.getOpenFileName(self, 'abrir archivo', 'C:\\',filters)
        if self.dataset[0]:
            data = self.open_file(self.dataset)
            self.pushButton.setEnabled(True)
        return self.dataset
    def get_file(self):
        return self.dataset[0]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
