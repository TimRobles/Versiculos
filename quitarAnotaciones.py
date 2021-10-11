from funciones import *

version='RVR60'

nuevaBiblia=[]
with open('Versiones/%s.json' % version) as file:
    biblia=json.load(file)


for libro in biblia:
    nuevoLibro = {
        "nombre": libro['nombre'],
        "capitulos": [],
    }
    for capitulos in libro['capitulos']:
        nuevoCapitulo = []
        for versiculo in capitulos:
            nuevoCapitulo.append(quitarAnotaciones(versiculo))
        nuevoLibro['capitulos'].append(nuevoCapitulo)

    nuevaBiblia.append(nuevoLibro)

with open('Versiones/%s.json' % version, 'w') as file:
    json.dump(nuevaBiblia, file, indent=4)
