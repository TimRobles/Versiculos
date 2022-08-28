from funciones import *
import pandas as pd

tildes={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U'}

def quitarTildes(texto):
    textoSinTildes=texto
    for k,v in tildes.items():
        textoSinTildes=textoSinTildes.replace(k,v)
        textoSinTildes=textoSinTildes.replace(k.lower(),v.lower())
    return textoSinTildes

def slugify(texto):
    texto = quitarTildes(texto)
    return texto.replace(" ", "-")

def buscar_cancion(url):
    if url=="": return False
    try:
        r=requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        letras = soup.find("pre", {'id':'letras'}).text
        acordes = soup.find("pre", {'id':'acordes'}).text
        tempo = soup.find("input", {'id':'tempo'}).value
        youtube = soup.find("div", {'id':'video'})
        print(youtube)
        nombre = soup.findAll("h3")[1].text
        datos = soup.find("span", {'class':'post-meta'}).findAll("a")
        artista = datos[0].text
        album = datos[1].text
        data = [artista, album, nombre, letras, acordes, tempo]
        print(url, data)
        return data
    except Exception as e:
        print(e)
        return False

lista_canciones = {}
lista_albumes = {}
lista_artistas = {}

dfCanciones = pd.DataFrame(columns=[
                        'pista',
                        'nombre',
                        'tempo',
                        'youtube',
                        'letras',
                        'acordes',
                        'slug',
                        'album_id',
                        ])
dfAlbum = pd.DataFrame(columns=[
                        'nombre',
                        'slug',
                        'artista_id',
                        ])
dfArtista = pd.DataFrame(columns=[
                        'nombre',
                        'slug',
                        ])

fp = open('link_canciones.txt', 'r')

for url in fp:
    print(url)
    [artista, album, nombre, letras, acordes, tempo] = buscar_cancion(url)
    if not artista in lista_artistas:
        lista_artistas[artista] = len(lista_artistas) + 1
        filaArtista = {}
        filaArtista['nombre'] = artista
        filaArtista['slug'] = slugify(artista)
        dfArtista = dfArtista.append(filaArtista, ignore_index=True)

    if not album in lista_albumes:
        lista_albumes[album] = len(lista_albumes) + 1
        filaAlbum = {}
        filaAlbum['nombre'] = album
        filaAlbum['slug'] = slugify(album)
        filaAlbum['artista_id'] = lista_artistas[artista]
        dfAlbum = dfAlbum.append(filaAlbum, ignore_index=True)

    filaCancion = {}
    filaCancion['pista'] = 0
    filaCancion['nombre'] = nombre
    filaCancion['tempo'] = tempo
    filaCancion['youtube'] = ""
    filaCancion['letras'] = letras
    filaCancion['acordes'] = acordes
    filaCancion['slug'] = slugify(nombre)
    filaCancion['album_id'] = lista_albumes[album]
    dfCanciones = dfCanciones.append(filaCancion, ignore_index=True)

dfCanciones['created_by_id'] = 1
dfCanciones['updated_by_id'] = 1

dfAlbum['created_by_id'] = 1
dfAlbum['updated_by_id'] = 1

dfArtista['created_by_id'] = 1
dfArtista['updated_by_id'] = 1

dfCanciones.to_csv('canciones.csv', sep=';', index=False)
dfAlbum.to_csv('albumes.csv', sep=';', index=False)
dfArtista.to_csv('artistas.csv', sep=';', index=False)

# DELETE FROM musica_ordencanciones;
# DELETE FROM musica_cancion;
# DELETE FROM musica_album;
# DELETE FROM musica_artista;
#
# ALTER SEQUENCE musica_ordencanciones_id_seq RESTART WITH 1;
# ALTER SEQUENCE musica_cancion_id_seq RESTART WITH 1;
# ALTER SEQUENCE musica_album_id_seq RESTART WITH 1;
# ALTER SEQUENCE musica_artista_id_seq RESTART WITH 1;
#
\COPY musica_artista(nombre, slug, created_by_id, updated_by_id, foto, created_at, updated_at) FROM /home/tim/github/Versiculos/artistas.csv DELIMITER ';' CSV HEADER;
select setval( pg_get_serial_sequence('musica_artista', 'id'),(select max(id) from musica_artista));

\COPY musica_album(nombre, slug, artista_id, created_by_id, updated_by_id) FROM /home/tim/github/Versiculos/albumes.csv DELIMITER ';' CSV HEADER;
select setval( pg_get_serial_sequence('musica_album', 'id'),(select max(id) from musica_album));

\COPY musica_cancion(pista, nombre, tempo, youtube, letras, acordes, slug, album_id, created_by_id, updated_by_id) FROM /home/tim/github/Versiculos/canciones.csv DELIMITER ';' CSV HEADER;
select setval( pg_get_serial_sequence('musica_cancion', 'id'),(select max(id) from musica_cancion));
