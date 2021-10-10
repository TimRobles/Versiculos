from funciones import *

version='RVR60'

with open('Versiones/%s.json' % version, 'rw') as file:
    biblia=json.load(file)
    for libro in biblia:
        for capitulos in libro['capitulos']:
            for versiculo in capitulos:
                versiculo = quitarAnotaciones(versiculo)
    json.dump(biblia, file, indent=4)
