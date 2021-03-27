import requests
import lxml.html as html
import os
import datetime

# Constantes

HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//div/a[starts-with(@class,"kicker")]/@href[contains(.,"www.larepublica.co")]'
XPATH_LINK_TO_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_LINK_TO_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_LINK_TO_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'
XPATH_LINK_TO_AUTHOR = '//div[@class = "autorArticle"]/p/text()'

# Funciones para ejecutar el script

def parse_notice(link, today):

    #Bloque para manejar los status code u otros errores que se presenten
    try:
        
        #Respuesta de una petición al conectarse a un url
        response = requests.get(link)

        # Comprobar que la respuesta sea OK, comprobando el status code
        if response.status_code == 200:

            # Trae el contenido de HTML (content) que necesita ser traducido (decode) de tal manera que python lo entienda
            notice = response.content.decode('utf-8')

            # Transforma el contenido HTML a un archivo útil para Xpath
            parsed = html.fromstring(notice)
            
            # Bloque para validar que estoy traendo el título, autor, resumen y cuerpo de la noticia.
            try:

                # Traer el primer elemento de la lista. (El título tiene un solo elemento)
                title = parsed.xpath(XPATH_LINK_TO_TITLE)[0]
                # Quitar las comillas dobles del título, evitando un error en OS.
                title = title.replace('\"', '')
                # Traer el primer elemento del autor. (El autor tiene un solo elemento)
                author = parsed.xpath(XPATH_LINK_TO_AUTHOR)[0]

                # Traer el primer elemento del resumen. (El resumen tiene un solo elemento)
                summary = parsed.xpath(XPATH_LINK_TO_SUMMARY)[0]
                
                # Traer el contenido del cuerpo
                body = parsed.xpath(XPATH_LINK_TO_BODY)

            except IndexError:
                # Se prevee cuando una noticia no tenga un resumen u otro elemento
                return
            
            # Guardar el contenido de la noticia en un archivo dentro de la carpeta previamente creada.
            # with es un manejador de contexto que nos permite mantener las cosas de forma segura si algo sucede y el script se cierra
            with open(f'{today}/{title}.txt','w', encoding ='utf-8') as f:

                # Escribir en el archivo el título de la noticia
                f.write(title)
                f.write('\n\n')

                # Escribir en el archivo el autor de la noticia
                f.write(author)
                f.write('\n\n')

                # Escribir en el archivo el resumen de la noticia
                f.write(summary)
                f.write('\n\n')

                # Escribir en el archivo el cuerpo de la noticia
                for p in body:
                    f.write(p)
                    f.write('\n')
                print("FIN 1")
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():

    #Bloque para manejar los status code u otros errores que se presenten
    try:
        
        #Respuesta de una petición al conectarse a un url
        response = requests.get(HOME_URL)
        
        # Comprobar que la respuesta sea OK, comprobando el status code
        if response.status_code == 200:
            
            # Trae el contenido de HTML (content) que necesita ser traducido (decode) de tal manera que python lo entienda
            home = response.content.decode('utf-8')
            
            # Transforma el contenido HTML a un archivo útil para Xpath
            parsed = html.fromstring(home)
            
            # Extrae las urls de la página web usando Xpath, usando el archivo parseado previamente
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            # print(links_to_notices)

            # Extrae la fecha actual. Se usa strftime para tener una cadena de caracteres con un determinado formato
            today = datetime.date.today().strftime('%d-%m-%Y')

            # Verifica que no exista una carpeta con el nombre de la fecha de hoy, para posteriormente crearlo.
            if not os.path.isdir(today):
                os.mkdir(today)

            # Llamo a la función para recorrer la lista de los links usando un for.
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            # Elevar un error (ValueError), mostrando el status code
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)

# Función para ejecutar los scripts
def run():
    parse_home()

# Menu principal
if __name__ == '__main__':
    run()