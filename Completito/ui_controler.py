""" Creacion de una ventana integrando el backend de Matplotlib!
"""

# PyQt5 Modules
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import pyqtSlot

# Matplotlib Modules
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Project Modules
from ui.matplotlib import Ui_Form

# Python Modules
from numpy import *
from time import *
from random import *


class MatplotlibWidget(QWidget, Ui_Form):
    """ Creamos nuestra clase MatplotlibWidget, heredo de QWidget porque asi lo defino en QtDesigner,
        y luego heredo la forma compilada que tenemos en la carpeta /ui
    """

    def __init__(self):
        super(MatplotlibWidget, self).__init__()        # Llamamos al constructor de los padres
        self.setupUi(self)                              # Necesitamos usar esto para hacer el build de los componentes
        seed(time())                                    # Random seed para generacion aleatoria

        # Tenemos que utilizar el backend que provee Matplotlib para PyQt y crear un FigureCanvas,
        # son las entidades encargadas de proveer el soporte grafico necesario para dibujar en pantalla
        # y basicamente hacen la magica.
        #
        # Asi como FigureCanvas es el control del entorno grafico donde dibujamos, Figure
        # corresponde al espacio utilizado para dibujar y despues sobre el se agregan pares de ejes.
        #self.figure = Figure()
        #self.canvas = FigureCanvas(self.figure)

        # A partir de aca es lo mismo que con pyplot, solo que el manejo no es automatico, sino
        # que lo hace uno con criterio, entonces creamos un par de ejes
        #self.axes = self.figure.add_subplot()

        #canvas_index = self.plotter_container.addWidget(self.canvas)
        #self.plotter_container.setCurrentIndex(canvas_index)

        # Algo mas emocionante, cambiemos el contenido con un callback al boton de pantalla!
        #self.update_button.clicked.connect(self.on_plot_update)

    @pyqtSlot()
    def on_plot_update(self):
        """ Slot/Callback usado para actualizar datos en el Axes """

        # Creamos un puntos para el eje x y para el eje y!
        x_axis = linspace(0, 2 * pi, num=1000)
        y_axis = sin(x_axis * randint(1, 5))

        # Limpiamos el axes, agregamos los puntos, y actualizamos el canvas
        # IMPORTANTE! Te invito a comentar para que veas la importancia del .clear() y .draw()
        self.axes.clear()
        self.axes.plot(x_axis, y_axis, label="Señal")   # Nuevo, podemos agregarle un label y activar con .legend()

        # Configuramos los ejes para que tengan un label
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [V]")

        self.axes_configuration()

        self.figure.legend()
        self.canvas.draw()

    def axes_configuration(self):
        """ Agrego una configuracion al axes, no hace falta un metodo nuevo, simplemente separacion
            para mayor claridad del ejemplo! """

        # Podemos agregar una grilla
        self.axes.minorticks_on()                           # Necesitamos esto para usar los ticks menores!
        self.axes.grid(b=True, which="both", axis="both")   # Podes elegir que eje y si es para ticks mayores/menores

###############################################################################################################
###############################################################################################################

"""
    Este ejemplo muestra como leer input del usuario y como hacer para que la GUI responda a dicho input
"""



class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)	# como siempre, inicializamos todo

        self.setWindowTitle("InputFetching")	# titulo de la ventana
        self.input_line.textChanged.connect(self.update_bar)	# CADA VEZ que cambie el texto se llamara al callback
        """ El QIntValidator no deja que ingresen nada mas que numeros enteros.
            Mas info sobre validators: 
            https://doc.qt.io/qtforpython/PySide2/QtGui/QRegExpValidator.html#qregexpvalidator """
        self.input_line.setValidator(QtGui.QIntValidator(1, 12, self))
        self.capacity_bar.setValue(100)	# valor inicial de la barra de capacidad
        self.msg_oculto.hide()	# oculto lo que voy a mostrar mas adelante

    def update_bar(self):
        text = self.input_line.text()	# levanto entrada que acaban de ingresar
        if text:	# si hay algo escrito
            """ Puedo castear directo a int porque el validator solo permite que ingresen numeros enteros """
            input = int(self.input_line.text())
            if input:	# si el valor ingresado es 0 no hago nada
                self.capacity_bar.setValue(1/input**2*100)	# cambia la barra de capacidad en funcion de la entrada
                if self.capacity_bar.value() == 0:	# si llego a cero, muestro el mensaje oculto
                    self.msg_oculto.setText("Tenes la misma capacidad neuronal que yo cuando escribi esto :)")
                    self.msg_oculto.show()
                else:
                    self.msg_oculto.hide()
        else:	# si no ingresaron nada seteo 100%
            self.capacity_bar.setValue(100)

############################################################################################################################
###########################################################################################################################


""" Esta es una aplicacion simple que al mover un Slider actualiza el contenido
    de una display numerico en la pantalla. Simple conexion de dos eventos, pero tambien
    a traves del QtDesigner se puede hacer directo.
"""

# PyQt5 Modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

# Python Modules

# Example Modules
from ui.slider import Ui_test_form


class SliderWidget(QWidget, Ui_test_form):
    """ SliderWidget ejemplo, siempre tenemos que heredar el padre original de lo que estamos implementando,
    y ademas la compilacion del QtDesigner. """

    # Creamos el constructor de la clase y luego con super() llamamos
    # al constructor del padre, con herencia multiple python lo maneja solo
    def __init__(self):
        super(SliderWidget, self).__init__()

        # Hacemos un build de la Widget
        self.setupUi(self)

        # Conexion signal (evento) con slot (callback)
        self.slider.valueChanged.connect(self.update_number)

    @pyqtSlot(int)
    def update_number(self, value: int):
        self.number.display(value)
