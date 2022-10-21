import numpy as np
import matplotlib.pyplot as plt
import csv


### open file

# file = open('../datasets/dataset1.csv')
# file = open('../datasets/dataset2.csv')
# file = open('../datasets/dataset3.csv')

class Graphics:

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)

    def plot_dataset(self, data):
        # data = self.open_file_data('dataset1.csv')
        # get_data_porc(data, 0.8)

        # for x in range(len(data)):

        x = data[:, [0, 1, 2]]
        y = data[:, -1].astype(int)

        print('La data: ', data)

        plt.scatter(x[:, 0][y == 0], x[:, 1][y == 0], s=4, c='red')
        plt.scatter(x[:, 0][y == 1], x[:, 1][y == 1], s=4, c='blue')
        plt.scatter(x[:, 0][y == 2], x[:, 1][y == 2], s=4, c='g')

        plt.scatter(x[:, 0][y == -100], x[:, 1][y == -100], s=4, c='orange')
        plt.scatter(x[:, 0][y == -1], x[:, 1][y == -1], s=4, c='turquoise')
        plt.scatter(x[:, 0][y == -2], x[:, 1][y == -2], s=4, c='y')

        plt.show()


    def open_file_data(self, filename):
        # file = open('../datasets/' + filename)
        file = open('./datasets/' + filename)
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