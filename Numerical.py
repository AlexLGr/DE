import numpy as np
import matplotlib.pyplot as plt
import math


class ODE:
    def __init__(self, x0, y0, X, N):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        self.eulerRes = []
        self.improvedEulerRes = []
        self.rungeRes = []
        self.exactRes = []
        self.eulerErr = []
        self.eulerIErr = []
        self.rungeErr = []

    def euler(self):
        x = []
        y = []
        x0 = self.x0
        y0 = self.y0
        h = (self.X - x0)/self.N
        for j in range(self.N):
            m = (2*x0)*(pow(x0, 2)+y0)
            y1 = y0 + h*m
            x1 = x0 + h
            x.append(x1)
            y.append(y1)
            x0 = x1
            y0 = y1
        grid = [x, y]
        self.eulerRes = grid.copy()
        return grid

    def improved_euler(self):
        x = []
        y = []
        x0 = self.x0
        y0 = self.y0
        h = (self.X - x0) / self.N
        for j in range(self.N):
            k1 = (2 * x0) * (pow(x0, 2) + y0)
            k2 = (2 * (x0+h)) * (pow((x0+h), 2) + (y0+h*k1))
            x1 = x0 + h
            y1 = y0 + h*((k1+k2)/2)
            x.append(x1)
            y.append(y1)
            x0 = x1
            y0 = y1
        grid = [x, y]
        self.improvedEulerRes = grid.copy()
        return grid

    def runge_kutta(self):
        x = []
        y = []
        x0 = self.x0
        y0 = self.y0
        h = (self.X - x0) / self.N
        for j in range(self.N):
            k1 = h * (2*x0)*(pow(x0, 2)+y0)
            k2 = h * (2*(x0+(h/2)))*(pow((x0+(h/2)), 2) + (y0+(k1/2)))
            k3 = h * (2*(x0+(h/2)))*(pow((x0+(h/2)), 2) + (y0+(k2/2)))
            k4 = h * (2*(x0+h))*(pow((x0+h), 2) + (y0+k3))
            y1 = y0 + (k1+2*k2+2*k3+k4)/6
            x1 = x0 + h
            x.append(x1)
            y.append(y1)
            x0 = x1
            y0 = y1
        grid = [x, y]
        self.rungeRes = grid.copy()
        return grid

    def exact(self):
        x = []
        y = []
        x0 = self.x0
        y0 = self.y0
        x1 = x0
        C = (y0 + pow(x0, 2)+1) * math.exp(-pow(x0, 2))
        h = (self.X - x0) / (self.N)
        for j in range(self.N):
            x1 += h
            y1 = math.exp(pow(x1, 2)) * (-math.exp(-pow(x1, 2)) * pow(x1, 2) - -math.exp(-pow(x1, 2)) + C)
            x.append(x1)
            y.append(y1)
        grid = [x, y]
        self.exactRes = grid.copy()
        return grid
    def solve(self):
        self.exact()
        self.runge_kutta()
        self.improved_euler()
        self.euler()
    def errors(self):
        for i in range(len(self.eulerRes[0])):
            if(i!=0):
                self.eulerErr.append(math.fabs(self.exactRes[1][i] - self.eulerRes[1][i]))
                self.eulerIErr.append(math.fabs(self.exactRes[1][i] - self.improvedEulerRes[1][i]))
                self.rungeErr.append(math.fabs(self.exactRes[1][i] - self.rungeRes[1][i]))
            else:
                self.eulerErr.append(math.fabs(self.exactRes[1][i] - self.eulerRes[1][i]))
                self.eulerIErr.append(math.fabs(self.exactRes[1][i] - self.improvedEulerRes[1][i]))
                self.rungeErr.append(math.fabs(self.exactRes[1][i] - self.rungeRes[1][i]))

class Global:
    def __init__(self, x0, y0, X, N, N0):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        self.N0 = N0
        self.n = []
        self.errorEuler = []
        self.errorIE = []
        self.errorRunge = []
    def solve(self):
        n = self.N0
        while(n<=self.N):
            new_eq = ODE(self.x0, self.y0, self.X, n)
            new_eq.solve()
            new_eq.errors()
            self.n.append(n)
            self.errorEuler.append(new_eq.eulerErr[-1])
            self.errorIE.append(new_eq.eulerIErr[-1])
            self.errorRunge.append(new_eq.rungeErr[-1])
            n = n + 5
