# Grafica 2D con linea
import numpy as np
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtCore
import matplotlib.pyplot as plt

from controller.Controller import KnnController


### open file

# file = open('../datasets/dataset1.csv')
# file = open('../datasets/dataset2.csv')
# file = open('../datasets/dataset3.csv')

def open_file_data(self, path_dataset):
    with open(path_dataset[0], 'r') as file:
        print(file)
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        print(header)
        rows = []
        for row in csvreader:
            rows.append(row)
            # print('row: ', row)
        # print(rows)
        data = np.array(rows)
        data_float = data.astype(float)
    return data_float


def get_data_porc(data, porcent):
    rows = []
    cont = 0
    range_loop = int(len(data) * porcent)
    for x in range(range_loop):
        rows.append(data[x])
        # print('row: ', row)
    # print('80 porc of data: ', rows)
    print('tamaño de rows: ', len(rows))
    return rows
def grafica_datos1(canvas,data):
    #data = self.controller.get_point_to_plot()
    # grafica el resultado del algoritmo
    x = data[:, [0, 1, 2]]
    y = data[:, -1].astype(int)
    plt.title("Clasificación con K optimo")
    plt.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=4, c='red')
    plt.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=4, c='blue')
    plt.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=4, c='g')
    plt.scatter(x[:, 0][y == -100], x[:, 1][y == -100], s=4, c='orange')
    plt.scatter(x[:, 0][y == -1], x[:, 1][y == -1], s=4, c='turquoise')
    plt.scatter(x[:, 0][y == -2], x[:, 1][y == -2], s=4, c='y')
    canvas.draw()


class Canvas_grafica2(FigureCanvas):
        def __init__(self,controller, parent=None):
            self.fig, self.ax = plt.subplots(facecolor='gray')
            super().__init__(self.fig)
            self.ax.grid()
            self.ax.margins(x=0)
            self.controller = controller
            print("data desde vista grafics init", self.controller.get_point())
            grafica_datos1(self,self.controller.get_point())

        def grafica_datos(self):
            # grafica el resultado del algoritmo
            data = self.controller.get_point()
            x = data[:, [0, 1, 2]]
            y = data[:, -1].astype(int)
            plt.title("Dataset Original")
            self.ax.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=3, c='r')
            self.ax.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=3, c='b')
            self.ax.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=3, c='y')
            self.draw()




class Canvas_grafica(FigureCanvas):

    def __init__(self, controller, parent=None):
        self.fig, self.ax = plt.subplots(facecolor='gray')
        super().__init__(self.fig)
        self.ax.grid()
        self.ax.margins(x=0)
        self.controller = controller
        grafica_datos1(self,self.controller.get_point_to_plot())


    def grafica_datos(self):

        data = self.controller.get_point_to_plot()
        # grafica el resultado del algoritmo
        x = data[:, [0, 1, 2]]
        y = data[:, -1].astype(int)
        plt.title("Clasificación con K optimo")
        plt.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=4, c='red')
        plt.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=4, c='blue')
        plt.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=4, c='g')
        plt.scatter(x[:, 0][y == -100], x[:, 1][y == -100], s=4, c='orange')
        plt.scatter(x[:, 0][y == -1], x[:, 1][y == -1], s=4, c='turquoise')
        plt.scatter(x[:, 0][y == -2], x[:, 1][y == -2], s=4, c='y')
        self.draw()

    def get_koptim(self):
        return self.controller.get_k_optim_value_from_controller()


