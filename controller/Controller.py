import copy
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
        self.point_to_plot = None
        self.points_csv = None
        self.k_optimo = None

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
        # print('Vector with distances ::: ', self.distances)
        self.distances.sort(key=lambda tup: tup[1])
        return self.distances

    def get_neighbors_of_trainee_data(self, point, dataset):
        distances = list()
        # for 80% Clase 0
        for i in range(0, 160):
            distance = self.euclidean_distance(point, dataset[i])
            self.distances.append((dataset[i], distance))
        # for 80% Clase 1
        for i in range(200, 360):
            distance = self.euclidean_distance(point, dataset[i])
            self.distances.append((dataset[i], distance))
        # for 80% Clase 2
        for i in range(400, 560):
            distance = self.euclidean_distance(point, dataset[i])
            self.distances.append((dataset[i], distance))
        print('Vector with distances TRAINEE DATA ::: ', self.distances)
        self.distances.sort(key=lambda tup: tup[1])
        return self.distances

    # deprecated
    def get_class_ponderated_old(self, neighbors: list):
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
    # cambia el formato que llega la data
    def validate_class_of_ponderated(self, class_eval, class_target):
        # print('class taget: ', class_target[0][2])
        if (class_eval == class_target):
            return 1
        else:
            return 0

    def get_class_ponderated(self, neighbors: list, k):
        class_0 = 0
        class_1 = 0
        class_2 = 0
        range_k = range(k)
        array_of_k_elements = [neighbors[i] for i in range_k]
        # print('primeros k elementos: ', array_of_k_elements)

        for i in range(0, k):
            if neighbors[i][1] != 0:  # not division by zero
                # print('div: ', 1/neighbors[i][1])
                # print('el divisor: ', neighbors[i][1])
                # print('mult. por clase 0 ', self.validate_class(0, neighbors[i]))
                class_0 += 1/neighbors[i][1] * self.validate_class(0, neighbors[i])
                class_1 += 1/neighbors[i][1] * self.validate_class(1, neighbors[i])
                class_2 += 1/neighbors[i][1] * self.validate_class(2, neighbors[i])
            print('class 0 quantity: ', class_0)
            print('class 1 quantity: ', class_1)
            print('class 2 quantity: ', class_2)


        #print('class 0 quantity: ', class_0)
        #print('class 1 quantity: ', class_1)
        #print('class 2 quantity: ', class_2)

        if class_2 > class_1 and class_2 > class_0:
            return 2
        elif class_1 > class_0 and class_1 > class_2:
            return 1
        elif class_0 > class_1 and class_0 > class_2:
            return 0
        else:
            return 1


    def get_class_ponderated_old_2(self, neighbors: list, k):
        class_0 = 0
        class_1 = 0
        class_2 = 0
        range_k = range(k)
        array_of_k_elements = [neighbors[i] for i in range_k]
        #print('primeros k elementos: ', array_of_k_elements)

        for i in range(len(neighbors)):
            if neighbors[i][1] != 0:  # not division by zero
                class_0 += 1/neighbors[i][1] * self.validate_class(0, neighbors[i])
                class_1 += 1/neighbors[i][1] * self.validate_class(1, neighbors[i])
                class_2 += 1/neighbors[i][1] * self.validate_class(2, neighbors[i])
            print('class 0 quantity: ', class_0)
            print('class 1 quantity: ', class_1)
            print('class 2 quantity: ', class_2)


        #print('class 0 quantity: ', class_0)
        #print('class 1 quantity: ', class_1)
        #print('class 2 quantity: ', class_2)

        if class_0 > class_1 and class_0 > class_2:
            return 0
        elif class_1 > class_0 and class_1 > class_2:
            return 1
        else:
            return 2

    def get_class(self, neighbors: list, k):
        class_0 = 0
        class_1 = 0
        class_2 = 0
        range_k = range(k)
        array_of_k_elements = [neighbors[i] for i in range_k]
        # print('primeros k elementos: ', array_of_k_elements)
        class_0 = sum(self.validate_class(0, x) for x in array_of_k_elements)
        class_1 = sum(self.validate_class(1, x) for x in array_of_k_elements)
        class_2 = sum(self.validate_class(2, x) for x in array_of_k_elements)

        print('class 0 quantity: ', class_0)
        print('class 1 quantity: ', class_1)
        print('class 2 quantity: ', class_2)

        if class_0 > class_1 and class_0 > class_2:
            return 0
        elif class_1 > class_0 and class_1 > class_2:
            return 1
        else:
            return 2

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

    def get_k_optim(self, data_points):
        print('El dataset: ', data_points)
        quantity_points = len(data_points)
        # declarando la matrix nxn
        matrix_distances = [[0 for x in range(quantity_points)] for y in range(quantity_points)]
        for i in range(len(data_points)):
            for j in range(len(data_points)):
                if i == j:
                    # guardo distancia que es 0, y su clase [2]
                    matrix_distances[i][j] = [0, data_points[i][2]]
                    # print('Data point j2 : ', data_points[i][2])

                    # matrix_distances[i][j] = 0
                    # print('PRINT AFFTER ERROR: ', matrix_distances[i][j])
                elif i > j:
                    # copio el valor ya calculado, pero como incluye su clase yo quiero solo la distancia ya que estamos tratando otra columna la clase cambia
                    matrix_distances[i][j] = [matrix_distances[j][i][0], data_points[i][2]]
                    # print('Data point i > j  : ', matrix_distances[i][j])
                    # matrix_distances[i][j] = matrix_distances[j][i]
                else:
                    aux = []
                    aux.append(float(self.euclidean_distance(data_points[i], data_points[j])))
                    aux.append(data_points[i][2])
                    # matrix_distances[i][j] = [self.euclidean_distance(data_points[i], data_points[j]), data_points[j][2]]
                    matrix_distances[i][j] = aux
                    # print('ELSE I < J: ', matrix_distances[i][j])

                    # matrix_distances[i][j] = self.euclidean_distance(data_points[i], data_points[j])

        print('The matrix of distances: ', np.array(matrix_distances))
        # Hasta aqui la matriz de distancias

        matrix_ordered = self.order_matrix_by_column(matrix_distances, len(matrix_distances), len(matrix_distances[0]))
        print('Matriz ordenada: ', np.array(matrix_ordered))
        # segundo parametro (len(matrix_distances)) parametro es el k variable
        matrix_of_ones = self.build_matrix_of_k(matrix_ordered, len(matrix_distances), len(matrix_distances[0]))
        k = self.get_row_max_k(matrix_of_ones)
        print('K OPTIMO: ', k)
        return k

    def get_k_optim_ponderated(self, data_points):
        matrix_ordered = self.get_matrix_of_distances_ordered(data_points)
        print('Matriz ordenada: ', np.array(matrix_ordered))
        # segundo parametro (len(matrix_distances)) parametro es el k variable
        matrix_of_ones = self.build_matrix_of_k_pondered(matrix_ordered, len(matrix_ordered), len(matrix_ordered[0]))
        k = self.get_row_max_k(matrix_of_ones)
        print('K OPTIMO: ', k)
        return k

    def get_matrix_of_distances_ordered(self, data_points):
        print('El dataset: ', data_points)
        quantity_points = len(data_points)
        # declarando la matrix nxn
        matrix_distances = [[0 for x in range(quantity_points)] for y in range(quantity_points)]
        for i in range(len(data_points)):
            for j in range(len(data_points)):
                if i == j:
                    # guardo distancia que es 0, y su clase [2]
                    matrix_distances[i][j] = [0, data_points[i][2]]
                    # print('Data point j2 : ', data_points[i][2])

                    # matrix_distances[i][j] = 0
                    # print('PRINT AFFTER ERROR: ', matrix_distances[i][j])
                elif i > j:
                    # copio el valor ya calculado, pero como incluye su clase yo quiero solo la distancia ya que estamos tratando otra columna la clase cambia
                    matrix_distances[i][j] = [matrix_distances[j][i][0], data_points[i][2]]
                    # print('Data point i > j  : ', matrix_distances[i][j])
                    # matrix_distances[i][j] = matrix_distances[j][i]
                else:
                    aux = []
                    aux.append(float(self.euclidean_distance(data_points[i], data_points[j])))
                    aux.append(data_points[i][2])
                    # matrix_distances[i][j] = [self.euclidean_distance(data_points[i], data_points[j]), data_points[j][2]]
                    matrix_distances[i][j] = aux
                    # print('ELSE I < J: ', matrix_distances[i][j])

                    # matrix_distances[i][j] = self.euclidean_distance(data_points[i], data_points[j])

        print('The matrix of distances: ', np.array(matrix_distances))
        # Hasta aqui la matriz de distancias
        matrix_ordered = self.order_matrix_by_column(matrix_distances, len(matrix_distances), len(matrix_distances[0]))
        return matrix_ordered


    def get_row_max_k(self, matrix):
        result = []
        for i in range(len(matrix)):
            # print('fil.', i)
            sum_aux = 0
            for j in range(len(matrix) + 1):
                # print('col.', j)
                sum_aux += matrix[i][j]
            result.append(sum_aux)
            # print('Suma fila: ', sum_aux)
        print('Array de k values rows: ', np.array(result))
        tmp = max(result)
        k = result.index(tmp) + 1  # + 1 porque usamos los indices de arreglos!
        print('Valor maximo: ', tmp)
        print('K Optimo:::: ', k)

        # my_list = [10, 72, 54, 25, 73, 40]
        max_item = max(result)
        print(f'Max index is : {result.index(max_item)}')
        return k

    def build_matrix_of_k(self, matrix_ordered, R, C):
        # matriz con una fila menos
        res = [[0] * C for _ in range(R - 1)]
        c0 = 0
        c1 = 0
        c2 = 0
        for col in range(C):
            values = [r[col] for r in matrix_ordered]
            values.sort(key=lambda s: s[0], reverse=True)
            # print('VALUES ordenada en teoria para comparar los c0 y c1: ', values)
            # print('columna::::: ', col)
            # obtengo la clase dueña de la columna
            item_owner = values.pop()
            for i in range(1, R):
                # for i = 1 in range(R):
                # print('ITERATOR: ', i)
                # obtengo la clase
                item = values.pop()
                # print('The Class in matrix ordered: ', item[1])
                if int(item[1]) == 0:
                    c0 += 1
                elif int(item[1]) == 1:
                    c1 += 1
                elif int(item[1]) == 2:
                    c2 += 1
                else:
                    print('no deberia llegar aqui')
                # print('Hasta el momento: ')
                # print('c0: ', c0)
                # print('c1: ', c1)
                # print('c2: ', c2)
                if c0 > c1 and c0 > c2:
                    if int(item_owner[1]) == 0:
                        # print('Cargo 1 en la matrix, gano c0')
                        res[i - 1][col] = 1
                    else:
                        # print('Cargo 0 en la matrix porque la clase 1 no gano y aca comparo por la clase 1.')
                        res[i - 1][col] = 0
                elif c0 < c1 and c2 < c1:
                    if int(item_owner[1]) == 1:
                        # print('Cargo 1 en la matrix, gano c1')
                        res[i - 1][col] = 1
                    else:
                        # print('Cargo 0 en la matrix porque la c0 o c1 gano y aca comparo por la clase 1.')
                        res[i - 1][col] = 0
                elif c2 > c1 and c2 > c0:
                    if int(item_owner[1]) == 2:
                        # print('Cargo 1 en la matrix gano c2.')
                        res[i - 1][col] = 1
                    else:
                        # print('Cargo 0 en la matrix porque la clase c2 no gano y aca comparo por la clase 2.')
                        res[i - 1][col] = 0
                else:
                    # Aca cuando no se puede decidir por ser iguales.
                    res[i - 1][col] = 0
            c0 = 0
            c1 = 0
            c2 = 0
        print('Final matrix:: ', np.array(res))
        return res

    def build_matrix_of_k_pondered(self, matrix_ordered, R, C):
        # matriz con una fila menos
        res = [[0] * C for _ in range(R - 1)]
        c0 = 0
        c1 = 0
        c2 = 0
        for col in range(C):
            values = [r[col] for r in matrix_ordered]
            values.sort(key=lambda s: s[0], reverse=True)
            # print('VALUES ordenada en teoria para comparar los c0 y c1: ', values)
            # print('columna::::: ', col)
            # obtengo la clase dueña de la columna (sera 0 la distancia a si mismo)
            item_owner = values.pop()
            print('item Owner: ', item_owner)
            for i in range(1, R):
                # for i = 1 in range(R):
                # print('ITERATOR: ', i)
                # obtengo la clase
                item = values.pop()
                print('item..... ', item)
                # print('The Class in matrix ordered: ', item[1])
                # print('div: ', 1/neighbors[i][1])
                # print('el divisor: ', neighbors[i][1])
                # print('mult. por clase 0 ', self.validate_class(0, neighbors[i]))
                c0 += (1 / (item[0] ** 2)) * self.validate_class_of_ponderated(0, item[1])
                c1 += (1 / (item[0] ** 2)) * self.validate_class_of_ponderated(1, item[1])
                c2 += (1 / (item[0] ** 2)) * self.validate_class_of_ponderated(2, item[1])

                #if int(item[1]) == 0:
                #    c0 += 1
                #elif int(item[1]) == 1:
                #    c1 += 1
                #elif int(item[1]) == 2:
                #    c2 += 1
                #else:
                #    print('no deberia llegar aqui')
                # print('Hasta el momento: ')
                print('c0: ', c0)
                print('c1: ', c1)
                print('c2: ', c2)
                if c0 > c1 and c0 > c2:
                    if int(item_owner[1]) == 0:
                        print('Cargo 1 en la matrix, gano c0')
                        res[i - 1][col] = 1
                    else:
                        print('Cargo 0 en la matrix porque la clase 1 no gano y aca comparo por la clase 1.')
                        res[i - 1][col] = 0
                elif c0 < c1 and c2 < c1:
                    if int(item_owner[1]) == 1:
                        print('Cargo 1 en la matrix, gano c1')
                        res[i - 1][col] = 1
                    else:
                        print('Cargo 0 en la matrix porque la c0 o c1 gano y aca comparo por la clase 1.')
                        res[i - 1][col] = 0
                elif c2 > c1 and c2 > c0:
                    if int(item_owner[1]) == 2:
                        print('Cargo 1 en la matrix gano c2.')
                        res[i - 1][col] = 1
                    else:
                        print('Cargo 0 en la matrix porque la clase c2 no gano y aca comparo por la clase 2.')
                        res[i - 1][col] = 0
                else:
                    # Aca cuando no se puede decidir por ser iguales.
                    res[i - 1][col] = 0
            c0 = 0
            c1 = 0
            c2 = 0
        print('Final matrix:: ', np.array(res))
        return res


    def order_matrix_by_column(self, matrix, R, C):
        res = [[0] * C for _ in range(R)]
        for col in range(C):
            values = [r[col] for r in matrix]
            # print('VALUES FOR COLUMN ORDER: ', values)
            # values.sort(reverse=True) key=lambda tup: tup[1]
            values.sort(key=lambda s: s[0], reverse=True)
            # print('VALUES ordenada en teoria: ', values)
            for row in range(R):
                res[row][col] = values.pop()
        return res

    # deprecated pue
    def get_test_values(self, matrix):
        # for i in range(len(matrix)):
        #     for j in range(len(matrix[0])):
        #         matrix[i][j]
        array_test = []
        # c0
        for i in range(160, 200):
            array_test.append(matrix[i])
        for i in range(360, 400):
            array_test.append(matrix[i])
        for i in range(560, 600):
            array_test.append(matrix[i])

        print('array ::: ', np.array(array_test))
        print('lenght:: ', len(array_test))

        return np.array(array_test)

    def exec_data_knn(self, data_test, matrix, k):
        matrix_result = []
        for i in range(len(data_test)):
            neighbors = self.get_neighbors(data_test[i], matrix)
            print('neighbors quantity: ', len(neighbors))
            class_result = self.get_class(neighbors, k)
            print('Clasifica como clase: ', class_result)
            print('Sin embargo era de clase:: ', matrix[i][2])
            if int(class_result) != matrix[i][2]:
                point_failed = copy.deepcopy(matrix[i])
                if class_result == 0:
                    point_failed[2] = -100
                else:
                    point_failed[2] = point_failed[2] * -1
                print('point failed: ', point_failed)
                matrix_result.append(point_failed)
            else:
                matrix_result.append(matrix[i])
            neighbors.clear()
        return matrix_result

    def exec_data_knn_ponderated(self, data_test, matrix, k):
        errors = 0
        matrix_result = []
        #for i in range(len(data_test)):
        # aca el range seria el tamaño de la matriz (Todos contra todos!)
        for i in range(len(data_test)):
            neighbors = self.get_neighbors(data_test[i], matrix)
            print('neighbors quantity: ', np.array(neighbors))
            class_result = self.get_class_ponderated(neighbors, k)
            print('punto a clasificar:: ', matrix[i])
            print('Clasifica como clase: ', class_result)
            print('Sin embargo era de clase:: ', matrix[i][2])

            # aca appendear el array nuevo con sus colores si hay errores.
            # ...
            if int(class_result) != matrix[i][2]:
                point_failed = copy.deepcopy(matrix[i])
                if class_result == 0:
                    point_failed[2] = -100
                else:
                    point_failed[2] = point_failed[2] * -1
                print('point failed: ', point_failed)
                matrix_result.append(point_failed)
            else:
                matrix_result.append(matrix[i])

            if int(class_result) != int(matrix[i][2]):
                # contar los errores
                errors += 1
            neighbors.clear()
        print('Errors quantity: ', errors)
        #return matrix_result
        return errors

    def run_algorith(self, path_dataset, k):
        data = self.open_file_data(path_dataset)
        #data = self.open_file_data('dataset1.csv')
        self.points_csv = data
        # print('Data 1: ', data[0])
        # [-5. -2.  0.]

        #############################################################
        # Funca: 1- K optimo entre 1 y 15
        ############################################################

        self.k_optimo = self.get_k_optim(data)
        # point_unknowkn = [2, 1]

        # neighbors = self.get_neighbors(point_unknowkn, self.dataset)
        # print('neighbors quantity: ', len(neighbors))
        # class_result = self.get_class(neighbors, 3)
        # print('Clasifica como clase: ', class_result)

        # test_data = self.get_test_values(data)

        #############################################################
        # Funca: 2- Evaluar la clasificacion utilizando el k optimo obtenido
        #############################################################
        # dataset, dataset, k
        if k == 0:
            result_points_plot = self.exec_data_knn(data, data, self.k_optimo)
            print("escribio")
            self.point_to_plot = np.array(result_points_plot)
            return np.array(result_points_plot)
        else:
            result_points_plot = self.exec_data_knn(data, data, k)
            print("escribio")
            self.point_to_plot = np.array(result_points_plot)
            return np.array(result_points_plot)

        #############################################################
        # Process: 3- Obtener la mejor clasificacion utilizando knn ponderado para un rango de [1-15]
        #############################################################
        # dataset, dataset, k
        # para cada k hasta 15 (Pasar k al range) la vista necesita la clasificacion entera de cada k
        # pasar k
        #self.get_errors_in_k_ponderated(data, k)
        #data_a_plotear = self.exec_data_knn_ponderated(data, data, k)
        #print('data a plotear: ', data_a_plotear)
        #return np.array(data_a_plotear)
        # print('lista de vecinos: ', neighbors)
        # classif = self.get_class_ponderated(neighbors)
        # print('THE CLASS CLASSIFIED TO UNKNOWN POINT IS: ', classif)
        return np.array(data)

    ########
    # Usar esto para obtener el k optimo ponderado
    ########
    def run_algorithm_of_k_optim_ponderated(self, path, k):
        data = self.open_file_data(path)
        k_optim = self.get_k_optim_ponderated(data)
        print('K Optimo poderated: ', k_optim)
        #self  .get_errors_in_k_ponderated(data, k)

    def run_algorithm_aug(self, path, k):
        pass

    def get_errors_in_k_ponderated(self, data, k):
        errors_array_in_k_ponderated = []
        for i in range(0,k):
            quantity_errors_ponderated = self.exec_data_knn_ponderated(data, data, i)
            errors_array_in_k_ponderated.append(quantity_errors_ponderated)
            quantity_errors_ponderated = 0
        print('Errors Array in k ponderated: ', np.array(errors_array_in_k_ponderated))


    def open_file_data(self, filename):
        #file = open('../datasets/' + filename)
        file = open(filename)
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

    def get_point_to_plot(self):
        return self.point_to_plot
    def get_point(self):
        return self.points_csv
    def get_k_optim_value_from_controller(self):
        return self.k_optimo