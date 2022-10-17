# Grafica 2D con linea
import numpy as np
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtCore
import matplotlib.pyplot as plt
### open file

# file = open('../datasets/dataset1.csv')
# file = open('../datasets/dataset2.csv')
# file = open('../datasets/dataset3.csv')

def open_file_data(filename):
    # file = open('../datasets/' + filename)
    file = open('../datasets/' + filename)
    type(file)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
        # print('row: ', row)
    # print(rows)
    file.close()
    data = np.array(rows)
    data_float = data.astype(float)
    return data_float

def get_data_porc(data, porcent):
    rows = []
    cont = 0
    range_loop = int(len(data)*porcent)
    for x in range(range_loop):
        rows.append(data[x])
        # print('row: ', row)
    #print('80 porc of data: ', rows)
    print('tamaño de rows: ', len(rows))
    return rows


class Canvas_grafica2(FigureCanvas):
    def plot_dataset():
        def __init__(self, parent=None):     
            self.fig , self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), 
                sharey=True, facecolor='white')
            super().__init__(self.fig) 
        data = open_file_data('dataset1.csv')
        #get_data_porc(data, 0.8)

        #for x in range(len(data)):


        x = data[:, [0, 1,2]]
        y = data[:, -1].astype(int)

        print('La data: ', data)



        plt.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=3, c='r')
        plt.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=3, c='b')
        plt.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=3, c='y')

class Canvas_grafica(FigureCanvas):
    def __init__(self, parent=None):     
        self.fig , self.ax = plt.subplots(facecolor='gray')
        super().__init__(self.fig) 
        self.ax.grid()
        self.ax.margins(x=0)
        self.grafica_datos()

    def grafica_datos(self):
        data = open_file_data('dataset1.csv')
        #get_data_porc(data, 0.8)

        #for x in range(len(data)):
        x = data[:, [0, 1,2]]
        y = data[:, -1].astype(int)
        plt.title("Grafica")
        self.ax.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=3, c='r')
        self.ax.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=3, c='b')
        self.ax.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=3, c='y')
        self.draw()     
        QtCore.QTimer.singleShot(10, self.grafica_datos)

