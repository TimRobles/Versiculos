import requests, sys, os, json, time
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
tildes={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U'}
urlBase="https://api.scripture.api.bible"
token='d1eded304a6a68a4befc685b42447bcf'

def QDateASQL(QFecha):
    return "%s-%s-%s" % (str(QFecha.date().year()), "0"*(2-len(str(QFecha.date().month()))) + str(QFecha.date().month()), "0"*(2-len(str(QFecha.date().day()))) + str(QFecha.date().day()))

def leerData():
    try:
        with open('data.json') as file:
            return json.load(file)
    except Exception as e:
        with open('data.json', 'w') as file:
            json.dump({}, file, indent=4)
            return {}

def subirData(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def modificarData(key, value):
    data=leerData()
    data[key]=value
    subirData(data)

def leerHistorial():
    try:
        with open('historial.json') as file:
            return json.load(file)
    except Exception as e:
        with open('historial.json', 'w') as file:
            json.dump({str(date.today()):[]}, file, indent=4)
            return {str(date.today()):[]}

def subirHistorial(data):
    with open('historial.json', 'w') as file:
        json.dump(data, file, indent=4)

def agregarHistorial(key, value):
    data=leerHistorial()
    if not key in data: data[key]=[]
    data[key].append(value)
    subirHistorial(data)

def esnumero(texto):
    try:
        numero=float(texto)
        return True
    except Exception as e:
        return False

def quitarTildes(texto):
    textoSinTildes=texto
    for k,v in tildes.items():
        textoSinTildes=textoSinTildes.replace(k,v)
        textoSinTildes=textoSinTildes.replace(k.lower(),v.lower())
    return textoSinTildes

def buscarIndex(cb,texto):
    for i in range(cb.count()):
        if quitarTildes(texto.lower())==quitarTildes(cb.itemText(i).lower())[0:len(texto)]:
            cb.setCurrentIndex(i)
            return
    cb.setCurrentIndex(0)

class Mostrar(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mostrar.ui",self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("main.ui",self)

        self.deFecha.setDate(date.today())
        self.showMaximized()
        self.data=leerData()
        self.cargarHistorial()
        self.cargarDatos()
        self.cargarLibros()

        self.mostrar=Mostrar()
        self.mostrar.show()
        self.datosMostrar()


        self.animacion=QPropertyAnimation(self.hsTransparencia, b'value')
        self.hsTransparencia.valueChanged.connect(self.escalarTransparencia)

        self.btnColorFuente.clicked.connect(self.seleccionarColorFuente)
        self.btnColorFondo.clicked.connect(self.seleccionarColorFondo)

        self.lePasaje.textChanged.connect(self.separar)

        self.sbAltura.valueChanged.connect(self.guardarAltura)
        self.sbAncho.valueChanged.connect(self.guardarAncho)
        self.sbMargen.valueChanged.connect(self.guardarMargen)
        self.sbFuente.valueChanged.connect(self.guardarFuente)

        self.deFecha.dateChanged.connect(self.cargarHistorial)
        self.cbHistorial.currentIndexChanged.connect(self.consultarHistorial)

        self.cbBiblia.currentIndexChanged.connect(self.cargarVersion)
        self.cbLibro.currentIndexChanged.connect(self.cargarCapitulos)
        self.cbCapitulo.currentIndexChanged.connect(self.cargarVersiculos)
        self.cbVersiculo.currentIndexChanged.connect(self.leerVersiculo)

        self.btnEnviar.clicked.connect(self.enviarVersiculo)
        self.btnLimpiar.clicked.connect(self.limpiarVersiculo)
        self.btnOcultarMostrar.clicked.connect(self.ocultarMostrar)
        self.btnSiguiente.clicked.connect(self.siguiente)
        self.btnAnterior.clicked.connect(self.anterior)

    def datosMostrar(self):
        self.data=leerData()
        self.mostrar.textEdit.setMaximumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.textEdit.setMinimumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.widget.setMaximumSize(self.data["sbAncho"], self.data["sbMargen"])
        self.mostrar.widget.setMinimumSize(self.data["sbAncho"], self.data["sbMargen"])
        self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgb(%s); color: rgb(%s)" % (",".join(self.data["colorFondo"]), ",".join(self.data["colorFuente"])))

    def seleccionarColorFuente(self):
        colorInicial=QColor()
        dato=self.data["colorFuente"]
        colorInicial.setRgb(int(dato[0]), int(dato[1]), int(dato[2]), int(dato[3]))
        color = QColorDialog.getColor(colorInicial, self, "Color de Fuente")
        modificarData("colorFuente", [str(color.red()), str(color.green()), str(color.blue()), str(self.hsTransparencia.value()*255/100)])
        self.datosMostrar()

    def seleccionarColorFondo(self):
        colorInicial=QColor()
        dato=self.data["colorFondo"]
        colorInicial.setRgb(int(dato[0]), int(dato[1]), int(dato[2]), int(dato[3]))
        color = QColorDialog.getColor(colorInicial, self, "Color de Fondo")
        modificarData("colorFondo", [str(color.red()), str(color.green()), str(color.blue()), str(self.hsTransparencia.value()*255/100)])
        self.datosMostrar()

    def cargarVersion(self):
        self.data=leerData()
        version=self.data["cbBiblia"][self.cbBiblia.currentText()]
        with open(version) as file:
            self.biblia=json.load(file)

    def cargarDatos(self):
        if not "colorFuente" in self.data:
            modificarData("colorFuente", ["0", "0", "0", "255"])
        if not "colorFondo" in self.data:
            modificarData("colorFondo", ["138", "226", "52", "255"])
        if "sbAltura" in self.data:
            self.sbAltura.setValue(self.data["sbAltura"])
        else:
            self.sbAltura.setValue(100)
            modificarData("sbAltura", 100)
        if "sbAncho" in self.data:
            self.sbAncho.setValue(self.data["sbAncho"])
        else:
            self.sbAncho.setValue(100)
            modificarData("sbAncho", 100)
        if "sbMargen" in self.data:
            self.sbMargen.setValue(self.data["sbMargen"])
        else:
            self.sbMargen.setValue(100)
            modificarData("sbMargen", 100)
        if "sbFuente" in self.data:
            self.sbFuente.setValue(self.data["sbFuente"])
        else:
            self.sbFuente.setValue(12)
            modificarData("sbFuente", 12)
        if "cbBiblia" in self.data:
            self.cbBiblia.clear()
            for dato in self.data["cbBiblia"]:
                self.cbBiblia.addItem(dato)
        else:
            versiones={"RVR60": "RVR60.json"}
            modificarData("cbBiblia", versiones)
            self.cbBiblia.clear()
            for dato in versiones:
                self.cbBiblia.addItem(dato)
        self.cargarVersion()
        self.hsTransparencia.setValue(int(round(float(self.data["colorFuente"][3])*100/255,0)))

    def cargarLibros(self):
        self.cbLibro.clear()
        self.cbLibro.addItem("--LIBRO--")
        for libro in self.biblia:
            self.cbLibro.addItem(libro["nombre"])

    def cargarCapitulos(self):
        if self.cbLibro.currentText()=="--LIBRO--" or self.cbLibro.currentText()=="":
            self.cbCapitulo.clear()
            # self.cbVersiculo.clear()
            return
        self.cbCapitulo.clear()
        self.cbCapitulo.addItem("--CAPITULO--")
        for libro in self.biblia:
            if libro["nombre"]==self.cbLibro.currentText():
                for i in range(len(libro["capitulos"])-1):
                    self.cbCapitulo.addItem(str(i+1))

    def cargarVersiculos(self):
        if self.cbCapitulo.currentText()=="--CAPITULO--" or self.cbCapitulo.currentText()=="":
            self.cbVersiculo.clear()
            # self.cbVersiculo.clear()
            return
        self.cbVersiculo.clear()
        self.cbVersiculo.addItem("--VERSICULO--")
        for libro in self.biblia:
            if libro["nombre"]==self.cbLibro.currentText():
                for i in range(len(libro["capitulos"][int(self.cbCapitulo.currentText())-1])):
                    self.cbVersiculo.addItem(str(i+1))

    def leerVersiculo(self):
        if self.cbVersiculo.currentText()=="--VERSICULO--" or self.cbVersiculo.currentText()=="":
            self.tePrev.clear()
            self.tePrevMas1.clear()
            self.tePrevMas2.clear()
            self.tePrevMenos1.clear()
            self.tePrevMenos2.clear()
            return
        for libro in self.biblia:
            if libro["nombre"]==self.cbLibro.currentText():
                self.tePrev.clear()
                self.tePrevMas1.clear()
                self.tePrevMas2.clear()
                self.tePrevMenos1.clear()
                self.tePrevMenos2.clear()
                capitulo=int(self.cbCapitulo.currentText())-1
                versiculo=int(self.cbVersiculo.currentText())-1
                verMenos1=versiculo-1
                verMenos2=versiculo-2
                verMas1=versiculo+1
                verMas2=versiculo+2

                self.tePrev.insertHtml('<p style="text-align:center; font-size:%ipx;"><strong>%s %i:%i</strong> %s | %s</p>' % (self.sbFuente.value(), self.cbLibro.currentText(), capitulo+1, versiculo+1, libro["capitulos"][capitulo][versiculo], self.cbBiblia.currentText()))

                if verMenos1 in range(self.cbVersiculo.count()-1): self.tePrevMenos1.insertHtml('<p style="text-align:center; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMenos1+1, libro["capitulos"][capitulo][verMenos1]))

                if verMenos2 in range(self.cbVersiculo.count()-1): self.tePrevMenos2.insertHtml('<p style="text-align:center; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMenos2+1, libro["capitulos"][capitulo][verMenos2]))

                if verMas1 in range(self.cbVersiculo.count()-1): self.tePrevMas1.insertHtml('<p style="text-align:center; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMas1+1, libro["capitulos"][capitulo][verMas1]))

                if verMas2 in range(self.cbVersiculo.count()-1): self.tePrevMas2.insertHtml('<p style="text-align:center; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMas2+1, libro["capitulos"][capitulo][verMas2]))

    def guardarAltura(self):
        modificarData("sbAltura", self.sbAltura.value())
        self.datosMostrar()

    def guardarAncho(self):
        modificarData("sbAncho", self.sbAncho.value())
        self.datosMostrar()

    def guardarMargen(self):
        modificarData("sbMargen", self.sbMargen.value())
        self.datosMostrar()

    def guardarFuente(self):
        modificarData("sbFuente", self.sbFuente.value())
        self.leerVersiculo()

    def separar(self):
        texto=self.lePasaje.text()
        if texto!="":
            division=texto.split(" ")
            numeros=[]
            if ":" in division[-1]: numeros=division[-1].split(":")
            if "." in division[-1]: numeros=division[-1].split(".")
            if len(division)==1:
                buscarIndex(self.cbLibro, texto)
            elif len(division)==2 and (esnumero(division[1]) or division[1]=="" or numeros!=[]):
                buscarIndex(self.cbLibro, division[0])
            else:
                buscarIndex(self.cbLibro, " ".join(division[0:2]))

            try:
                buscarIndex(self.cbCapitulo, numeros[0])
            except Exception as e:
                self.cbCapitulo.setCurrentIndex(0)
            try:
                buscarIndex(self.cbVersiculo, numeros[1])
            except Exception as e:
                self.cbVersiculo.setCurrentIndex(0)
        else:
            self.cbLibro.setCurrentIndex(0)

    def consultarHistorial(self):
        if self.cambiar:
            historial=self.cbHistorial.currentText()
            dividir=historial.split(" | ")
            version=dividir[1]
            dividir2=dividir[0].split(":")
            dividir3=dividir2[0].split(" ")
            libro=" ".join(dividir3[0:-1])
            capitulo=dividir3[-1]
            versiculo=dividir2[1].split(" ")[0]
            buscarIndex(self.cbBiblia, version)
            buscarIndex(self.cbLibro, libro)
            buscarIndex(self.cbCapitulo, capitulo)
            buscarIndex(self.cbVersiculo, versiculo)

    def cargarHistorial(self):
        self.cambiar=False
        self.historial=leerHistorial()
        if QDateASQL(self.deFecha) in self.historial:
            indice=self.cbHistorial.currentIndex()
            self.cbHistorial.clear()
            for versiculo in self.historial[QDateASQL(self.deFecha)]:
                self.cbHistorial.addItem(versiculo)
            self.cbHistorial.setCurrentIndex(indice)
        else:
            self.cbHistorial.clear()
        self.cambiar=True

    def enviarVersiculo(self):
        self.mostrar.textEdit.clear()
        self.mostrar.textEdit.insertHtml(self.tePrev.toHtml())
        agregarHistorial(QDateASQL(self.deFecha), self.tePrev.toPlainText())
        self.cargarHistorial()

    def limpiarVersiculo(self):
        self.mostrar.textEdit.clear()

    def escalarTransparencia(self, value):
        self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgb(%s); color: rgb(%s)" % (",".join(self.data["colorFondo"][0:-1] + [str(value*255/100)]), ",".join(self.data["colorFuente"][0:-1] + [str(value*255/100)])))
        modificarData("colorFuente", self.data["colorFuente"][0:-1]+[str(value*255/100)])
        modificarData("colorFondo", self.data["colorFondo"][0:-1]+[str(value*255/100)])
        if value==0:
            self.btnOcultarMostrar.setText("Mostrar")
        else:
            self.btnOcultarMostrar.setText("Ocultar")

    def ocultarMostrar(self):
        if self.btnOcultarMostrar.text()=="Ocultar":
            self.animacion.setDuration(10*self.hsTransparencia.value())
            self.animacion.setStartValue(self.hsTransparencia.value())
            self.animacion.setEndValue(0)
            self.animacion.start()
            self.btnOcultarMostrar.setText("Mostrar")
        else:
            self.animacion.setDuration(10*(100-self.hsTransparencia.value()))
            self.animacion.setStartValue(self.hsTransparencia.value())
            self.animacion.setEndValue(100)
            self.animacion.start()
            self.btnOcultarMostrar.setText("Ocultar")

    def siguiente(self):
        if self.cbLibro.currentText() in self.tePrevMas1.toHtml():
            self.cbVersiculo.setCurrentIndex(self.cbVersiculo.currentIndex()+1)
            self.enviarVersiculo()

    def anterior(self):
        if self.cbLibro.currentText() in self.tePrevMenos1.toHtml():
            self.cbVersiculo.setCurrentIndex(self.cbVersiculo.currentIndex()-1)
            self.enviarVersiculo()

app=QApplication(sys.argv) #Instancia para iniciar una aplicación
_main=Principal() #Crear un objeto de la clase / Como el Load en VBA
_main.show() #Mostrar la ventana
app.exec_() #Ejecutar applicación
