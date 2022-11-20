import os

from PyQt5 import uic
from PyQt5.QtCore import QMutex
import sys
from main_view import *
from Graphics2D import *
from PyQt5.QtWidgets import QFileDialog, QScrollArea, QDialog, QMessageBox, QVBoxLayout,QLabel
from PyQt5.QtWidgets import QTableWidgetItem
from controller.Controller import KnnController
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import numpy as np

#qt_creator_file = "main_view.ui"
qt_creator_file = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "main_view.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Espere, se esta corriendo el Algoritmo")
        self.layout = QVBoxLayout()
        message = QLabel("Esta ventana se cerrara automaticamente cuando termine")
        self.layout.addWidget(message)
        self.setFixedSize(400, 80)



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionAbrir.triggered.connect(self.abrir)
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.run_alg)
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(2, 120)
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
        self.dialog = Dialog(self)

    def show_dialog(self):
          # self hace referencia al padre
        self.dialog.show()

    def close_dialog(self):
        self.dialog.close()
    def checked_item(self):
        if self.k_slider.isEnabled():
            self.k_slider.setEnabled(False)
            self.label_value.setEnabled(False)
        else:
            self.k_slider.setEnabled(True)
            self.label_value.setEnabled(True)

    def run_alg(self):
        self.show_dialog()
        self.controller.run_algorith(self.get_file(),int(self.label_value.text()))
        if self.grafico1.count() > 0:
            self.grafico1.removeWidget(self.grafica1)
            self.grafico1.removeWidget(self.toolbar_knn)
            self.grafico3.removeWidget(self.grafica3)
            self.grafico3.removeWidget(self.toolbar_knn_pon)
            self.grafico2.removeWidget(self.grafica2)
            self.grafico2.removeWidget(self.toolbar_dataset)
            self.error_layout1.removeWidget(self.grafico_errores)
            self.error_layout2.removeWidget(self.grafico_errores_pond)
        if self.layout_k_sel_pon.count() > 0:
            self.layout_k_sel_pon.removeWidget(self.grafica_k_sel_pon)
            self.layout_k_sel_pon.removeWidget(self.toolbar_k_sel_pon)
            self.layout_k_sel.removeWidget(self.toolbar_k_sel)
            self.layout_k_sel.removeWidget(self.grafica_k_sel)
        #Grafico K optimo KNN
        self.grafica1 = Canvas_grafica(self.controller)
        self.toolbar_knn = NavigationToolbar(self.grafica1, self)
        self.grafico1.addWidget(self.toolbar_knn)
        self.grafico1.addWidget(self.grafica1)
        #Grafico KNN POND K opt
        self.grafica3 = Canvas_grafica3(self.controller)
        self.toolbar_knn_pon = NavigationToolbar(self.grafica3, self)
        self.grafico3.addWidget(self.toolbar_knn_pon)
        self.grafico3.addWidget(self.grafica3)
        # Grafico Dataset
        self.grafica2 = Canvas_grafica2(self.controller)
        self.toolbar_dataset = NavigationToolbar(self.grafica2, self)
        self.grafico2.addWidget(self.toolbar_dataset)
        self.grafico2.addWidget(self.grafica2)
        #Grafico Errores knn
        self.errore_pond = GraficoErrores(self.controller.run_algorithm_of_k_optim_ponderated(self.get_file(),4), "Errores Alg. KNN Ponderado")
        self.grafico_errores_pond = self.errore_pond
        self.grafico_errores = GraficoErrores(self.controller.run_algorithm_k_optim(self.get_file(), 4),"Errores Alg. KNN")
        self.error_layout1.addWidget(self.grafico_errores)
        self.error_layout2.addWidget(self.grafico_errores_pond)
        self.k_value.setText(" "+str(self.grafica1.get_koptim()))
        self.k_value_2.setText(" "+str(self.grafica3.get_koptim()))
        self.k_value_4.setText(" " + self.label_value.text())
        self.k_value_5.setText(" " + self.label_value.text())
        self.errores1.setText(" " + str(self.controller.get_error_k_pon()))
        self.errores2.setText(" " + str(self.controller.get_error_k_pon_opt()))
        self.errores3.setText(" " + str(self.controller.get_error_k_elect()))
        self.errores4.setText(" " + str(self.controller.get_error_k_pond_elect()))
        if int(self.label_value.text()) != 0:
            self.grafica_k_sel_pon = Canvas_grafica_k_pond_sel(self.controller)
            self.toolbar_k_sel_pon = NavigationToolbar(self.grafica_k_sel_pon, self)
            self.layout_k_sel_pon.addWidget(self.toolbar_k_sel_pon)
            self.layout_k_sel_pon.addWidget(self.grafica_k_sel_pon)
            self.grafica_k_sel = Canvas_grafica_k_sel(self.controller)
            self.toolbar_k_sel = NavigationToolbar(self.grafica_k_sel, self)
            self.layout_k_sel.addWidget(self.toolbar_k_sel)
            self.layout_k_sel.addWidget(self.grafica_k_sel)
        self.close_dialog()

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




# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     app.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()