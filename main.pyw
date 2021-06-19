from funciones import *

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
        self.cargarFuentes()
        self.cargarHistorial()
        self.cargarDatos()
        self.cargarLibros()

        self.mostrar=Mostrar()
        self.mostrar.show()
        self.datosMostrar()
        self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgba(%s); color: rgba(%s)" % (",".join(self.data["colorFondo"][0:-1] + [str(int(self.data["sbTransparenciaMax"]*255/100))]), ",".join(self.data["colorFuente"][0:-1] + ["0"])))

        self.animacion=QPropertyAnimation(self.hsTransparencia, b'value')
        self.animacionTextoDesaparecer=QPropertyAnimation(self.hsTransparenciaTexto, b'value')
        self.animacionTextoAparecer=QPropertyAnimation(self.hsTransparenciaTexto, b'value')
        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.animacionTextoDesaparecer)
        self.anim_group.addAnimation(self.animacionTextoAparecer)

        self.hsTransparencia.valueChanged.connect(self.escalarTransparenciaTotal)
        self.hsTransparenciaTexto.valueChanged.connect(self.escalarTransparenciaTexto)
        self.sbTransparenciaMax.valueChanged.connect(self.guardarTransparencia)

        self.btnColorFuente.clicked.connect(self.seleccionarColorFuente)
        self.btnColorFondo.clicked.connect(self.seleccionarColorFondo)

        self.btnUpdate.clicked.connect(self.actualizarSistema)

        self.lePasaje.textChanged.connect(self.separar)

        self.sbAltura.valueChanged.connect(self.guardarAltura)
        self.sbAncho.valueChanged.connect(self.guardarAncho)
        self.sbMargen.valueChanged.connect(self.guardarMargen)
        self.cbFuente.currentIndexChanged.connect(self.guardarFuente)
        self.sbFuente.valueChanged.connect(self.guardarFuenteTamano)

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
        self.leBuscar.textChanged.connect(self.buscarCancionRegistrada)
        self.twCancionesRegistradas.itemDoubleClicked.connect(self.agregarCancion)
        self.twCancionesHoy.itemDoubleClicked.connect(self.elegirCancion)
        self.twLetras.itemDoubleClicked.connect(self.elegirLetra)
        self.btnSiguienteC.clicked.connect(self.siguienteParrafo)
        self.btnAnteriorC.clicked.connect(self.anteriorParrafo)

    def cargarFuentes(self):
        for fuente in QFontDatabase().families(QFontDatabase.Latin):
            self.cbFuente.addItem(fuente)

    def datosMostrar(self):
        self.data=leerData()
        self.mostrar.textEdit.setMaximumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.textEdit.setMinimumSize(self.data["sbAncho"], self.data["sbAltura"])
        self.mostrar.widget.setMaximumSize(self.data["sbAncho"], self.data["sbMargen"])
        self.mostrar.widget.setMinimumSize(self.data["sbAncho"], self.data["sbMargen"])

    def seleccionarColorFuente(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFuente"]
            colorInicial.setRgb(int(dato[0]), int(dato[1]), int(dato[2]), int(dato[3]))
            color = QColorDialog.getColor(colorInicial, self, "Color de Fuente")
            modificarData("colorFuente", [str(color.red()), str(color.green()), str(color.blue()), str(int(self.hsTransparencia.value()*255/100))])
            self.datosMostrar()
        except Exception as e:
            print(e)

    def seleccionarColorFondo(self):
        try:
            colorInicial=QColor()
            dato=self.data["colorFondo"]
            colorInicial.setRgb(int(dato[0]), int(dato[1]), int(dato[2]), int(dato[3]))
            color = QColorDialog.getColor(colorInicial, self, "Color de Fondo")
            modificarData("colorFondo", [str(color.red()), str(color.green()), str(color.blue()), str(int(self.hsTransparencia.value()*255/100))])
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
        except Exception as e:
            print("Error", msg + "\n" + e)

    def cargarVersion(self):
        self.data=leerData()
        if self.cbBiblia.currentText()=="": return
        version=self.data["cbBiblia"][self.cbBiblia.currentText()]
        with open(version) as file:
            self.biblia=json.load(file)

    def cargarDatos(self):
        self.data=leerData()
        if not "colorFuente" in self.data:
            modificarData("colorFuente", ["0", "0", "0", "255"])
        if not "colorFondo" in self.data:
            modificarData("colorFondo", ["138", "226", "52", "255"])
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
            print("buscar cbFuente", self.data["cbFuente"])
            buscarIndex(self.cbFuente, self.data["cbFuente"])
        else:
            self.cbFuente.setCurrentIndex(-1)
            modificarData("cbFuente", "")
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

                previsual='<p style="text-align:center; font-family:%s; font-size:%ipx;"><strong>%s %i:%i</strong> %s | %s</p>' % (self.cbFuente.currentText(), self.sbFuente.value(), self.cbLibro.currentText(), capitulo+1, versiculo+1, libro["capitulos"][capitulo][versiculo], self.cbBiblia.currentText())

                if verMenos1 in range(self.cbVersiculo.count()-1): prevMenos1='<p style="text-align:center; font-family:%s; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMenos1+1, libro["capitulos"][capitulo][verMenos1])

                if verMenos2 in range(self.cbVersiculo.count()-1): prevMenos2='<p style="text-align:center; font-family:%s; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMenos2+1, libro["capitulos"][capitulo][verMenos2])

                if verMas1 in range(self.cbVersiculo.count()-1): prevMas1='<p style="text-align:center; font-family:%s; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMas1+1, libro["capitulos"][capitulo][verMas1])

                if verMas2 in range(self.cbVersiculo.count()-1): prevMas2='<p style="text-align:center; font-family:%s; font-size:%ipx;"><strong>%s %i:%i</strong> %s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.cbLibro.currentText(), capitulo+1, verMas2+1, libro["capitulos"][capitulo][verMas2])

                self.cargarTextos(previsual, prevMenos1, prevMenos2, prevMas1, prevMas2)

    def guardarTransparencia(self):
        modificarData("sbTransparenciaMax", self.sbTransparenciaMax.value())
        self.datosMostrar()

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
        self.animacionTextoDesaparecer.setDuration(10*(self.hsTransparenciaTexto.value()))
        self.animacionTextoAparecer.setDuration(10*(self.sbTransparenciaMax.value()))

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
        self.mostrarVersiculo=True
        if self.hsTransparenciaTexto.value()>0:
            self.animacionTextoDesaparecer.setDuration(10*self.hsTransparenciaTexto.value())
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
        if value==self.sbTransparenciaMax.value() or value==0:
            self.btnEnviar.setEnabled(True)
            self.btnLimpiar.setEnabled(True)
            self.btnOcultarMostrar.setEnabled(True)
            self.btnAnteriorC.setEnabled(True)
            self.btnSiguienteC.setEnabled(True)
            self.btnAnteriorV.setEnabled(True)
            self.btnSiguienteV.setEnabled(True)
        if value in [0,1]:
            self.mostrar.textEdit.clear()
            if self.mostrarVersiculo:
                self.mostrar.textEdit.insertHtml(self.tePrev.toHtml())
        self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgba(%s); color: rgba(%s)" % (",".join(self.data["colorFondo"][0:-1] + [str(int(self.hsTransparencia.value()*255/100))]), ",".join(self.data["colorFuente"][0:-1] + [str(int(value*255/100))])))

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

        if self.hsTransparenciaTexto.value()==0:
            self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgba(%s); color: rgba(%s)" % (",".join(self.data["colorFondo"][0:-1] + [str(int(value*255/100))]), ",".join(self.data["colorFuente"][0:-1] + ["0"])))
        else:
            self.mostrar.textEdit.setStyleSheet("border-radius:15px; background-color: rgba(%s); color: rgba(%s)" % (",".join(self.data["colorFondo"][0:-1] + [str(int(value*255/100))]), ",".join(self.data["colorFuente"][0:-1] + [str(int(value*255/100))])))
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
            self.animacion.setDuration(10*(self.sbTransparenciaMax.value()-self.hsTransparencia.value()))
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
            buttonActualizar.clicked.connect(lambda checked=False, identificador=item.text(5): self.actualizarCancion(identificador))
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
                parrafo.append(letra)

    def actualizarCancion(self, url):
        print(url)
        print(buscarLetra(url))

    def elegirLetra(self, item):
        indice=-1
        for i in range(self.twLetras.topLevelItemCount()):
            if item==self.twLetras.topLevelItem(i): indice=i
        if indice==-1:
            self.lblItemIndex.setText(str(indice))
            return

        self.lblItemIndex.setText(str(indice))
        previsual=""
        prevMenos1=""
        prevMenos2=""
        prevMas1=""
        prevMas2=""

        previsual='<p style="text-align:center; font-family:%s; font-size:%ipx;">%s</p>' % (self.cbFuente.currentText(), self.sbFuente.value(), item.text(0).replace("\n",'<br>'))

        if indice>0:
            prevMenos1='<p style="text-align:center; font-family:%s; font-size:%ipx;">%s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.twLetras.topLevelItem(indice-1).text(0).replace("\n",'<br>'))
        if indice>1:
            prevMenos2='<p style="text-align:center; font-family:%s; font-size:%ipx;">%s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.twLetras.topLevelItem(indice-2).text(0).replace("\n",'<br>'))
        if indice<self.twLetras.topLevelItemCount()-2:
            prevMas1='<p style="text-align:center; font-family:%s; font-size:%ipx;">%s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.twLetras.topLevelItem(indice+1).text(0).replace("\n",'<br>'))
        if indice<self.twLetras.topLevelItemCount()-3:
            prevMas2='<p style="text-align:center; font-family:%s; font-size:%ipx;">%s</p>' % (self.cbFuente.currentText(), self.sbFuente.value()/2, self.twLetras.topLevelItem(indice+2).text(0).replace("\n",'<br>'))
        self.cbLibro.setCurrentIndex(0)
        self.cargarTextos(previsual, prevMenos1, prevMenos2, prevMas1, prevMas2)

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
        if self.lblItemIndex.text()=="-1": return
        if int(self.lblItemIndex.text())<self.twLetras.topLevelItemCount()-2:
            self.elegirLetra(self.twLetras.topLevelItem(int(self.lblItemIndex.text())+1))
            self.enviarPrevisualizacion()

    def anteriorParrafo(self):
        if self.lblItemIndex.text()=="-1": return
        if int(self.lblItemIndex.text())>0:
            self.elegirLetra(self.twLetras.topLevelItem(int(self.lblItemIndex.text())-1))
            self.enviarPrevisualizacion()

app=QApplication(sys.argv) #Instancia para iniciar una aplicación
_main=Principal() #Crear un objeto de la clase / Como el Load en VBA
_main.show() #Mostrar la ventana
app.exec_() #Ejecutar applicación
