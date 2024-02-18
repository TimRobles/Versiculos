from funciones import *

urlBase='https://www.palabrayespiritu.org'
url=urlBase + '/musica/'
print(url)
r=requests.get(url)
soup=BeautifulSoup(r.text, 'lxml')
artistas=soup.findAll("div", {"class":"col-lg-3 col-md-3 col-sm-4 col-xs-6 ministries-grid"})
linkArtistas=[]

for artista in artistas:
    link=artista.find("a", href=True)
    linkArtistas.append(urlBase + link["href"])

linkAlbums=[]
for url in linkArtistas:
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'lxml')
    albums=soup.findAll("div", {"class":"col-md-4 ministries-grid"})

    for album in albums:
        link=album.find("a", href=True)
        linkAlbums.append(urlBase + link["href"])

linkCanciones=[]
for url in linkAlbums:
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'lxml')
    canciones=soup.findAll("td")

    for cancion in canciones:
        link=cancion.find("a", href=True)
        if link!=None: linkCanciones.append(urlBase + link["href"])

with open('link_canciones.txt', 'w') as fp:
    for link in linkCanciones:
        fp.write("%s\n" % link)
