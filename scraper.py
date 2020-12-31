
import requests  # importo paquetes q voy a necesitar
import lxml.html as html
import os
import datetime  # Estos ultimos modulos serviran para crear carpetas con fechas de hoy


HOME_URL = 'https://www.larepublica.co/'

#XPATH_LINK_TO_ARTICLE = '//h2[@class="headline"]/a/@href'
# el path q funciona
XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title"]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'
# creo constantes para extraer los links,titulos,cuerpos de las noticias que realice con Xpath


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode(
                'utf-8')  # trae el html de la noticia
            # genera el html en el q puedo aplicar xpath
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            # "WITH""manejador contextual
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:  # para trabajar de manera segura
        # Con esto,hago un get a este URL, y me devolvera todo el documento HTML y todo lo q involucra al HTTP(cabeceras x ej)
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # response.content devuelve el html de la respuesta...y el decode, codifica todos los caracteres especiales a algo q python puede leer
            home = response.content.decode('utf-8')
            # toma el contenido html q tengo en la variable home,  y lo trnsforma en un documento en el q puedo  hacer Xpath
            parsed = html.fromstring(home)
            # obtengo lista de resultados d los links
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notice)
            today = datetime.date.today().strftime('%d-%m-%Y')  # con el modulo datetime, manejamos las fechas, con el metodo date, nos trae una fecha, y con "today", traemos la fecha de hoy, y lo guardaen un objeto, pero necesito transformarlo en cadena de caracter, por eso, strftime q nos permite modificaral formato para el q querramos usar
            # pregunto si existe, en la carpeta donde estamos, una carpeta llamada "today"...sino, la creamos
            if not os.path.isdir(today):
                os.mkdir(today)  # creo la carpeta si no existe
            for link in links_to_notice:
                parse_notice(link, today)

        else:  # elevo el error
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
