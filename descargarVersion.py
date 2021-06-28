from funciones import *
libros=["Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Josué", "Jueces", "Rut", "1 Samuel", "2 Samuel", "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras", "Nehemías", "Ester", "Job", "Salmos", "Proverbios", "Eclesiastés", "Cantares", "Isaías", "Jeremías", "Lamentaciones", "Ezequiel", "Daniel", "Oseas", "Joel", "Amós", "Abdías", "Jonás", "Miqueas", "Nahúm", "Habacuc", "Sofonías", "Hageo", "Zacarías", "Malaquías", "Mateo", "Marcos", "Lucas", "Juan", "Hechos", "Romanos", "1 Corintios", "2 Corintios", "Gálatas", "Efesios", "Filipenses", "Colosenses", "1 Tesalonicenses", "2 Tesalonicenses", "1 Timoteo", "2 Timoteo", "Tito", "Filemón", "Hebreos", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Apocalipsis"]

versiones=["TLA", "DHH", "NTV", "PDT"]
urlBase="https://www.biblegateway.com/passage/?search="

for version in versiones:
    biblia=[]
    for libro in libros:
        diccionario={}
        diccionario["nombre"]=libro
        diccionario["capitulos"]=[]
        capitulo=0
        busqueda=True
        while busqueda!=None:
            capitulo+=1
            textoCapitulo=[]
            url=urlBase + libro.replace(" ", "+") + "+" + str(capitulo) + "&version=" + version
            r=requests.get(url)
            print(url)
            soup=BeautifulSoup(r.text, 'lxml')
            busqueda= soup.find("div", {'class': 'result-text-style-normal'})
            # busqueda= soup.findAll("p", {'class': 'line'})
            if busqueda==None:
                continue

            versiculo=[]
            inicio=True
            for dato in busqueda.findAll("span"):
                if dato.attrs["class"][0]=="text" and dato.parent.name!="h3":
                    texto=dato.text
                    separar=texto.split("\xa0")
                    if len(separar)==1:
                        versiculo.append(texto)
                    else:
                        if inicio:
                            inicio=False
                            versiculo.append(separar[1])
                        else:
                            textoCapitulo.append(" ".join(versiculo))
                            versiculo=[]
                            versiculo.append(separar[1])

            textoCapitulo.append(" ".join(versiculo))
            diccionario["capitulos"].append(textoCapitulo)

        diccionario["capitulos"].append([])
        biblia.append(diccionario)

    with open('Versiones/%s.json' % version, 'w') as file:
        json.dump(biblia, file, indent=4)

    versionesRegistradas=leerData()["cbBiblia"]
    versionesRegistradas[version]='%s.json' % version
    modificarData("cbBiblia", versionesRegistradas)


            # ['__bool__', '__call__', '__class__', '__contains__', '__copy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_all_strings', '_find_all', '_find_one', '_is_xml', '_lastRecursiveChild', '_last_descendant', '_should_pretty_print', 'append', 'attrs', 'can_be_empty_element', 'cdata_list_attributes', 'childGenerator', 'children', 'clear', 'contents', 'decode', 'decode_contents', 'decompose', 'decomposed', 'descendants', 'encode', 'encode_contents', 'extend', 'extract', 'fetchNextSiblings', 'fetchParents', 'fetchPrevious', 'fetchPreviousSiblings', 'find', 'findAll', 'findAllNext', 'findAllPrevious', 'findChild', 'findChildren', 'findNext', 'findNextSibling', 'findNextSiblings', 'findParent', 'findParents', 'findPrevious', 'findPreviousSibling', 'findPreviousSiblings', 'find_all', 'find_all_next', 'find_all_previous', 'find_next', 'find_next_sibling', 'find_next_siblings', 'find_parent', 'find_parents', 'find_previous', 'find_previous_sibling', 'find_previous_siblings', 'format_string', 'formatter_for_name', 'get', 'getText', 'get_attribute_list', 'get_text', 'has_attr', 'has_key', 'hidden', 'index', 'insert', 'insert_after', 'insert_before', 'isSelfClosing', 'is_empty_element', 'known_xml', 'name', 'namespace', 'next', 'nextGenerator', 'nextSibling', 'nextSiblingGenerator', 'next_element', 'next_elements', 'next_sibling', 'next_siblings', 'parent', 'parentGenerator', 'parents', 'parserClass', 'parser_class', 'prefix', 'preserve_whitespace_tags', 'prettify', 'previous', 'previousGenerator', 'previousSibling', 'previousSiblingGenerator', 'previous_element', 'previous_elements', 'previous_sibling', 'previous_siblings', 'recursiveChildGenerator', 'renderContents', 'replaceWith', 'replaceWithChildren', 'replace_with', 'replace_with_children', 'select', 'select_one', 'setup', 'smooth', 'string', 'strings', 'stripped_strings', 'text', 'unwrap', 'wrap']
