'''
Clase para crear graficos
'''
import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import matplotlib.dates as mdates

class graph:

    def graficar(x,y1,y2):
        
        # split the data into two parts
        xdata1 = x
        ydata1 = y1
        ydata2 = y2

        plt.plot(xdata1,ydata1)
        plt.title('Rendimiento FCIs Billeteras')
        plt.xlabel('Rendimiento')
        plt.ylabel('Fecha')


        # display the plot
        plt.show()
