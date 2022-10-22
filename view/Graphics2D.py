# Grafica 2D con linea
import numpy as np
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from controller.Controller import KnnController
import matplotlib


def grafica_datos1(canvas,data,title):
    #data = self.controller.get_point_to_plot()
    # grafica el resultado del algoritmo
    x = data[:, [0, 1, 2]]
    y = data[:, -1].astype(int)
    plt.title(title)
    plt.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=4, c='red')
    plt.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=4, c='blue')
    plt.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=4, c='g')
    plt.scatter(x[:, 0][y == -100], x[:, 1][y == -100], s=4, c='orange')
    plt.scatter(x[:, 0][y == -1], x[:, 1][y == -1], s=4, c='turquoise')
    plt.scatter(x[:, 0][y == -2], x[:, 1][y == -2], s=4, c='y')
    canvas.draw()

def grafica_errores(canvas,title):
    #data = self.controller.get_point_to_plot()
    # grafica el resultado del algoritmo
    xpoints = np.array([1, 2, 6, 8])
    ypoints = np.array([3, 8, 1, 10])

    plt.plot(xpoints, ypoints)
    plt.title(title)
    canvas.draw()


class Canvas_grafica2(FigureCanvas):
        def __init__(self,controller, parent=None):
            self.fig, self.ax = plt.subplots(facecolor='gray')
            super().__init__(self.fig)
            self.ax.grid()
            self.ax.margins(x=0)
            self.controller = controller
            print("data desde vista grafics init", self.controller.get_point())
            grafica_datos1(self,self.controller.get_point(),"Dataset Original")




class Canvas_grafica(FigureCanvas):

    def __init__(self, controller, parent=None):
        self.fig, self.ax = plt.subplots(facecolor='gray')
        super().__init__(self.fig)
        self.ax.grid()
        self.ax.margins(x=0)
        self.controller = controller
        grafica_datos1(self,self.controller.get_point_to_plot(),"Clasificación con K optimo")

    def get_koptim(self):
        return self.controller.get_k_optim_value_from_controller()


class GraficoErrores(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(facecolor='white')
        super().__init__(self.fig)
        self.ax.grid()
        self.ax.margins(x=0)
        grafica_errores(self,"Errores de clasificacion")
