import sys
from Numerical import ODE
from Numerical import Global

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.solutions = PlotCanvas(self, width=7, height=2.3)
        self.solutions.move(0, 0)

        self.local = PlotCanvas(self, width=7, height=2.3, mode=1)
        self.local.move(0, 220)

        self.glob = PlotCanvas(self, width=7, height=2.3, mode=2)
        self.glob.move(0, 440)


        label = QtWidgets.QLabel(self)
        label.move(770, 0)
        label.setText('Enter x0')
        self.x0 = QtWidgets.QLineEdit(self)
        self.x0.move(750, 30)
        self.x0.setText('0')

        label1 = QtWidgets.QLabel(self)
        label1.move(770, 60)
        label1.setText('Enter y0')
        self.y0 = QtWidgets.QLineEdit(self)
        self.y0.move(750, 90)
        self.y0.setText('0')

        label2 = QtWidgets.QLabel(self)
        label2.move(770, 120)
        label2.setText('Enter X')
        self.X = QtWidgets.QLineEdit(self)
        self.X.move(750, 150)
        self.X.setText('2')

        label3 = QtWidgets.QLabel(self)
        label3.move(770, 180)
        label3.setText('Enter N')
        self.N = QtWidgets.QLineEdit(self)
        self.N.move(750, 210)
        self.N.setText('100')

        label4 = QtWidgets.QLabel(self)
        label4.move(770, 240)
        label4.setText('Enter N0')
        self.N0 = QtWidgets.QLineEdit(self)
        self.N0.move(750, 270)
        self.N0.setText('5')

        button = QPushButton('Solve', self)
        button.move(750, 310)
        button.clicked.connect(self.compute)

        self.show()
    def compute(self):
        self.solutions.clear()
        self.local.clear()
        self.glob.clear()
        x0 = float(self.x0.text())
        y0 = float(self.y0.text())
        X = float(self.X.text())
        N = int(self.N.text())
        N0 = int(self.N0.text())
        self.solutions.plot_solution(x0, y0, X, N)
        self.local.plot_errors(x0, y0, X, N)
        self.glob.plot_global(x0, y0, X, N, N0)



class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, mode=0, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(1, 1, 1)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        if (mode == 0):
            self.plot_solution()
        else:
            if(mode==1):
                self.plot_errors()
            else:
                self.plot_global()


    def plot_solution(self, x0=0, y0=0, X=2, N=50):
        new_eq = ODE(x0, y0, X, N)
        new_eq.solve()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_ylabel('f(x) values')
        ax.set_xlabel('x values')
        ax.plot(new_eq.eulerRes[0], new_eq.eulerRes[1], color='tab:red', label='Euler')
        ax.plot(new_eq.rungeRes[0], new_eq.rungeRes[1], color='tab:blue', label='Runge-Kutta')
        ax.plot(new_eq.improvedEulerRes[0], new_eq.improvedEulerRes[1], color='tab:green', label='Improved Euler')
        ax.plot(new_eq.exactRes[0], new_eq.exactRes[1], color='tab:orange', label='Exact')
        ax.set_title('Solutions')
        ax.legend(loc='upper left')
        self.draw()

    def plot_errors(self, x0=0, y0=0, X=2, N=50):
        new_eq = ODE(x0, y0, X, N)
        new_eq.solve()
        new_eq.errors()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_ylabel('local errors values')
        ax.set_xlabel('x values')
        ax.plot(new_eq.exactRes[0], new_eq.eulerErr, color='tab:red', label='Euler')
        ax.plot(new_eq.rungeRes[0], new_eq.rungeErr, color='tab:blue', label='Runge-Kutta')
        ax.plot(new_eq.improvedEulerRes[0], new_eq.eulerIErr, color='tab:green', label='Improved Euler')
        ax.set_title('Local Errors')
        ax.legend(loc='upper left')
        self.draw()

    def plot_global(self, x0=0, y0=0, X=2, N=100, N0 = 5):
        new_global = Global(x0, y0, X, N, N0)
        new_global.solve()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_ylabel('global error values')
        ax.set_xlabel('number of steps N')
        ax.plot(new_global.n, new_global.errorEuler, color='tab:red', label='Euler')
        ax.plot(new_global.n, new_global.errorRunge, color='tab:blue', label='Runge-Kutta')
        ax.plot(new_global.n, new_global.errorIE, color='tab:green', label='Improved Euler')
        ax.set_title('Global Errors')
        ax.legend(loc='upper right')
        self.draw()

    def clear(self):
        ax = self.figure.add_subplot(1, 1, 1)
        ax.clear()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())