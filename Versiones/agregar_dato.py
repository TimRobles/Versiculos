import pandas as pd
import datetime

fecha = datetime.datetime.strptime('2000-01-01 05:00:00.000000+0000', '%Y-%m-%d %H:%M:%S.%f%z')

# ruta = '/home/tim/github/Versiculos/artistas.csv'
# dfArtista = pd.read_csv(ruta, sep=';', dtype=str)
# dfArtista['foto'] = 'img/musica/artista/sin-imagen.jpeg'
# dfArtista['created_at'] = fecha
# dfArtista['updated_at'] = fecha
# dfArtista.to_csv(ruta, sep=';', index=False)

# ruta = '/home/tim/github/Versiculos/albumes.csv'
# dfAlbum = pd.read_csv(ruta, sep=';', dtype=str)
# dfAlbum['foto'] = 'img/musica/album/sin-imagen.jpeg'
# dfAlbum['created_at'] = fecha
# dfAlbum['updated_at'] = fecha
# dfAlbum.to_csv(ruta, sep=';', index=False)

ruta = '/home/tim/github/Versiculos/canciones.csv'
dfCancion = pd.read_csv(ruta, sep=';', dtype=str)
# dfCancion['kids'] = False
# dfCancion['created_at'] = fecha
# dfCancion['updated_at'] = fecha
dfCancion['tempo'] = 0
dfCancion.to_csv(ruta, sep=';', index=False)
