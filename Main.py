#%run plotters

import sympy as sym
import scipy.signal as ss
import matplotlib as plt
import numpy as np


# Segunda Parte
def RLCSim(punta1=1 , punta2=4, R=0, L=0, C=0):
    
    if punta1==1 and punta2==2:
        print("pepito")
    
    num = [1]
    denom = [L * C2, R * C2, C2/C1 + 1]
    H = ss.TransferFunction(num, denom)
    
def drawBode(H):
    plotbode(H, 1)

def plotbode(H, ylim = None):
    w = np.logspace(-4, 3, 10000)       #Preguntar
    bode = ss.bode(H, w = w)
    
    fig = plt.figure(figsize = (13, 4))
    mag, phase = fig.add_subplot(1,2,1), fig.add_subplot(1, 2, 2)
    mag.plot(bode[0], bode[1])
    phase.plot(bode[0], bode[2])
    fig.suptitle('Diagrama de Bode')
    mag.set_title('Magnitud')
    phase.set_title('Fase')
    mag.set_xlabel(r'$\omega$ [$\frac{rad}{seg}$] | log')
    phase.set_xlabel(r'$\omega$ [$\frac{rad}{seg}$] | log')
    mag.set_ylabel(r'|H(j$\omega$)| [dB]')
    phase.set_ylabel(r'Phase [deg]')
    mag.set_xscale('log') 
    phase.set_xscale('log')
    mag.grid(); phase.grid(); mag.set_ylim(None if not ylim else [-125, 5])
    fig.subplots_adjust(wspace = .4)