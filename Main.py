import sympy as sym
import scipy.signal as ss
import matplotlib.pyplot as plt
import numpy as np

def maxZP(H):
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

def plotbode(H, mag, phase, ylim = None):
    
    xlim = maxZP(H)   # Cálculo de la máxima frec representativa

    w = np.logspace(-4, xlim, 10000)       # Revisar para graficar facha
    bode = ss.bode(H, w=w)            # Calculo del Bode

    # Creamos las figuras
    ejeX = bode[0] / (2*np.pi)
    mag.plot(ejeX, bode[1])
    phase.plot(ejeX, bode[2])

    # Ponemos comentarios
    fig.suptitle('Diagrama de Bode')
    mag.set_title('Magnitud')
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
    mag.set_ylim(None if not ylim else [-125, 5])
    fig.subplots_adjust(wspace = .4)

def filterImpulse(H, u, axis, w=1, A=1):
  
  t = np.linspace(0, 1/w, 500, endpoint=False)
  
  if u == "escalon":
    u = A*t
  elif u == "seno":  
    u = A*(np.sin(w*t))
  else:
    u = np.ones(500)

  tout, yout, xout = ss.lsim((H.num, H.den), U=u, T=t)
  axis.plot(tout, yout)
  axis.set_ylabel("out")
  axis.set_xlabel('time[sec]')
  axis.grid(True)

def plotZerosPoles(H, figure, ax):
  zeros, poles = H.zeros, H.poles

  ax.scatter(np.real(zeros), np.imag(zeros), c="g", marker="o")
  ax.scatter(np.real(poles), np.imag(poles), c="r", marker="x")

  ax.set_xlabel(r'$\sigma$', fontsize=15)
  ax.set_ylabel(r'$jw$', fontsize=15)
  ax.set_title('Gráfico Polos y Ceros')

  ax.grid(True)

########################################################################################
#                                       Primer parte
########################################################################################

#generamos la Ganancia
H_num=[1]
H_den=[1,0,1]
H=ss.TransferFunction(H_num,H_den)

#Graficamos polos y ceros
figure_scatter, ax_scatter= plt.subplots()
plotZerosPoles(H, figure_scatter, ax_scatter)
#figure_scatter.show()

#Graficamos Bode
fig = plt.figure(figsize = (13, 4))
mag, phase = fig.add_subplot(1,2,1), fig.add_subplot(1, 2, 2)
plotbode(H=H, mag=mag, phase=phase)
#fig.show()

#Graficamos impulso
A=1
w=1
u = 'escalon'
figure_impulse, ax_impulse = plt.subplots()
filterImpulse(H, u, ax_impulse, w, A)
#figure_impulse.show()

########################################################################################
#                                       Segunda parte
########################################################################################
def sumTransfer(a, b):
    return  [ np.polyadd( np.polymul( a[0], b[1] ), np.polymul( b[0], a[1] ) ), np.polymul(a[1], b[1]) ]

def RLCSim(fig, punta1=1 , punta2=2, R=0, L=0, C=0):
    
    # H_base = s*C/(s^2LC+sCR+1)
    # Z = s^2*L + s*R + 1/C

    H_base = [ [ C, 0 ],[ L*C, R*C, 1 ] ]
    
    H_R = [ [ R ]   ,    [ 1 ] ]
    H_L = [ [ L, 0 ],    [ 1 ] ]
    H_C = [ [ 1 ]   , [ C, 0 ] ]
    
    # Setear H_2 en base a las puntas
    H_2 = [ [ 0 ], [ 1 ] ]

    puntaMin = min(punta1, punta2)
    puntaMax = max(punta1, punta2)

    tipRange = range(puntaMin, puntaMax+1)

    if (all(node in tipRange for node in [1,2])):           # Resistencia
        H_2 = sumTransfer(H_2, H_R)

    if (all(node in tipRange for node in [2,3])):           # Inductor
        H_2 = sumTransfer(H_2, H_L)

    if (all(node in tipRange for node in [3,4])):           # Capacitor
        H_2 = sumTransfer(H_2, H_C)

    if (puntaMin != punta1):                                # Las pinzas estan invertidas?
        H_2[0] = np.polymul(H_2[0],-1)

    H = ss.TransferFunction(np.polymul(H_base[0], H_2[0]), np.polymul(H_base[1], H_2[1]))
    
    if (np.array_equal(H.num, H.den)):  # Se rompe si H=1
      H = ss.TransferFunction([1], [1])

    fig = plt.figure(figsize = (13, 4))
    mag, phase = fig.add_subplot(1,2,1), fig.add_subplot(1, 2, 2) 
    plotbode(H=H, mag=mag, phase=phase)


#Main
fig = plt.figure(figsize = (13, 4))
RLCSim(fig, 2, 4, 10, 10E-3, 10E-6)