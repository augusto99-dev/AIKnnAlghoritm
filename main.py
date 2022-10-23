# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from math import sqrt

from controller.Controller import KnnController
#from view.Graphics2DTest import Graphics
#from view.main_view_cont import MainWindow
from view.Graphics2DTest import Graphics


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #pass
    controller = KnnController()
    graphics = Graphics()
    array_data = controller.run_algorithm_aug('./datasets/dataset3.csv', 4)
    #print('resulttttt. ', array_data)

    #graphics.plot_dataset(array_data)




