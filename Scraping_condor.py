import time
import json
import csv
import os

#Selenium
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


#BeatifulSoup
from bs4 import BeautifulSoup
import requests


# Imprime la ruta del directorio actual
print("Directorio actual:", os.getcwd())

#Urls a utilizar
login_url = 'https://estudiantes.portaloas.udistrital.edu.co/appserv/'
url = 'https://estudiantes.portaloas.udistrital.edu.co/academicopro/index.php?index=mClHx-m_sB_AiTKR9TQo4KhM800aJirc7LzedeOC2MPiWXgxjkRO4atpzwiLKgc4xc6SALIBCKB9Erx0SffK6O5bstqt-Pr64EuwlKCzS-QTlLWk3QbjllMWc1dQvkLNIIjfgQ-ZDJpsqAEDWoNmBgam5RfeLF7FEm8ireekvA8Q_gOYBIb53JEsBd86wHsupy9lyzafb-NxAfzq2Nko2Q' 


#Selenium
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(chrome_options)
driver.get(login_url)


def inicio_sesion():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            
        username = config['usuario']
        password = config['clave']
        
        caja = driver.find_element(By.XPATH,'//*[@id="nickname"]')
        caja.send_keys(username)#Poner usuario
        caja = driver.find_element(By.XPATH,'//*[@id="contrasena"]')
        caja.send_keys(password)#Poner contraseña
        # Cambiar al frame del captcha
        driver.switch_to.frame(0)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
        captcha_element = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')
        captcha_element.click()
        
        time.sleep(5)
        # Volver al contenido principal
        driver.switch_to.default_content()
        # Esperar a que el captcha se resuelva y el botón sea clickeable
        ingresar_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ingresar"]')))
        ingresar_button.click()
        print("Entro a la pagina") 
        
    except FileNotFoundError:
        print("Archivo 'config.json' no encontrado.")
    except json.JSONDecodeError:
        print("Error al decodificar 'config.json'. Verifica que sea un JSON válido.")
    except KeyError:
        print("Error al acceder a las claves de usuario/contraseña. Verifica las claves en 'config.json'.")    
    except ElementClickInterceptedException:
            actions = ActionChains(driver)
            actions.move_to_element(ingresar_button).perform()
            ingresar_button.click()    
               
    time.sleep(10)
    scraping_notas()
    
    
def scraping_notas():    
    driver.get(url)
    # Hacer web scraping de la página
    titulo = driver.find_element(By.XPATH,'/html/body/table/tbody/tr[2]/td/table[5]/tbody/tr[1]/td/table[3]/caption').text
    notas = driver.find_element(By.XPATH,'/html/body/table/tbody/tr[2]/td/table[5]/tbody/tr[1]/td/table[4]').text
    
    Conversion_csv(titulo,notas)
    # Cerrar el navegador
    time.sleep(3)
    driver.quit()
    
def Conversion_csv(titulo,notas):
    try:
        titulo_txt = str(titulo)
        notas_txt = str(notas)

        archivo_txt = 'HTML_sucio.txt'

        with open(archivo_txt, 'w', encoding='utf-8') as archivo:
            archivo.write(titulo_txt)
            archivo.write(notas_txt)

        print(f"HTML guardado en {archivo_txt}")

        # Crear una lista para almacenar los datos estructurados
        datos_estructurados = []

        # Agregar el título a la lista
        datos_estructurados.append(['Título', titulo_txt])
        
        # Iterar sobre las notas y extraer la información relevante
        for linea in notas_txt.split('\n'):
            # Ejemplo: Extraer el texto de cada nota
            texto_linea = '   '.join(linea.split())  # Agrega más espacio entre cada palabra

            # Añadir los datos a la lista
            datos_estructurados.append([texto_linea])

        # Nombre del archivo CSV
        Cambio_csv = 'notas.csv'

        # Escribir los datos estructurados en un archivo CSV
        with open(Cambio_csv, 'w', encoding='utf-8', newline='') as archivo_csv:
            # Crear un objeto escritor CSV
            trancision = csv.writer(archivo_csv)

            # Escribir los datos en el archivo CSV
            trancision.writerows(datos_estructurados)

        print(f"Datos organizados y guardados en {Cambio_csv}")

    except Exception as e:
        print(f"Error en Conversion_csv: {str(e)}")
    
inicio_sesion()

  
      









