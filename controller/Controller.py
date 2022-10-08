from math import sqrt
import numpy as np
import csv

class KnnController:

    def __init__(self):
        self.distances = []
        self.dataset = [[-5, -2, 0],
                        [-7, -3, 0],
                        [-8, -1, 0],
                        [-3, -8, 1],
                        [-2, -9, 1],
                        [-4, -7, 1]]

        # Struct vector point
        # [x,y,class,distance]

    def __repr__(self):
        return str(self.__dict__)

    # distancia entre pares de valores (x,y)
    def euclidean_distance(self, vector1, vector2):
        # print('v3ctor 1: ', vector1)
        # print('v3ctor 2: ', vector2)
        return sqrt((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2)

    def get_neighbors(self, point, dataset):
        distances = list()
        for pair_dataset in dataset:
            distance = self.euclidean_distance(point, pair_dataset)
            self.distances.append((pair_dataset, distance))
        self.distances.sort(key=lambda tup: tup[1])
        print('Vector with distances ::: ', self.distances)
        return self.distances

    def get_class_ponderated(self, neighbors: list):
        freq1 = 0
        freq2 = 0
        for i in range(len(neighbors)):
            if neighbors[i][0][2] == 1:
                print('La distancia: ', neighbors[i][1])
                if neighbors[i][1] != 0:  # not division by zero
                    freq1 += 1 / neighbors[i][1]
            else:
                freq2 += 1
        if freq1 > freq2:
            return 1
        else:
            return 0

    def validate_class(self, class_eval, class_target):
        # print('class taget: ', class_target[0][2])
        if (class_eval == class_target[0][2]):
            return 1
        else:
            return 0

    def get_class(self, neighbors: list, k):
        class_0 = 0
        class_1 = 0
        range_k = range(k)
        array_of_k_elements = [neighbors[i] for i in range_k]
        print('primeros k elementos: ', array_of_k_elements)
        class_0 = sum(self.validate_class(0, x) for x in array_of_k_elements)
        class_1 = sum(self.validate_class(1, x) for x in array_of_k_elements)
        print('class 0 quantity: ', class_0)
        print('class 1 quantity: ', class_1)
        if class_0 > class_1:
            return 0
        else:
            return 1

        # for i in range(len(neighbors)):
        #     print('value in matrix: ', neighbors[i][0][2])
        #     if neighbors[i][0][2] == 1:
        #         class_0 += 1
        #     else:
        #         class_1 += 1
        # if class_0 > class_1:
        #     return 1
        # else:
        #     return 0

    def get_k_optim(self, data_points: list):
        print('El dataset: ', data_points)
        quantity_points = len(data_points)
        # declarando la matrix nxn
        matrix_distances = [[0 for x in range(quantity_points)] for y in range(quantity_points)]
        for i in range(len(data_points)):
            for j in range(len(data_points)):
                if i == j:
                    matrix_distances[i][j] = 0
                elif i > j:
                    matrix_distances[i][j] = matrix_distances[j][i]
                else:
                    matrix_distances[i][j] = self.euclidean_distance(data_points[i], data_points[j])
        print('The matrix of distances: ', np.array(matrix_distances))
        # Hasta aqui la matriz de distancias

        # ahora ordenar matrix de distancias guardando el punto en cada celda
        matrix_order_points = [[0 for x in range(quantity_points)] for y in range(quantity_points)]
        for j in range(len(data_points)):
            for i in range(len(data_points)):
                # guardo los puntos de encabezado de la tabla
                if i == 0:
                    matrix_order_points[i][j] = data_points[j]
                else:
                    matrix_order_points[i][j][0] = matrix_distances[i][j]
                    matrix_order_points[i][j][1] = data_points[j]

    def run_algorith(self):
        point_unknowkn = [2, 1]
        neighbors = self.get_neighbors(point_unknowkn, self.dataset)
        print('neighbors quantity: ', len(neighbors))
        class_result = self.get_class(neighbors, 3)
        print('Clasifica como clase: ', class_result)

        data = self.open_file_data('dataset4.csv')
        print('Data leida CSV: ', data)
        # print('Data 1: ', data[0])
        # [-5. -2.  0.]

        self.get_k_optim(data)

        # print('lista de vecinos: ', neighbors)
        # classif = self.get_class_ponderated(neighbors)
        # print('THE CLASS CLASSIFIED TO UNKNOWN POINT IS: ', classif)

        # for neighbor in neighbors:
        #    print(neighbor)


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