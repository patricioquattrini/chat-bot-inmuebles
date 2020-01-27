from bs4 import BeautifulSoup
import requests

class Zonaprop():

    urlBase = "https://www.zonaprop.com.ar/"
    def BuscarDeptos(self, lista_zonaprop,inmueble=None ,barrio=None, ambientes=None, precioHasta=None):

        urlFInal = self.obtenerUrl(inmueble, barrio, ambientes, precioHasta)
        i=1
        while True:
            page = requests.get(urlFInal + "-pagina-" + str(i) + ".html")
            soup = BeautifulSoup(page.content, "html.parser")

            if i == 1:
                noHayAvisos = soup.find_all("div", class_="no-results__message")
                if len(noHayAvisos):
                    break
                cantDeptosSoup = soup.find_all("h1", class_="list-result-title")
                cantDeptosText = cantDeptosSoup[0].text
                cantDeptosTotal = int(((cantDeptosText.split()[0])).replace(".", ""))

            #ubicaciones = soup.find_all("span", class_="posting-location")
            #prices = soup.find_all("span", class_="first-price")
            urlsAvisosYTitulosAv = soup.find_all("a", class_="go-to-posting")
            masInfos = soup.find_all("ul", class_="main-features go-to-posting")
            lista_ambientes = []
            self.buscarAmbientes(masInfos, lista_ambientes)

            for j in range(0, len(lista_ambientes)):

                urlAviso = "https://www.zonaprop.com.ar"+urlsAvisosYTitulosAv[j]['href']
                if ambientes == None:
                    lista_zonaprop.append(urlAviso)
                else:
                    if str(ambientes) == lista_ambientes[j]:
                        lista_zonaprop.append(urlAviso)

            if cantDeptosTotal > 20:
                cantDeptosTotal-=20
            else:
                break
            i+=1


    def buscarAmbientes(self, infos, lista_ambientes):

        for info in infos:
           ls = (info.text).split()
           for j in range(0, len(ls)):
                if ls[j] == "Ambiente":
                    lista_ambientes.append(ls[j - 1])
                if ls[j] == "Ambientes":
                    lista_ambientes.append(ls[j - 1])


    def obtenerUrl(self,inmueble=None, barrio=None, ambientes=None, precioHasta=None):
        urlPrep = self.urlBase
        inmueble = inmueble.lower()
        inmueble = inmueble.replace(" ", "-")
        urlPrep = urlPrep + inmueble + "-alquiler"
        if (barrio != None):
            barrio = barrio.lower()
            barrio = barrio.replace(" ", "-")
            urlPrep = urlPrep + "-" + barrio
        if ambientes:
            ambientes = int(ambientes)
            if (ambientes > 1):
                urlPrep = urlPrep + "-" + str(ambientes) + "-ambientes"  # ambiente ambientes
            if (ambientes == 1):
                urlPrep = urlPrep + "-" + str(ambientes) + "-ambiente"  # ambiente ambientes
        urlPrep = urlPrep+"-publicado-hace-menos-de-1-dia"
        if (precioHasta != None):
            ##precioHasta = str(precioHasta)
            urlPrep = urlPrep + "-menos-" + precioHasta + "-pesos"
        urlPrep = urlPrep + "-orden-publicado-descendente.html"
        return urlPrep