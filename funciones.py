import requests, sys, os, json, subprocess, re, git
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
tildes={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U'}
urlBase="https://api.scripture.api.bible"
token='d1eded304a6a68a4befc685b42447bcf'

def abrirPrograma(programa):
    if sys.platform == "win32":
        subprocess.Popen("python %s" % (programa))
    else:
        subprocess.call(['gnome-terminal', '--', 'python3' , programa])

def buscarTabla(tw, texto, columnas):
    try:
        rango = range(tw.topLevelItemCount())
        palabras=re.sub(' +', ' ', texto).split(" ")
        patrones=[]
        for palabra in palabras:
            patrones.append(re.compile(palabra.upper()))
        if texto=="":
            for i in rango:
                tw.topLevelItem(i).setHidden(False)
        else:
            for i in rango:
                busqueda=True
                for j in columnas:
                    subBusqueda=False
                    for patron in patrones:
                        subBusqueda=subBusqueda or (patron.search(tw.topLevelItem(i).text(j).upper()) is None)
                    busqueda=busqueda and subBusqueda
                if busqueda:
                    tw.topLevelItem(i).setHidden(True)
                else:
                    tw.topLevelItem(i).setHidden(False)
    except Exception as e:
        print(e)

def buscarLetra(url):
    if url=="": return False
    try:
        r=requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        letras = soup.find("pre", {'id':'letras'}).text
        nombre = soup.findAll("h3")[1].text
        datos = soup.find("span", {'class':'post-meta'}).findAll("a")
        artista = datos[0].text
        album = datos[1].text
        modificarCanciones(url, [artista, album, nombre, letras])
        return True
    except Exception as e:
        print(e)
        return False

def insertarFila(tw, Fila):
    tw.setIndentation(0)
    item=QTreeWidgetItem(tw, Fila)
    tw.addTopLevelItem(item)

    for i in range(tw.columnCount()):
        tw.resizeColumnToContents(i)

    # if tw.columnCount()>1:
    #     tw.setColumnWidth(tw.columnCount()-1, 0)

def QDateASQL(QFecha):
    return "%s-%s-%s" % (str(QFecha.date().year()), "0"*(2-len(str(QFecha.date().month()))) + str(QFecha.date().month()), "0"*(2-len(str(QFecha.date().day()))) + str(QFecha.date().day()))

def leerCanciones():
    try:
        with open('../canciones.json') as file:
            return json.load(file)
    except Exception as e:
        with open('../canciones.json', 'w') as file:
            json.dump({"Canciones Hoy":[]}, file, indent=4)
            return {"Canciones Hoy":[]}

def subirCanciones(data):
    with open('../canciones.json', 'w') as file:
        json.dump(data, file, indent=4)

def modificarCanciones(key, value):
    data=leerCanciones()
    data[key]=value
    subirCanciones(data)

def leerData():
    try:
        with open('../data.json') as file:
            return json.load(file)
    except Exception as e:
        with open('../data.json', 'w') as file:
            json.dump({}, file, indent=4)
            return {}

def subirData(data):
    with open('../data.json', 'w') as file:
        json.dump(data, file, indent=4)

def modificarData(key, value):
    data=leerData()
    data[key]=value
    subirData(data)

def leerHistorial():
    try:
        with open('../historial.json') as file:
            return json.load(file)
    except Exception as e:
        with open('../historial.json', 'w') as file:
            json.dump({str(date.today()):[]}, file, indent=4)
            return {str(date.today()):[]}

def subirHistorial(data):
    with open('../historial.json', 'w') as file:
        json.dump(data, file, indent=4)

def agregarHistorial(key, value):
    data=leerHistorial()
    if not key in data: data[key]=[]
    if not value in data[key]:
        data[key].append(value)
        subirHistorial(data)

def esnumero(texto):
    try:
        numero=int(texto)
        if str(numero)==texto:
            return True

        return False
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
