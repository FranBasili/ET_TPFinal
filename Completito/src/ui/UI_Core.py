from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from design import Ui_MainWindow
import numpy as np
import sys
import scipy.signal as ss



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)	# como siempre, inicializamos todo

        self.okbtn.clicked.connect(self.btn1Click)   # Boton parte 1
        self.okbtn_ok.clicked.connect(self.btn2Click)    # Boton parte 2

        self.filterType = ""

        self.actionPasa_Bajos.triggered.connect(self.setPasaBajos)
        self.actionPasa_Altos.triggered.connect(self.setPasaAltos)
        self.actionPasa_Todo.triggered.connect(self.setPasaTodo)
        self.actionPasa_Altos_2.triggered.connect(self.setPasaAltos2)
        self.actionPasa_Bajos_2.triggered.connect(self.setPasaBajos2)
        self.actionPasa_Banda.triggered.connect(self.setPasaBanda)
        self.actionPasa_Todo_2.triggered.connect(self.setPasaTodo2)
        self.actionNotch.triggered.connect(self.setNotch)


    def setPasaBajos(self):
        self.filterType = "PasaBajos"
    
    def setPasaAltos(self):
        self.filterType = "PasaAltos"    

    def setPasaTodo(self):
        self.filterType = "PasaTodo"
        
    def setPasaBajos2(self):
        self.filterType = "PasaBajos2"
        
    def setPasaAltos2(self):
        self.filterType = "PasaAltos2"
    
    def setNotch(self):
        self.filterType = "Notch"

    def setPasaBanda(self):
        self.filterType = "PasaBanda"        
    
    def setPasaTodo2(self):
        self.filterType = "PasaTodo2"                 
    
    
    def btn1Click(self):
        # num = [1, 5]
        # den = [1, 5, 6]
        # k=10
        # print("Filtro:", self.filterType)
        if self.filterType:     # Solo actuamos si hay un filtro seleccionao
            num = [1]
            den = [1]
            k = self.kt.value()

            # Vemos tipo de filtro:

            if self.filterType == "PasaBajos":
                num = [ 1 ]
                den = [ 1/self.wopt.value(), 1]
                
            elif self.filterType == "PasaAltos":
                num = [1, 0]
                den = [ 1/self.wopt.value(), 1]
            
            elif self.filterType == "PasaTodo":
                num = [ 1/self.woct.value(), -1]
                den = [ 1/self.woct.value(), 1]

            elif self.filterType == "PasaBajos2":
                num = [ 1 ]
                den = [ 1/(self.wopt_2.value()**2), 2*self.xipt_2.value()/self.wopt_2.value(), 1 ]

            elif self.filterType == "PasaAltos2":
                num = [ 1, 0, 0 ]
                den = [ 1/(self.wopt_2.value()**2), 2*self.xipt_2.value()/self.wopt_2.value(), 1 ]

            elif self.filterType == "PasaTodo2":
                num = [ 1/(self.woct_4.value()**2), -2*self.xict_2.value()/self.woct_4.value(), 1 ]
                den = [ 1/(self.woct_4.value()**2), 2*self.xict_2.value()/self.woct_4.value(), 1 ]

            elif self.filterType == "PasaBanda":
                num = [ 1, 0 ]
                den = [ 1/(self.wopt_2.value()**2), 2*self.xipt_2.value()/self.wopt_2.value(), 1 ]
                
            elif self.filterType == "Notch":
                num = [ 1/self.woct_4.value()**2, 0, 1]
                den = [ 1/(self.woct_4.value()**2), 2*self.xict_2.value()/self.woct_4.value(), 1 ]

            
            num = np.polymul(num,k)
            H=ss.TransferFunction(num, den)

            self.Bode_Graph_Modulo.plotBodeModule(H)
            self.Bode_Graph_Fase.plotBodePhase(H)
            self.PyC_Graph.plotZerosPoles(H)

            if self.pulsobtn.isChecked():
                u = "escalon"
            elif self.senoidalbtn.isChecked():
                u = "seno"
            self.Respuesta_Graph.filterImpulse(H=H, u=u, w=self.wo_senoidalt.value(), A=self.amplitudt.value())

        else:
            self.Bode_Graph_Modulo.clearAxis()
            self.Bode_Graph_Fase.clearAxis()
            self.PyC_Graph.clearAxis()
            self.Respuesta_Graph.clearAxis()

    def btn2Click(self):
        v1 = 0
        v2 = 0

        if self.V1_0.isChecked():
            v1 = 1
        elif self.V2_0.isChecked():
            v1 = 2
        elif self.V3_0.isChecked():
            v1 = 3
        elif self.V4_0.isChecked():
            v1 = 4
            
        if self.V1_1.isChecked():
            v2 = 1
        elif self.V2_1.isChecked():
            v2 = 2
        elif self.V3_1.isChecked():
            v2 = 3
        elif self.V4_1.isChecked():
            v2 = 4

        if v1 != v2:
            self.Bode_Graph_2.RLCSim(v1, v2, self.R_box.value()*1E3, self._Lbox.value()*1E-3, self.C_box.value()*1E-9)
        else:
            self.Bode_Graph_2.clearFigure()

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
 