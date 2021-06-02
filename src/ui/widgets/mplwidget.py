# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvas

# from matplotlib.figure import Figure

import scipy.signal as ss
import matplotlib.pyplot as plt
import numpy as np

    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.figure = plt.figure()
        # self.figure = plt.figure(figsize = (13, 2))
        self.canvas = FigureCanvas(self.figure)


        # A partir de aca es lo mismo que con pyplot, solo que el manejo no es automatico, sino
        # que lo hace uno con criterio, entonces creamos un par de ejes
        
        self.axes = self.figure.add_subplot()
        self.axes.set_position([0.125, 0.15, 0.775, 0.77])

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        
    def _maxZP(self, H):
        zeroes, poles, gain=ss.tf2zpk(H.num, H.den)
        zMax=abs(max(zeroes, default=0))
        pMax=abs(min(poles, default=0))
        
        if zMax > pMax:
            if zMax==0:
                return 3
            return np.ceil(np.log10(zMax))+2
            
        else:
            if pMax==0:
                return 3
            return np.ceil(np.log10(pMax))+2

    def plotBodeModule(self, H):

        self.axes.clear()

        xlim = self._maxZP(H)   # Cálculo de la máxima frec representativa

        w = np.logspace(-4, xlim, 10000)       # Revisar para graficar facha
        eje, modulo, fase= ss.bode(H, w=w)            # Calculo del Bode


        # Creamos las figuras
        ejeX = eje / (2*np.pi)
        self.axes.plot(ejeX, modulo)

        # Ponemos comentarios
        # self.axes.set_title('Magnitud')
        self.axes.set_xlabel(r'f [$Hz$] | log')
        self.axes.set_ylabel(r'|H(j$\omega$)| [dB]')

        # Pasamos a escala logaritmica 
        self.axes.set_xscale('log') 
        
        # Graficamos
        self.axes.grid(True)
        self.canvas.draw()

    
    def plotBodePhase(self, H):

        self.axes.clear()

        xlim = self._maxZP(H)   # Cálculo de la máxima frec representativa

        w = np.logspace(-4, xlim, 10000)       # Revisar para graficar facha
        eje, modulo, fase = ss.bode(H, w=w)            # Calculo del Bode

        # Creamos las figuras
        ejef = eje / (2*np.pi)
        self.axes.plot(ejef, fase)

        # Ponemos comentarios
        # self.axes.set_title('Fase')
        self.axes.set_xlabel(r'f [$Hz$] | log')
        self.axes.set_ylabel(r'Fase [deg]')

        # Pasamos a escala logaritmica 
        self.axes.set_xscale('log') 
        
        # Graficamos
        self.axes.grid(True)
        self.canvas.draw()

    def plotZerosPoles(self, H):

        self.axes.clear()

        zeros, poles = H.zeros, H.poles

        self.axes.scatter(np.real(zeros), np.imag(zeros), c="g", marker="o")
        self.axes.scatter(np.real(poles), np.imag(poles), c="r", marker="x")

        self.axes.set_xlabel(r'$\sigma$', fontsize=15)
        self.axes.set_ylabel(r'$jw$', fontsize=15)
        self.axes.set_title('Gráfico Polos y Ceros')

        self.axes.grid(True)
        self.canvas.draw()

    def filterImpulse(self, H, u=0, w=1, A=1):
        self.axes.clear()

        if u == "escalon":
            t = np.linspace(0, 5, 10000, endpoint=False)
            u = A*np.ones(10000)
        elif u == "seno":  
            xMax= 1/w
            t = np.linspace(0, xMax, 10000, endpoint=False)
            u = A*(np.sin(w*t))
        else:
            u = np.ones(10000)

        tout, yout, xout = ss.lsim((H.num, H.den), U=u, T=t)
        self.axes.plot(tout, yout)
        self.axes.set_ylabel("Salida")
        self.axes.set_xlabel('Tiempo[sec]')
        self.axes.grid(True)
        self.canvas.draw()
        
    def _sumTransfer(self, a, b):
        return  [ np.polyadd( np.polymul( a[0], b[1] ), np.polymul( b[0], a[1] ) ), np.polymul(a[1], b[1]) ]

    def RLCSim(self, punta1=1 , punta2=2, R=0, L=0, C=0):    

        H_base = [ [ C, 0 ],[ L*C, R*C, 1 ] ]
        
        H_R = [ [ R ]   ,    [ 1 ] ]
        H_L = [ [ L, 0 ],    [ 1 ] ]
        H_C = [ [ 1 ]   , [ C, 0 ] ]
        
        # Setear H_2 en base a las puntas
        H_2 = [ [ 0 ], [ 1 ] ]

        puntaMin = min(punta1, punta2)
        puntaMax = max(punta1, punta2)

        tipRange = range(puntaMin, puntaMax+1)

        # print('punta1:', punta1, 'punta2:', punta2, 'tipRange:', tipRange)

        if (all(node in tipRange for node in [1,2])):           # Resistencia
            H_2 = self._sumTransfer(H_2, H_R)

        if (all(node in tipRange for node in [2,3])):           # Inductor
            H_2 = self._sumTransfer(H_2, H_L)

        if (all(node in tipRange for node in [3,4])):           # Capacitor
            H_2 = self._sumTransfer(H_2, H_C)


        if (puntaMin != punta1):                                # Las pinzas estan invertidas?
            H_2[0] = np.polymul(H_2[0],-1)


        H = ss.TransferFunction(np.polymul(H_base[0], H_2[0]), np.polymul(H_base[1], H_2[1]))
        self.figure.clear()

    
        if (np.array_equal(H.num, H.den)):  # Se rompe si H=+-1
            H = ss.TransferFunction([1], [1])
        elif np.array_equal(np.polymul(H.num, -1), H.den):
            H = ss.TransferFunction([-1], [1])

        num_str, den_str = tfToString(H)

        self.figure.suptitle('$H(s) = \\frac{'+ num_str +'}{'+ den_str+'}$')
        # self.figure.suptitle('Diagrama de Bode\n$H(s) = \\frac{'+ num_str +'}{'+ den_str+'}$')
        mag, phase = self.figure.add_subplot(1,2,1), self.figure.add_subplot(1, 2, 2)
        self.figure.subplots_adjust(wspace = .4)
        self._plotBode(H=H, mag=mag, phase=phase)
        self.canvas.draw()

    def _plotBode(self, H, mag, phase):
        
        xlim = self._maxZP(H)   # Cálculo de la máxima frec representativa

        w = np.logspace(-4, xlim, 10000)       # Revisar para graficar facha
        bode = ss.bode(H, w=w)            # Calculo del Bode

        # Creamos las figuras
        ejeX = bode[0] / (2*np.pi)
        mag.plot(ejeX, bode[1])
        phase.plot(ejeX, bode[2])

        # Ponemos comentarios
        mag.set_title('Modulo')
        phase.set_title('Fase')
        mag.set_xlabel(r'f [$Hz$] | log')
        phase.set_xlabel(r'f [$Hz$] | log')
        mag.set_ylabel(r'|H(j$\omega$)| [dB]')
        phase.set_ylabel(r'Phase [deg]')

        # Pasamos a escala logaritmica 
        mag.set_xscale('log') 
        phase.set_xscale('log')
        
        # Graficamos
        mag.grid(); phase.grid()

    def clearAxis(self):
        self.axes.clear()
        self.canvas.draw()

    def clearFigure(self):
        self.figure.clear()
        self.canvas.draw()

def tfToString(H):
    num_str = ""
    den_str = ""

    for i in range(len(H.num)):
        q = len(H.num)-i-1
        if H.num[i] != 0:

            if i>0 and H.num[i-1] !=0:
                num_str += ' + '

            num_str += str(H.num[i])
            if  q > 1:
                num_str += 's^' + str(q)
            elif q==1:
                num_str += 's'

    for index in range(len(H.den)):
        exponente = len(H.den)-index-1
        if H.den[index] != 0:
            if index>0 and H.den[index-1] !=0:
                den_str += ' + '
            den_str += str(H.den[index])
            if  exponente > 1:
                den_str += 's^' + str(exponente)
            elif exponente==1:
                den_str += 's'

    return num_str, den_str