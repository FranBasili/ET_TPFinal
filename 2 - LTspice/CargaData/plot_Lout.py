import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sympy as sp

fig, ax_f = plt.subplots()
ax_c = ax_f.twinx()

#################################################################################
# Lectura de datos y plot del txt!
#################################################################################
FILE_NAME = sys.argv[1]
FILE_NAME2 = sys.argv[2]

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
my = [element * 1 for element in y] # Multiplied to see in mA
ax_c.plot(x,my, 'blue', linewidth=6)

with open(FILE_NAME2, "r") as f:
	first_row2 = f.readline()

my_data2 = np.genfromtxt(FILE_NAME2, delimiter='\t')
x2 = []
y2 = []
for i in range(len(my_data2)):
	# check if number
	x1 = float(my_data2[i][0])
	y1 = float(my_data2[i][1])	
	if not (math.isnan(x1) or math.isnan(y1)):
		x2.append(x1)
		y2.append(y1)
my2 = [element * 1 for element in y2] # Multiplied to see in mA
ax_f.plot(x2,my2, 'red', linewidth=6)

if math.isnan(my_data2[0][1]):
	ax_f.set_ylabel("$"+first_row2.split('\t')[1][:-1] + "\ [V]$")
	ax_f.set_xlabel("$"+first_row.split('\t')[0] + "\ [s]$")

if math.isnan(my_data[0][0]) and math.isnan(my_data[0][1]):
	ax_c.set_ylabel("$"+first_row.split('\t')[1][:-1] + "\ [A]$")

#################################################################################
# Data
#################################################################################
V0 = 5
Il0 = 0.8333
R1 = 7
R2 = 6
L = 0.45
C = 300e-6

#Condiciones Iniciales
IL0 = 0
VC0 = 0

t_s = sp.symbols('t', real = True)
I_s = sp.symbols('I', cls = sp.Function)
#################################################################################
# Calculo diferencial
#################################################################################
# Ecuación diferencial
eq = L * I_s(t_s).diff(t_s,1) + R2 * I_s(t_s) - V0

# Igualo a las condiciones iniciales
init_values = {I_s(0) : IL0}

#Resolvemos la ecuación diferencial
res = sp.dsolve(eq, I_s(t_s), ics = init_values).args
#print(res)
I_symbol = res[1]

I_lambda = sp.lambdify(t_s, I_symbol, modules = 'numpy')

t = np.linspace(0, .495, 10000)
IL = I_lambda(t)
ax_c.plot(t+0.005, IL, 'orange')

t2 = np.linspace(0, .495, 10000)
VL = V0*np.exp(-(R2/L)*t2)
ax_f.plot(t+0.005, VL, 'orange')
#################################################################################
# EXTRA
#################################################################################
plt.grid(True)
# agregamos patches
patches = [
    mpatches.Patch(color="blue", label="Curva de simulacion I(t)"),
	mpatches.Patch(color="red", label="Curva de simulacion V(t)"),
    mpatches.Patch(color="orange" , label="Curva teorica")
]
plt.legend(handles=patches, loc ='center right')
plt.minorticks_on()
plt.grid(which = 'major', linestyle = '--', color = 'black', linewidth = 0.8)
plt.grid(which = 'minor', linestyle = ':', color = 'black', linewidth = 0.4)

#Mostramos todo
plt.show()