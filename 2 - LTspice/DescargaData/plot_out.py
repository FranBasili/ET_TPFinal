import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sympy as sp

#################################################################################
# Lectura de datos y plot del txt!
#################################################################################
FILE_NAME = sys.argv[1]

with open(FILE_NAME, "r") as f:
	first_row = f.readline()

my_data = np.genfromtxt(FILE_NAME, delimiter='\t')

x = []
y = []
for i in range(len(my_data)):
	# check if number
	x1 = float(my_data[i][0])
	y1 = float(my_data[i][1])	
	if not (math.isnan(x1) or math.isnan(y1)):
		x.append(x1)
		y.append(y1)

# Plotting .txt
#my = [element * 1000 for element in y] # Multiplied to see in mA
plt.plot(x,y, 'blue', linewidth=4)
if math.isnan(my_data[0][0]) and math.isnan(my_data[0][1]):
	plt.xlabel("$"+first_row.split('\t')[0] + "\ [s]$")
	plt.ylabel("$"+first_row.split('\t')[1][:-1] + "\ [A]$")
plt.grid(True)

#################################################################################
# Data
#################################################################################
V0 = 5
Il0 = 0.8333
R = 13
L = 0.45
C = 300e-6

w0 = 1/(np.sqrt(L*C))
alpha = R/(2*L)

#Condiciones Iniciales
I0 = 0.8333333333333
VL0 = 0

t_s = sp.symbols('t', real = True)
I_s = sp.symbols('I', cls = sp.Function)
#################################################################################
# Calculo diferencial
#################################################################################
# Ecuación diferencial
eq = I_s(t_s).diff(t_s,2) + 2 * alpha * I_s(t_s).diff(t_s,1) + w0**2 * I_s(t_s)

# Igualo a las condiciones iniciales
init_values = {I_s(0) : I0, I_s(t_s).diff(t_s,1).subs(t_s,0) : VL0 / L}

#Resolvemos la ecuación diferencial
res = sp.dsolve(eq, I_s(t_s), ics = init_values).args
print("Solución a la ecuación diferencial")
print(res)
I_symbol = res[1]

I_lambda = sp.lambdify(t_s, I_symbol, modules = 'numpy')

t = np.linspace(0, .395, 100000)
IL = I_lambda(t)
plt.plot(t+0.004, IL, 'orange')
#################################################################################
# EXTRA
#################################################################################
# agregamos patches
patches = [
    mpatches.Patch(color="blue", label="Curva de simulacion"),
    mpatches.Patch(color="orange" , label="Curva teorica")
]
plt.legend(handles=patches)
plt.minorticks_on()
plt.grid(which = 'major', linestyle = '--', color = 'black', linewidth = 0.8)
plt.grid(which = 'minor', linestyle = ':', color = 'black', linewidth = 0.4)

plt.suptitle('Descarga del RLC')

#Mostramos todo
plt.show()