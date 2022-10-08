from math import sqrt


class KnnController:

    def __init__(self):
        self.distances = []
        self.dataset = [[2.7810836, 2.550537003, 0],
                   [1.465489372, 2.362125076, 0],
                   [3.396561688, 4.400293529, 0],
                   [1.38807019, 1.850220317, 0],
                   [3.06407232, 3.005305973, 0],
                   [7.627531214, 2.759262235, 1],
                   [5.332441248, 2.088626775, 1],
                   [6.922596716, 1.77106367, 1],
                   [8.675418651, -0.242068655, 1],
                   [7.673756466, 3.508563011, 1]]
        self.k = 7

        # Struct vector point
        # [x,y,class,distance]

    def __repr__(self):
        return str(self.__dict__)




    # distancia entre pares de valores (x,y)
    def euclidean_distance(self, vector1, vector2):
        return sqrt((vector1[0] - vector2[0])**2 + (vector1[1] - vector2[1])**2)


    def get_neighbors(self, point, dataset, k):
        distances = list()
        for pair_dataset in dataset:
            distance = self.euclidean_distance(point, pair_dataset)
            self.distances.append((pair_dataset, distance))
        self.distances.sort(key=lambda tup: tup[1])
        print('Vector with distances ::: ', self.distances)
        neighbors = list()
        for i in range(k):
            #print(self.distances[i][0])
            # append distance from point
            # [x,y,class,"distance"]
            #self.distances[i][0].append(distance)
            neighbors.append(self.distances[i])
        return neighbors

    def get_class(self, neighbors: list):
        freq1 = 0
        freq2 = 0
        for i in range(len(neighbors)):
            print('value in matrix: ', neighbors[i][0][2])
            if neighbors[i][0][2] == 1:
                freq1 += 1
            else:
                freq2 += 1
        if freq1 > freq2:
            return 1
        else:
            return 0

    def get_class_ponderated(self, neighbors: list):
        freq1 = 0
        freq2 = 0
        for i in range(len(neighbors)):
            if neighbors[i][0][2] == 1:
                print('La distancia: ', neighbors[i][1])
                if neighbors[i][1] != 0: # not division by zero
                    freq1 += 1/neighbors[i][1]
            else:
                freq2 += 1
        if freq1 > freq2:
            return 1
        else:
            return 0


    def run_algorith(self):
        point_unknowkn = [7.673756466, 3.508563011]
        neighbors = self.get_neighbors(point_unknowkn, self.dataset, self.k)
        classif = self.get_class_ponderated(neighbors)
        print('THE CLASS CLASSIFIED TO UNKNOWN POINT IS: ', classif)
        for neighbor in neighbors:
            print(neighbor)

