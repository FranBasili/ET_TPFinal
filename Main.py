import sympy as sym
import scipy.signal as ss
import matplotlib.pyplot as plt
import numpy as np

def plotbode(H, ylim = None):
    
    w = np.logspace(-4, 3, 10000)       # Preguntar
    bode = ss.bode(H, w = w)            # Calculo del Bode
    
    # Creamos las figuras
    fig = plt.figure(figsize = (13, 4))
    mag, phase = fig.add_subplot(1,2,1), fig.add_subplot(1, 2, 2)
    mag.plot(bode[0], bode[1])
    phase.plot(bode[0], bode[2])

    # Ponemos comentarios
    fig.suptitle('Diagrama de Bode')
    mag.set_title('Magnitud')
    phase.set_title('Fase')
    mag.set_xlabel(r'$\omega$ [$\frac{rad}{seg}$] | log')
    phase.set_xlabel(r'$\omega$ [$\frac{rad}{seg}$] | log')
    mag.set_ylabel(r'|H(j$\omega$)| [dB]')
    phase.set_ylabel(r'Phase [deg]')

    # Pasamos a escala logaritmica 
    mag.set_xscale('log') 
    phase.set_xscale('log')
    
    # Graficamos
    mag.grid(); phase.grid(); mag.set_ylim(None if not ylim else [-125, 5])
    fig.subplots_adjust(wspace = .4)







# Segunda Parte
def sumTransfer(a, b):
    return  [ np.polyadd( np.polymul( a[0], b[1] ), np.polymul( b[0], a[1] ) ), np.polymul(a[1], b[1]) ]

def RLCSim(punta1=1 , punta2=2, R=0, L=0, C=0):
    
    # H_base = s*C/(s^2LC+sCR+1)
    # Z = s^2*L + s*R + 1/C

    # H_base = ss.TransferFunction([ C, 0 ],[ L*C, R*C, 1 ])
    H_base = [ [ C, 0 ],[ L*C, R*C, 1 ] ]
    
    H_R = [ [ R ]   ,    [ 1 ] ]
    H_L = [ [ L, 0 ],    [ 1 ] ]
    H_C = [ [ 1 ]   , [ C, 0 ] ]
    
    # Setear H_2 en base a las puntas
    # H_2 = ss.TransferFunction([1], [1])

    H_2 = [ [ 0 ], [ 1 ] ]

    puntaMin = min(punta1, punta2)
    puntaMax = max(punta1, punta2)

    tipRange = range(punta1, punta2+1)

    if (all(node in tipRange for node in [1,2])):           # Resistencia
        H_2 = sumTransfer(H_2, H_R)

    if (all(node in tipRange for node in [2,3])):           # Inductor
        H_2 = sumTransfer(H_2, H_L)

    if (all(node in tipRange for node in [3,4])):           # Capacitor
        H_2 = sumTransfer(H_2, H_C)

    if (puntaMin != punta1):
        H_2[0] = np.polymul(H_2[0],-1)

    H = ss.TransferFunction(np.polymul(H_base[0], H_2[0]), np.polymul(H_base[1], H_2[1]))
    
    plotbode(H, 1)





RLCSim(1, 2, 1000, 10E-3, 10E-6)
