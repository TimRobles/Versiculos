from funciones import *
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import threading

api_app = FastAPI()
letras_global = ""
server_running = False

@api_app.get("/letras", response_class=HTMLResponse)
def get_letras():
    return f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Letras de la Canción</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        <h2>Letras de la Canción</h2>
        <pre>{letras_global}</pre>
    </body>
    </html>
    """

def api_mostrar(letras):
    global letras_global, server_running
    letras_global = letras.replace("\r", "").replace("\n", "<br>")
    if not server_running:
        server_running = True
        threading.Thread(
            target=lambda: uvicorn.run(api_app, host="0.0.0.0", port=5000, log_level="info"),
            daemon=True
        ).start()

class LetrasEditar(QMainWindow):
    def __init__(self, url, cancion, artista, album, letras_texto):
        QMainWindow.__init__(self)
        uic.loadUi("letras_editar.ui",self)
        self.url = url
        self.cancion = cancion
        self.artista = artista
        self.album = album
        self.teLetra.setText(letras_texto)
        self.show()
    
    def closeEvent(self, event):
        letras = self.teLetra.toPlainText()
        print("Guardar letras")
        modificarCanciones(self.url, [self.artista, self.album, self.cancion, letras])
        event.accept()

class Mostrar(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mostrar.ui",self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

class MostrarPantalla(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mostrar pantalla.ui",self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showMaximized()

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("main.ui",self)

        self.deFecha.setDate(date.today())
        self.showMaximized()
        self.cargarFuentes()
        self.cargarHistorial()
        self.cargarDatos()
        self.cargarLibros()

        self.mostrar=Mostrar()
        self.mostrar_pantalla=MostrarPantalla()
        self.mostrar.show()
        self.mostrar_pantalla.show()
        self.datosMostrar()
        colorFondo=self.data["colorFondo"]
        colorFuente=self.data["colorFuente"]
        colorFondox=self.data["colorFondox"]
        colorFuentex=self.data["colorFuentex"]
        self.mostrar.label.setStyleSheet("border-radius:15px; background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondo[0], colorFondo[1], colorFondo[2],  int(self.data["sbTransparenciaMax"]*255/100), colorFuente[0], colorFuente[1], colorFuente[2], 0))
        self.mostrar_pantalla.label.setStyleSheet("background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondox[0], colorFondox[1], colorFondox[2],  int(self.data["sbTransparenciaMax"]*255/100), colorFuentex[0], colorFuentex[1], colorFuentex[2], 0))

        self.animacion=QPropertyAnimation(self.hsTransparencia, b'value')
        self.animacionAltura=QPropertyAnimation(self.hsAltura, b'value')
        self.animacionTextoDesaparecer=QPropertyAnimation(self.hsTransparenciaTexto, b'value')
        self.animacionTextoAparecer=QPropertyAnimation(self.hsTransparenciaTexto, b'value')
        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.animacionTextoDesaparecer)
        self.anim_group.addAnimation(self.animacionTextoAparecer)

        self.hsAltura.valueChanged.connect(self.cambiarAltura)
        self.hsTransparencia.valueChanged.connect(self.escalarTransparenciaTotal)
        self.hsTransparenciaTexto.valueChanged.connect(self.escalarTransparenciaTexto)
        self.sbTransparenciaMax.valueChanged.connect(self.guardarTransparencia)

        self.btnMostrar.clicked.connect(self.mostrarTextEdits)

        self.btnColorFuente.clicked.connect(self.seleccionarColorFuente)
        self.btnColorFondo.clicked.connect(self.seleccionarColorFondo)

        self.btnColorFuentex.clicked.connect(self.seleccionarColorFuentex)
        self.btnColorFondox.clicked.connect(self.seleccionarColorFondox)

        self.btnUpdate.clicked.connect(self.actualizarSistema)

        self.lePasaje.textChanged.connect(self.separar)

        self.sbAltura.valueChanged.connect(self.guardarAltura)
        self.sbAncho.valueChanged.connect(self.guardarAncho)
        self.sbMargen.valueChanged.connect(self.guardarMargen)
        self.cbFuente.currentIndexChanged.connect(self.guardarFuente)
        self.sbFuente.valueChanged.connect(self.guardarFuenteTamano)

        self.sbAlturax.valueChanged.connect(self.guardarAlturax)
        self.sbAnchox.valueChanged.connect(self.guardarAnchox)
        self.sbMargenx.valueChanged.connect(self.guardarMargenx)
        self.cbFuentex.currentIndexChanged.connect(self.guardarFuentex)
        self.sbFuentex.valueChanged.connect(self.guardarFuenteTamanox)

        self.deFecha.dateChanged.connect(self.cargarHistorial)
        self.cbHistorial.currentIndexChanged.connect(self.consultarHistorial)

        self.cbBiblia.currentIndexChanged.connect(self.cargarVersion)
        self.cbLibro.currentIndexChanged.connect(self.cargarCapitulos)
        self.cbCapitulo.currentIndexChanged.connect(self.cargarVersiculos)
        self.cbVersiculo.currentIndexChanged.connect(self.leerVersiculo)

        self.btnEnviar.clicked.connect(self.enviarPrevisualizacion)
        self.btnLimpiar.clicked.connect(self.limpiarPrevisualizacion)
        self.btnOcultarMostrar.clicked.connect(self.ocultarMostrar)
        self.btnSiguienteV.clicked.connect(self.siguienteVersiculo)
        self.btnAnteriorV.clicked.connect(self.anteriorVersiculo)

        self.btnGuardarCondV.clicked.connect(self.guardarCondicionesV)
        self.btnCargarCondV.clicked.connect(self.cargarCondicionesV)
        self.btnGuardarCondC.clicked.connect(self.guardarCondicionesC)
        self.btnCargarCondC.clicked.connect(self.cargarCondicionesC)

        self.cargarCanciones()
        self.cargarCancionesHoy()

        self.btnBuscarCancion.clicked.connect(self.buscarCancion)
        self.btnCargarTodas.clicked.connect(self.cargarTodas)
        self.btnActualizar.clicked.connect(self.cargarCanciones)
        self.btnAPI.clicked.connect(self.cargarAPI)
        self.leBuscar.textChanged.connect(self.buscarCancionRegistrada)
        self.twCancionesRegistradas.itemDoubleClicked.connect(self.agregarCancion)
        self.twCancionesHoy.itemDoubleClicked.connect(self.elegirCancion)
        self.twLetras.itemDoubleClicked.connect(self.elegirLetra)
        self.btnSiguienteC.clicked.connect(self.siguienteParrafo)
        self.btnAnteriorC.clicked.connect(self.anteriorParrafo)

        self.btnBuscar.clicked.connect(self.buscarConcordancia)
        self.twConcordancia.itemDoubleClicked.connect(self.usarVersiculo)

    def cargarFuentes(self):
        for fuente in QFontDatabase().families(QFontDatabase.Latin):
            self.cbFuente.addItem(fuente)
        for fuente in QFontDatabase().families(QFontDatabase.Latin):
            self.cbFuentex.addItem(fuente)

    def datosMostrar(self):
        self.data=leerData()
        self.mostrar.label.setMaximumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.label.setMinimumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.widget.setMaximumSize(self.data["sbAncho"], self.data["sbMargen"])
        self.mostrar.widget.setMinimumSize(self.data["sbAncho"], self.data["sbMargen"])

        self.mostrar_pantalla.label.setMaximumSize(self.data["sbAnchox"], self.data["sbAlturax"])
        self.mostrar_pantalla.label.setMinimumSize(self.data["sbAnchox"], self.data["sbAlturax"])
        self.mostrar_pantalla.widget.setMaximumSize(self.data["sbAnchox"], self.data["sbMargenx"])
        self.mostrar_pantalla.widget.setMinimumSize(self.data["sbAnchox"], self.data["sbMargenx"])

    def seleccionarColorFuente(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFuente"]
            colorInicial.setRgb(dato[0], dato[1], dato[2], dato[3])
            color = QColorDialog.getColor(colorInicial, self, "Color de Fuente")
            modificarData("colorFuente", [color.red(), color.green(), color.blue(), int(self.hsTransparencia.value()*255/100)])
            self.datosMostrar()
        except Exception as e:
            print(e)

    def seleccionarColorFondo(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFondo"]
            colorInicial.setRgb(dato[0], dato[1], dato[2], dato[3])
            color = QColorDialog.getColor(colorInicial, self, "Color de Fondo")
            modificarData("colorFondo", [color.red(), color.green(), color.blue(), int(self.hsTransparencia.value()*255/100)])
            self.datosMostrar()
        except Exception as e:
            print(e)

    def seleccionarColorFuentex(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFuentex"]
            colorInicial.setRgb(dato[0], dato[1], dato[2], dato[3])
            color = QColorDialog.getColor(colorInicial, self, "Color de Fuente")
            modificarData("colorFuentex", [color.red(), color.green(), color.blue(), 255])
            self.datosMostrar()
        except Exception as e:
            print(e)

    def seleccionarColorFondox(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFondox"]
            colorInicial.setRgb(dato[0], dato[1], dato[2], dato[3])
            color = QColorDialog.getColor(colorInicial, self, "Color de Fondo")
            modificarData("colorFondox", [color.red(), color.green(), color.blue(), 255])
            self.datosMostrar()
        except Exception as e:
            print(e)

    def actualizarSistema(self):
        try:
            g = git.cmd.Git(os.getcwd())
            msg=g.pull()
            print(msg)
            if msg=="Already up to date.":
                print("Actualización", "Ya está actualizado")
            if "Updating" in msg:
                print("Actualización", "Sistema actualizado")
                self.mostrar.close()
                self.mostrar_pantalla.close()
                self.close()
        except Exception as e:
            print("Error", msg + "\n" + e)

    def cargarVersion(self):
        self.data=leerData()
        if self.cbBiblia.currentText()=="": return
        version=self.data["cbBiblia"][self.cbBiblia.currentText()]
        with open("Versiones/" + version) as file:
            self.biblia=json.load(file)
        self.cargarLibros()

    def cargarDatos(self):
        self.data=leerData()
        if not "colorFuente" in self.data:
            modificarData("colorFuente", [0, 0, 0, 255])
        if not "colorFondo" in self.data:
            modificarData("colorFondo", [138, 226, 52, 255])
        if "sbTransparenciaMax" in self.data:
            self.sbTransparenciaMax.setValue(self.data["sbTransparenciaMax"])
        else:
            self.sbTransparenciaMax.setValue(100)
            modificarData("sbTransparenciaMax", 100)
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
        if "cbFuente" in self.data:
            buscarIndex(self.cbFuente, self.data["cbFuente"])
        else:
            self.cbFuente.setCurrentIndex(-1)
            modificarData("cbFuente", "")

        
        if not "colorFuentex" in self.data:
            modificarData("colorFuentex", [0, 0, 0, 255])
        if not "colorFondox" in self.data:
            modificarData("colorFondox", [138, 226, 52, 255])
        if "sbAlturax" in self.data:
            self.sbAlturax.setValue(self.data["sbAlturax"])
        else:
            self.sbAlturax.setValue(100)
            modificarData("sbAlturax", 100)
        if "sbAnchox" in self.data:
            self.sbAnchox.setValue(self.data["sbAnchox"])
        else:
            self.sbAnchox.setValue(100)
            modificarData("sbAnchox", 100)
        if "sbMargenx" in self.data:
            self.sbMargenx.setValue(self.data["sbMargenx"])
        else:
            self.sbMargenx.setValue(100)
            modificarData("sbMargenx", 100)
        if "sbFuentex" in self.data:
            self.sbFuentex.setValue(self.data["sbFuentex"])
        else:
            self.sbFuentex.setValue(12)
            modificarData("sbFuentex", 12)
        if "cbFuentex" in self.data:
            buscarIndex(self.cbFuentex, self.data["cbFuentex"])
        else:
            self.cbFuentex.setCurrentIndex(-1)
            modificarData("cbFuentex", "")

        if "cbBiblia" in self.data:
            self.cbBiblia.clear()
            for dato in self.data["cbBiblia"]:
                self.cbBiblia.addItem(dato)
        else:
            versiones={"RVR60": "RVR60.json", "NVI": "NVI.json"}
            modificarData("cbBiblia", versiones)
            self.cbBiblia.clear()
            for dato in versiones:
                self.cbBiblia.addItem(dato)
        self.cargarVersion()
        self.hsTransparencia.setValue(int(self.data["sbTransparenciaMax"]))

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

    def cargarTextos(self, previsual, prevMenos1, prevMenos2, prevMas1, prevMas2):
        self.tePrev.clear()
        self.tePrevMas1.clear()
        self.tePrevMas2.clear()
        self.tePrevMenos1.clear()
        self.tePrevMenos2.clear()

        self.tePrev.insertHtml("<div>" + previsual + "</div>")
        self.tePrevMenos1.insertHtml("<div>" + prevMenos1 + "</div>")
        self.tePrevMenos2.insertHtml("<div>" + prevMenos2 + "</div>")
        self.tePrevMas1.insertHtml("<div>" + prevMas1 + "</div>")
        self.tePrevMas2.insertHtml("<div>" + prevMas2 + "</div>")

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
                capitulo=int(self.cbCapitulo.currentText())-1
                versiculo=int(self.cbVersiculo.currentText())-1
                verMenos1=versiculo-1
                verMenos2=versiculo-2
                verMas1=versiculo+1
                verMas2=versiculo+2

                previsual=""
                prevMenos1=""
                prevMenos2=""
                prevMas1=""
                prevMas2=""

                previsual='<p style="text-align:center; font-family:%s;"><strong>%s %i:%i</strong> %s | %s</p>' % (self.cbFuente.currentText(), self.cbLibro.currentText(), capitulo+1, versiculo+1, libro["capitulos"][capitulo][versiculo], self.cbBiblia.currentText())
                
                if verMenos1 in range(self.cbVersiculo.count()-1): prevMenos1='<p style="text-align:center; font-family:%s;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.cbLibro.currentText(), capitulo+1, verMenos1+1, libro["capitulos"][capitulo][verMenos1])

                if verMenos2 in range(self.cbVersiculo.count()-1): prevMenos2='<p style="text-align:center; font-family:%s;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.cbLibro.currentText(), capitulo+1, verMenos2+1, libro["capitulos"][capitulo][verMenos2])

                if verMas1 in range(self.cbVersiculo.count()-1): prevMas1='<p style="text-align:center; font-family:%s;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.cbLibro.currentText(), capitulo+1, verMas1+1, libro["capitulos"][capitulo][verMas1])

                if verMas2 in range(self.cbVersiculo.count()-1): prevMas2='<p style="text-align:center; font-family:%s;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.cbLibro.currentText(), capitulo+1, verMas2+1, libro["capitulos"][capitulo][verMas2])

                self.cargarTextos(previsual, prevMenos1, prevMenos2, prevMas1, prevMas2)

    def guardarTransparencia(self):
        modificarData("sbTransparenciaMax", self.sbTransparenciaMax.value())
        self.hsTransparencia.setValue(self.sbTransparenciaMax.value())
        self.datosMostrar()

    def mostrarTextEdits(self):
        if self.btnMostrar.text()=="Mostrar menos":
            self.animacionAltura.setDuration(1000)
            self.animacionAltura.setStartValue(100)
            self.animacionAltura.setEndValue(0)
            self.animacionAltura.start()
            self.btnMostrar.setText("Mostrar más")
        else:
            self.animacionAltura.setDuration(1000)
            self.animacionAltura.setStartValue(0)
            self.animacionAltura.setEndValue(100)
            self.animacionAltura.start()
            self.btnMostrar.setText("Mostrar menos")

    def cambiarAltura(self, value):
        altura=int(self.hsAltura.value())
        self.lblPrevMenos1.setMaximumSize(self.lblPrevMenos1.maximumWidth(), altura)
        self.tePrevMenos1.setMaximumSize(self.tePrevMenos1.maximumWidth(), altura)
        self.lblPrevMenos2.setMaximumSize(self.lblPrevMenos2.maximumWidth(), altura)
        self.tePrevMenos2.setMaximumSize(self.tePrevMenos2.maximumWidth(), altura)
        self.lblPrevMas1.setMaximumSize(self.lblPrevMas1.maximumWidth(), altura)
        self.tePrevMas1.setMaximumSize(self.tePrevMas1.maximumWidth(), altura)
        self.lblPrevMas2.setMaximumSize(self.lblPrevMas2.maximumWidth(), altura)
        self.tePrevMas2.setMaximumSize(self.tePrevMas2.maximumWidth(), altura)

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
        modificarData("cbFuente", self.cbFuente.currentText())
        if self.cbVersiculo.currentIndex()>0:
            self.leerVersiculo()

    def guardarFuenteTamano(self):
        modificarData("sbFuente", self.sbFuente.value())
        if self.cbVersiculo.currentIndex()>0:
            self.leerVersiculo()

    def guardarAlturax(self):
        modificarData("sbAlturax", self.sbAlturax.value())
        self.datosMostrar()

    def guardarAnchox(self):
        modificarData("sbAnchox", self.sbAnchox.value())
        self.datosMostrar()

    def guardarMargenx(self):
        modificarData("sbMargenx", self.sbMargenx.value())
        self.datosMostrar()

    def guardarFuentex(self):
        modificarData("cbFuentex", self.cbFuentex.currentText())
        if self.cbVersiculo.currentIndex()>0:
            self.leerVersiculo()

    def guardarFuenteTamanox(self):
        modificarData("sbFuentex", self.sbFuentex.value())
        if self.cbVersiculo.currentIndex()>0:
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
                if esnumero(division[1]):
                    buscarIndex(self.cbCapitulo, division[1])
                else:
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

    def enviarPrevisualizacion(self):
        if self.hsTransparencia.value()==0: return
        self.mostrarVersiculo=True
        self.limpiarVersiculo=False
        self.animacionTextoDesaparecer.setDuration(int(self.sbTiempo.value()*0.5))
        self.animacionTextoAparecer.setDuration(int(self.sbTiempo.value()*0.5))

        self.animacionTextoDesaparecer.setStartValue(self.hsTransparenciaTexto.value())
        self.animacionTextoDesaparecer.setEndValue(0)

        self.animacionTextoAparecer.setStartValue(0)
        self.animacionTextoAparecer.setEndValue(self.sbTransparenciaMax.value())

        self.anim_group.start()
        if self.cbVersiculo.currentIndex()>0:
            agregarHistorial(QDateASQL(self.deFecha), self.tePrev.toPlainText())
            self.cargarHistorial()

    def limpiarPrevisualizacion(self):
        if self.hsTransparencia.value()==0: return
        self.limpiarVersiculo=True
        if self.hsTransparenciaTexto.value()>0:
            self.animacionTextoDesaparecer.setDuration(int(self.sbTiempo.value()))
            self.animacionTextoDesaparecer.setStartValue(self.hsTransparenciaTexto.value())
            self.animacionTextoDesaparecer.setEndValue(0)
            self.animacionTextoDesaparecer.start()

    def escalarTransparenciaTexto(self, value):
        if value<self.sbTransparenciaMax.value():
            self.btnEnviar.setEnabled(False)
            self.btnLimpiar.setEnabled(False)
            self.btnOcultarMostrar.setEnabled(False)
            self.btnAnteriorC.setEnabled(False)
            self.btnSiguienteC.setEnabled(False)
            self.btnAnteriorV.setEnabled(False)
            self.btnSiguienteV.setEnabled(False)
        else:
            self.btnEnviar.setEnabled(True)
            self.btnLimpiar.setEnabled(True)
            self.btnOcultarMostrar.setEnabled(True)
            self.btnAnteriorC.setEnabled(True)
            self.btnSiguienteC.setEnabled(True)
            self.btnAnteriorV.setEnabled(True)
            self.btnSiguienteV.setEnabled(True)
        if value==0 and self.limpiarVersiculo:
            self.limpiarVersiculo=False
            self.mostrar.label.clear()
            self.mostrar_pantalla.label.clear()
            self.btnEnviar.setEnabled(True)
            self.btnLimpiar.setEnabled(True)
            self.btnOcultarMostrar.setEnabled(True)
            self.btnAnteriorC.setEnabled(True)
            self.btnSiguienteC.setEnabled(True)
            self.btnAnteriorV.setEnabled(True)
            self.btnSiguienteV.setEnabled(True)
        if value<=10 and self.mostrarVersiculo:
            self.mostrar.label.clear()
            self.mostrar.label.setText(self.tePrev.toHtml().replace('style="', 'style="font-size:%ipx; ' % self.sbFuente.value()))
            self.mostrar_pantalla.label.clear()
            versiculo_text = self.tePrev.toHtml().replace('style="', 'style="font-size:%ipx; ' % self.sbFuentex.value())
            if ' | ' in versiculo_text:
                self.mostrar_pantalla.label.setText('<br>' + versiculo_text)
            else:
                self.mostrar_pantalla.label.setText(versiculo_text)
            self.mostrarVersiculo=False
        colorFondo=self.data["colorFondo"]
        colorFuente=self.data["colorFuente"]
        colorFondox=self.data["colorFondox"]
        colorFuentex=self.data["colorFuentex"]
        self.mostrar.label.setStyleSheet("border-radius:15px; background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondo[0], colorFondo[1], colorFondo[2],  int(self.hsTransparencia.value()*255/100), colorFuente[0], colorFuente[1], colorFuente[2], int(value*255/100)))
        self.mostrar_pantalla.label.setStyleSheet("background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondox[0], colorFondox[1], colorFondox[2],  int(self.hsTransparencia.value()*255/100), colorFuentex[0], colorFuentex[1], colorFuentex[2], int(value*255/100)))

    def escalarTransparenciaTotal(self, value):
        if value<self.sbTransparenciaMax.value():
            self.btnEnviar.setEnabled(False)
            self.btnLimpiar.setEnabled(False)
            self.btnOcultarMostrar.setEnabled(False)
            self.btnAnteriorC.setEnabled(False)
            self.btnSiguienteC.setEnabled(False)
            self.btnAnteriorV.setEnabled(False)
            self.btnSiguienteV.setEnabled(False)
        if value==self.sbTransparenciaMax.value() or value==0:
            self.btnEnviar.setEnabled(True)
            self.btnLimpiar.setEnabled(True)
            self.btnOcultarMostrar.setEnabled(True)
            self.btnAnteriorC.setEnabled(True)
            self.btnSiguienteC.setEnabled(True)
            self.btnAnteriorV.setEnabled(True)
            self.btnSiguienteV.setEnabled(True)
            self.mostrar.label.clear()
            self.mostrar_pantalla.label.clear()

        colorFondo=self.data["colorFondo"]
        colorFuente=self.data["colorFuente"]
        colorFondox=self.data["colorFondox"]
        colorFuentex=self.data["colorFuentex"]
        if self.hsTransparenciaTexto.value()==0:
            self.mostrar.label.setStyleSheet("border-radius:15px; background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondo[0], colorFondo[1], colorFondo[2],  int(value*255/100), colorFuente[0], colorFuente[1], colorFuente[2], int(value*255/100)))
            self.mostrar_pantalla.label.setStyleSheet("background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondox[0], colorFondox[1], colorFondox[2],  int(value*255/100), colorFuentex[0], colorFuentex[1], colorFuentex[2], int(value*255/100)))
        else:
            self.mostrar.label.setStyleSheet("border-radius:15px; background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondo[0], colorFondo[1], colorFondo[2],  int(value*255/100), colorFuente[0], colorFuente[1], colorFuente[2], 0))
            self.mostrar_pantalla.label.setStyleSheet("background-color: rgba(%i, %i, %i, %i); color: rgba(%i, %i, %i, %i)" % (colorFondox[0], colorFondox[1], colorFondox[2],  int(value*255/100), colorFuentex[0], colorFuentex[1], colorFuentex[2], 0))

        modificarData("colorFuente", [colorFuente[0], colorFuente[1], colorFuente[2], int(value*255/100)])
        modificarData("colorFondo", [colorFondo[0], colorFondo[1], colorFondo[2], int(value*255/100)])
        modificarData("colorFuentex", [colorFuentex[0], colorFuentex[1], colorFuentex[2], int(value*255/100)])
        modificarData("colorFondox", [colorFondox[0], colorFondox[1], colorFondox[2], int(value*255/100)])
        if value==0:
            self.btnOcultarMostrar.setText("Mostrar")
        else:
            self.btnOcultarMostrar.setText("Ocultar")

    def ocultarMostrar(self):
        if self.btnOcultarMostrar.text()=="Ocultar":
            self.animacion.setDuration(int(self.sbTiempo.value()))
            self.animacion.setStartValue(self.hsTransparencia.value())
            self.animacion.setEndValue(0)
            self.animacion.start()
            self.btnOcultarMostrar.setText("Mostrar")
        else:
            self.animacion.setDuration(int(self.sbTiempo.value()))
            self.animacion.setStartValue(self.hsTransparencia.value())
            self.animacion.setEndValue(self.sbTransparenciaMax.value())
            self.animacion.start()
            self.btnOcultarMostrar.setText("Ocultar")

    def siguienteVersiculo(self):
        if self.cbLibro.currentText() in self.tePrevMas1.toHtml():
            self.cbVersiculo.setCurrentIndex(self.cbVersiculo.currentIndex()+1)
            self.enviarPrevisualizacion()

    def anteriorVersiculo(self):
        if self.cbLibro.currentText() in self.tePrevMenos1.toHtml():
            self.cbVersiculo.setCurrentIndex(self.cbVersiculo.currentIndex()-1)
            self.enviarPrevisualizacion()

    def agregarBotonEliminar(self, tw, columna):
        for i in range(tw.topLevelItemCount()):
            item=tw.topLevelItem(i)
            buttonEliminar = QPushButton("Eliminar", tw)
            buttonEliminar.clicked.connect(lambda checked=False, identificador=item.text(5): self.quitarCancion(identificador))
            tw.setItemWidget(item, columna, buttonEliminar)

    def agregarBotonActualizar(self, tw, columna):
        for i in range(tw.topLevelItemCount()):
            item=tw.topLevelItem(i)
            buttonActualizar = QPushButton("Actualizar", tw)
            buttonActualizar.clicked.connect(lambda checked=False, identificador=item: self.actualizarCancion(identificador))
            tw.setItemWidget(item, columna, buttonActualizar)

    def cargarCancionesHoy(self):
        self.canciones=leerCanciones()
        self.twCancionesHoy.clear()
        self.twLetras.clear()
        self.leCancionSeleccionada.clear()
        lista=self.canciones["Canciones Hoy"]
        for urlCancion in lista:
            dato=self.canciones[urlCancion]
            cancion=dato[2]
            artista=dato[0]
            album=dato[1]
            fila=[cancion, artista, album, "", "", urlCancion]
            insertarFila(self.twCancionesHoy, fila)
        self.agregarBotonActualizar(self.twCancionesHoy, 3)
        self.agregarBotonEliminar(self.twCancionesHoy, 4)

    def cargarCanciones(self):
        self.canciones=leerCanciones()
        self.twCancionesRegistradas.clear()
        self.twCancionesRegistradas.sortItems(0, Qt.AscendingOrder)
        for url,v in self.canciones.items():
            if url!="Canciones Hoy":
                cancion=v[2]
                artista=v[0]
                album=v[1]
                fila=[cancion, artista, album, url]
                insertarFila(self.twCancionesRegistradas, fila)

    def cargarAPI(self, item):
        urlAPI = 'https://www.palabrayespiritu.org/musica/cancionero/api/'
        self.leCancionSeleccionada.setText('API')
        self.twLetras.clear()
        letras=requests.get(urlAPI).json()['letras']
        for parrafo in letras:
            if not parrafo[0] == "(":
                insertarFila(self.twLetras, [parrafo])
        api_mostrar("\n\n".join(letras))

    def buscarCancion(self):
        url=self.leUrlCancion.text()
        if buscarLetra(url):
            self.leUrlCancion.clear()
            self.cargarCanciones()

    def cargarTodas(self):
        abrirPrograma("actualizar_canciones.py")

    def buscarCancionRegistrada(self):
        buscarTabla(self.twCancionesRegistradas, self.leBuscar.text(), [0])

    def agregarCancion(self):
        self.canciones=leerCanciones()
        lista=self.canciones["Canciones Hoy"]
        lista.append(self.twCancionesRegistradas.currentItem().text(3))
        modificarCanciones("Canciones Hoy", lista)
        self.cargarCancionesHoy()

    def quitarCancion(self, url):
        self.canciones=leerCanciones()
        lista=self.canciones["Canciones Hoy"]
        for i in range(len(lista)):
            if lista[i]==url:
                indice=i
        lista.pop(indice)
        modificarCanciones("Canciones Hoy", lista)
        self.cargarCancionesHoy()

    def elegirCancion(self, item):
        self.leCancionSeleccionada.setText(item.text(0))
        self.canciones=leerCanciones()
        letras=self.canciones[item.text(5)][3]
        self.twLetras.clear()
        parrafo=[]
        for letra in letras.splitlines():
            if letra=="":
                insertarFila(self.twLetras, ["\n".join(parrafo)])
                parrafo=[]
            else:
                if letra[0]!="#":
                    parrafo.append(letra)
        insertarFila(self.twLetras, ["\n".join(parrafo)])
        api_mostrar(letras)

    def actualizarCancion(self, item):
        #print(url)
        #print(buscarLetra(url))
        cancion = item.text(0)
        artista = item.text(1)
        album = item.text(2)
        url = item.text(5)
        letras_texto = self.canciones[item.text(5)][3]
        self.ventana = LetrasEditar(url, cancion, artista, album, letras_texto)
        self.ventana.show()

    def elegirLetra(self, item):
        previsual=""
        prevMenos1=""
        prevMenos2=""
        prevMas1=""
        prevMas2=""

        if item!=None:
            previsual='<p style="text-align:center; font-family:%s;">%s</p>' % (self.cbFuente.currentText(), item.text(0).replace("\n",'<br>'))

        if buscarItem(self.twLetras)>0:
            prevMenos1='<p style="text-align:center; font-family:%s;">%s</p>' % (self.cbFuente.currentText(), self.twLetras.topLevelItem(buscarItem(self.twLetras)-1).text(0).replace("\n",'<br>'))
        if buscarItem(self.twLetras)>1:
            prevMenos2='<p style="text-align:center; font-family:%s;">%s</p>' % (self.cbFuente.currentText(), self.twLetras.topLevelItem(buscarItem(self.twLetras)-2).text(0).replace("\n",'<br>'))
        if buscarItem(self.twLetras)<self.twLetras.topLevelItemCount()-2:
            prevMas1='<p style="text-align:center; font-family:%s;">%s</p>' % (self.cbFuente.currentText(), self.twLetras.topLevelItem(buscarItem(self.twLetras)+1).text(0).replace("\n",'<br>'))
        if buscarItem(self.twLetras)<self.twLetras.topLevelItemCount()-3:
            prevMas2='<p style="text-align:center; font-family:%s;">%s</p>' % (self.cbFuente.currentText(), self.twLetras.topLevelItem(buscarItem(self.twLetras)+2).text(0).replace("\n",'<br>'))
        self.cbLibro.setCurrentIndex(0)
        self.cargarTextos(previsual, prevMenos1, prevMenos2, prevMas1, prevMas2)
        self.enviarPrevisualizacion()

    def guardarCondicionesV(self):
        modificarData("sbAlturaV", self.sbAltura.value())
        modificarData("sbAnchoV", self.sbAncho.value())
        modificarData("sbMargenV", self.sbMargen.value())
        modificarData("sbFuenteV", self.sbFuente.value())
        modificarData("cbFuenteV", self.cbFuente.currentText())

    def cargarCondicionesV(self):
        self.data=leerData()
        modificarData("sbAltura", self.data["sbAlturaV"])
        modificarData("sbAncho", self.data["sbAnchoV"])
        modificarData("sbMargen", self.data["sbMargenV"])
        modificarData("sbFuente", self.data["sbFuenteV"])
        modificarData("cbFuente", self.data["cbFuenteV"])
        self.cargarDatos()

    def guardarCondicionesC(self):
        modificarData("sbAlturaC", self.sbAltura.value())
        modificarData("sbAnchoC", self.sbAncho.value())
        modificarData("sbMargenC", self.sbMargen.value())
        modificarData("sbFuenteC", self.sbFuente.value())
        modificarData("cbFuenteC", self.cbFuente.currentText())

    def cargarCondicionesC(self):
        self.data=leerData()
        modificarData("sbAltura", self.data["sbAlturaC"])
        modificarData("sbAncho", self.data["sbAnchoC"])
        modificarData("sbMargen", self.data["sbMargenC"])
        modificarData("sbFuente", self.data["sbFuenteC"])
        modificarData("cbFuente", self.data["cbFuenteC"])
        self.cargarDatos()

    def siguienteParrafo(self):
        if self.twLetras.currentItem()==None:
            indice=-1
        else:
            indice=buscarItem(self.twLetras)
        self.twLetras.setCurrentItem(self.twLetras.topLevelItem(indice+1))
        self.elegirLetra(self.twLetras.currentItem())

    def anteriorParrafo(self):
        if self.twLetras.currentItem()==None:
            indice=self.twLetras.topLevelItemCount()
        else:
            indice=buscarItem(self.twLetras)
        self.twLetras.setCurrentItem(self.twLetras.topLevelItem(indice-1))
        self.elegirLetra(self.twLetras.currentItem())

    def buscarConcordancia(self):
        texto=self.leConcordancia.text()
        palabras=re.sub(' +', ' ', quitarTildes(texto)).split(" ")
        patrones=[]
        self.twConcordancia.clear()
        if texto!="":
            for palabra in palabras:
                patrones.append(re.compile(palabra.upper()))

            for version in self.biblia:
                contadorCapitulo=0
                libro=version["nombre"]
                capitulos=version["capitulos"]
                for capitulo in capitulos:
                    contadorCapitulo+=1
                    contadorVersiculo=0
                    for versiculo in capitulo:
                        contadorVersiculo+=1

                        busqueda=True
                        for patron in patrones:
                            if not patron.search(quitarTildes(versiculo.upper())):
                                busqueda=False

                        if busqueda:
                            fila=["%s %i:%i" % (libro, contadorCapitulo, contadorVersiculo), versiculo]
                            insertarFila(self.twConcordancia, fila)

    def usarVersiculo(self, item):
        self.lePasaje.setText(item.text(0))

app=QApplication(sys.argv) #Instancia para iniciar una aplicación
_main=Principal() #Crear un objeto de la clase / Como el Load en VBA
_main.show() #Mostrar la ventana
app.exec_() #Ejecutar applicación
