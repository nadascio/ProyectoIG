from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import ctypes
from datetime import datetime,timedelta
import time
import random
import sys
import csv
import re
import os
from os import path


#################################################################################################################################################
#####################################  CONFIGURACIONES BÁSICAS ##################################################################################
#################################################################################################################################################


Usuario = "blur.vs"                # Completar con usuario (entre comillas)       
Contraseña = "335522LurA"            # Completar con Contraseña (entre comillas)    

Link_foto = "https://www.instagram.com/p/CMrcGkNFCBr/"    #Introducir el link de la foto para hacer los likes (entre comillas) https://www.instagram.com/maselmariner/

Ciclos_Descanso = 20               # Cada cuantos perfiles se descansa (espera una pausa para continuar el proceso)
Descanso = random.randint(100,200) # Descanso en segundos / seteado para descansar entre 3 minutos (180) y 4 minutos (240) 

LikesFotos = 207                          # Completar con Cantidad de Likes que tiene la foto
Empezar_desde_perfil = 1           # En caso de que falle se puede retomar el perfil introduciendo / por default arranca en el primer perfil
Hasta_perfil = "la"         # Por defecto se harán todos los perfiles posibles. Caso contrario modificar por el nro de perfil sacando las comillas (ej: Hasta_perfil = 120)
                                  
n = random.randint(1,3)            # Tiempos de espera - seteados entre 1 y 3 segundos (desde,hasta).
n2 = random.randint(4,6)           # Tiempos de espera para dejar de seguir perfil- seteados entre 4 y 6 segundos (desde,hasta).




#################################################################################################################################################
#####################################  DAR INICIO AL BOT #######################################################################################
#################################################################################################################################################




#Abrir Navegador , activar las 'Actions' , iniciar reloj

driver = webdriver.Chrome()
driver.maximize_window()

act = ActionChains(driver)
Hora_historica = datetime.now()
Hora_inicio = datetime.now()

##Hora_Maxima = (datetime.now()+timedelta(minutes=20)) - datetime.now()  ## cada cuanto hace el break / seteado para 20 mins

##################################### LOG A INSTAGRAM ###########################################################################################

driver.get("https://www.instagram.com/")

WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[name='username']")))

username = driver.find_element_by_css_selector("[name='username']")
password = driver.find_element_by_css_selector("[name='password']")
login = driver.find_element_by_css_selector("button")

time.sleep(n)


username.send_keys(Usuario)  ########### INTRODUCIR USUARIO ###########
password.send_keys(Contraseña)   ########### INTRODUCIR CONTRASEÑA ########

login.click()

######################## VARIABLES DE LISTA DE LINKS #############

Links = []  #  PRIMER LISTA DE ELEMENTOS DE PERFILES EN ME GUSTA
lista = []  #  PLISTA TEMPORAL DE LECTURA DE CSV
Lista_final_links = [] #  LUSTA DEFIBUTUVA
conteo = int(LikesFotos/3) 


##################################### DEFINIR NOMBRE ARCHIVO CSV  Y VERIFICAR SI EXISTE#######################################################

time.sleep(10)

start = 'instagram.com/p/'
end = '/'

Nombre_csv = re.search('%s(.*)%s' % (start, end), Link_foto).group(1)   ####   DEFINO NOMBRE DEL ARCHIVO



if path.exists(f'{Nombre_csv}.csv') == True:  ####   SI EXISTE EL ARCHIVO NO ES NECESARIO HACER LOS TABS NI ABRIR IMAGEN
    
    with open(f'{Nombre_csv}.csv','r') as f:
        reader = csv.reader(f)

        for i in reader:   ###   MANDO LA INFO A NUEVA LISTA
            lista.append(i)


    cant = len(lista)

    for x in range (0,cant):  ###   SUMO CADA ELEMENTO A LA LISTA PARA EL LOOP

        Lista_final_links = Lista_final_links + lista[x]





else:

    ##################################### VISITAR LINK FOTO #######################################################

    time.sleep(10)


    driver.get(Link_foto)  ###########  LINK DE FOTO  #################


    WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME,"zV_Nj")))
    time.sleep(n)


    driver.find_element_by_class_name("zV_Nj").click()


    ###########COMPROBACIÓN SI ABRIÓ VENTANA

    try:  #ESTA COMPROBACION SE HACE POR SI NO ABRE BIEN EL DESPLEGABLES DE ME GUSTA, SUELE BUGGEARSE
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a.FPmhX.MBL3Z")))
        time.sleep(n)
        Lista_perfiles = driver.find_elements_by_css_selector("a.FPmhX.MBL3Z")

    except NoSuchElementException:  #SI NO SE ABRE, REINTENTAR

        driver.find_element_by_class_name("zV_Nj").click()
        time.sleep(n)
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a.FPmhX.MBL3Z")))
        time.sleep(n)
        Lista_perfiles = driver.find_elements_by_css_selector("a.FPmhX.MBL3Z")





    for perfil in Lista_perfiles:

        a = perfil.get_attribute("href")

        Links.append(a)


    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,"m82CD")))
    driver.find_element_by_class_name("m82CD").click()
        

    time.sleep(n)



    ##################################### LOOP PARA BUSCAR URLS #######################################################

    
    for a in range(1,conteo):

        src = driver.find_elements_by_css_selector("a.FPmhX.MBL3Z")

        try:
            for perfil in src:
                e = perfil.get_attribute("href")
                Links.append(e)
        except Exception:
            continue


        try:
            driver.execute_script("arguments[0].scrollIntoView();", src[8])
            time.sleep(1)

        except Exception:
            continue

         
        a += 1

    ##################################### CREACCIÓN LISTA FINAL LINKS #######################################################

    Lista_final_links = []

    for i in Links:  #SE QUITAN LOS URLS REPETIDOS EN CASO DE EXISTIR
        if i not in Lista_final_links:
            Lista_final_links.append(i)

    time.sleep(n)


    ##################################### CREACCIÓN ARCHIVO CSV #######################################################


    with open(f'{Nombre_csv}.csv','w',newline='') as f:
        thewritter = csv.writer(f)
        

        for i in Lista_final_links:

            thewritter.writerow([i])
    
 




############################# PROCESO DE LIKES A LOS DIFERENTES PERFILES #######################################################

Likes = 0
Priv = 0
loop = 0
ciclo = 0
Seguidos = 0

nI = len(Lista_final_links)

if type(Hasta_perfil) != str:  ### ESTA CONDICIÓN SE AGREGA PARA  EN CASO DE QUE SE QUIERA CAMBIAR EL ÚLTIMO PERFIL QUE SE QUIERA ENTRAR
    if Hasta_perfil < nI:
        nI = Hasta_perfil

Empezar_Loop = (Empezar_desde_perfil -1)   ##################### PORQUE NUMERO DE PERFIL EMPEZAR/RETOMAR, SI FALLA MODIFICAR ESTE NUMERO

#logueo 1 a 1 de los perfiles en lista consolidada

for profiles in range(Empezar_Loop, nI):   
    
    i = Lista_final_links[profiles]

    driver.get(i)
    time.sleep(n)

    Hora_en_curso = datetime.now()
    

    
    try:   #CHECK SI LA CUENTA ES PRIVADA Y LUEGO CLICK EN SEGUIR
        time.sleep(n)

        driver.find_element_by_class_name("rkEop")
        fotos = []
        print(loop+Empezar_Loop,' - Perfil Privado')
        Priv += 1

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm")))
        
        driver.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm").click()  #CLICK EN SEGUIR

        try: #SI ENCUENTRA BOTON DEJAR SEGUIR LE HACE CLICK, SINO LO ENCUENTRA ES PORQUE YA LA SEGUÍA ENTONCES LUEGO CANCELARÁ LA OPCIÓN DEJAR DE SEGUIR
            time.sleep(n)

            driver.find_element_by_css_selector("button.aOOlW.HoLwm").click()  
            
            
        except NoSuchElementException:  #ESTA EXCEPCIÓN ES PARA SABER SI EL BOT DEBE DEJAR DE SEGUIR O NO DEJAR DE SEGUIR (SI LA CUENTA ANTERIORMENTE YA LA SEGUÍA)
        
            try:     #SALE EL CARTEL Y CANCELA LA OPCIÓN DE DEJAR DE SEGUIR
                time.sleep(n)

                driver.find_element_by_css_selector(".vBF20._1OSdk").click()  
                time.sleep(n2)

                driver.find_element_by_css_selector("button.aOOlW.-Cab_").click()
                time.sleep(n)

                print(loop+Empezar_Loop,' - Perfil Seguido')
    
                Seguidos += 1

            except NoSuchElementException:  #EN CASO QUE NO FUERA SEGUIDA ANTERIORMENTE ENTRA Y DEJA DE SEGUIRLA NORMALMENTE PARA QUE NO QUEDE COMO SEGUIDOR EN LA CUENTA


                time.sleep(n)
                driver.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm").click() 
                time.sleep(n2)

                driver.find_element_by_css_selector("button.aOOlW.-Cab_").click()
                time.sleep(n)

                print(loop+Empezar_Loop,' - Perfil Seguido')
    
                Seguidos += 1       



    except NoSuchElementException: #Si no es privada que continúe proceso
        time.sleep(n)
        fotos = []
        pass       

    try:    #Busqueda de imagenes en perfil
        fotos = driver.find_elements_by_class_name("_9AhH0")
    
    except NoSuchElementException: #si no carga que siga
        fotos = []
        pass


#Check de cantidad de fotos que hay en el perfil. Si es mayor o igual a 3 se entra a 3 fotos, si es 2 se entra a 2 y si es 1 se entra a 1.
 

    if len(fotos) >= 3:  #EN CASO DE QUE TENGA 3 O MÁS FOTOS
        
        fotos = fotos[0:3]

        

        for clicks_en_fotos in fotos:

            try:
                
                clicks_en_fotos.click()
                time.sleep(n)

            except ElementClickInterceptedException:
                
                continue

            try:
                time.sleep(3)
                driver.find_element_by_css_selector("span.fr66n").click()
                time.sleep(1)
                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                Likes += 1
                
            except NoSuchElementException:

                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                pass

            except ElementClickInterceptedException:

                time.sleep(n)   
                print("Límite de Likes Alcanzado")
                
                try:
                    driver.find_element_by_css_selector("[aria-label='Cerrar']").click()  

                except NoSuchElementException:

                    time.sleep(n)   


                    Cant_perfiles_visitados = loop
                    Hora_final = datetime.now()
                    Hora_total = (Hora_final - Hora_historica)

                    print("Límite de Likes Alcanzado")
                    ctypes.windll.user32.MessageBoxW(0,"LIMITE DE LIKES ALCANZADO. Reintentar en otro momento. ", "Proceso Terminado", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Hora_total)[:-7] + ' (H:MM:SS)', "Tiempo de Ejecución del Bot", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Likes) + ' Likes.', "Likes total a Fotos", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados) + ' Perfiles.', "Cantidad de Perfiles Visitados", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados - Priv) + ' Perfiles.', "Cantidad de Perfiles Disponibles para Likes", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Priv) + ' Perfiles Privados.', "Cantidad de Perfiles Privados", 0)   
                    ctypes.windll.user32.MessageBoxW(0,str(Seguidos) + ' Perfiles Follow y Unfollow.', "Total de Follow/Unfollow", 0)                
                    driver.close()

            


            time.sleep(n)


    if len(fotos) == 2:   #EN CASO DE QUE TENGA 2 FOTOS
        
        fotos = fotos[0:2]

        

        for clicks_en_fotos in fotos:

            try:
                
                clicks_en_fotos.click()
                time.sleep(n)

            except ElementClickInterceptedException:
                
                continue

            try:
                driver.find_element_by_css_selector("span.fr66n").click()
                time.sleep(n)
                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                Likes += 1
                
            except NoSuchElementException:
                time.sleep(n)
                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                pass

            except ElementClickInterceptedException:

                time.sleep(n)   
                print("Límite de Likes Alcanzado")
                
                try:
                    driver.find_element_by_css_selector("[aria-label='Cerrar']").click()  

                except NoSuchElementException:

                    time.sleep(n)   


                    Cant_perfiles_visitados = loop
                    Hora_final = datetime.now()
                    Hora_total = (Hora_final - Hora_historica)

                    print("Límite de Likes Alcanzado")
                    ctypes.windll.user32.MessageBoxW(0,"LIMITE DE LIKES ALCANZADO. Reintentar en otro momento. ", "Proceso Terminado", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Hora_total)[:-7] + ' (H:MM:SS)', "Tiempo de Ejecución del Bot", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Likes) + ' Likes.', "Likes total a Fotos", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados) + ' Perfiles.', "Cantidad de Perfiles Visitados", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados - Priv) + ' Perfiles.', "Cantidad de Perfiles Disponibles para Likes", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Priv) + ' Perfiles Privados.', "Cantidad de Perfiles Privados", 0) 
                    ctypes.windll.user32.MessageBoxW(0,str(Seguidos) + ' Perfiles Follow y Unfollow.', "Total de Follow/Unfollow", 0)                  
                    driver.close()



    if len(fotos) == 1:    #EN CASO DE QUE TENGA 1 SOLA FOTO
        
        fotos = fotos[0:1]

        

        for clicks_en_fotos in fotos:

            try:
                
                clicks_en_fotos.click()
                time.sleep(n)

            except ElementClickInterceptedException:
                
                continue

            try:
                driver.find_element_by_css_selector("span.fr66n").click()
                time.sleep(n)
                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                Likes += 1
                
            except NoSuchElementException:
                time.sleep(n)
                driver.find_element_by_css_selector("[aria-label='Cerrar']").click()
                pass

            except ElementClickInterceptedException:
                
                time.sleep(n)   
                print("Límite de Likes Alcanzado")
                
                try:
                    driver.find_element_by_css_selector("[aria-label='Cerrar']").click()  

                except NoSuchElementException:

                    time.sleep(n)   


                    Cant_perfiles_visitados = loop
                    Hora_final = datetime.now()
                    Hora_total = (Hora_final - Hora_historica)

                    print("Límite de Likes Alcanzado")
                    ctypes.windll.user32.MessageBoxW(0,"LIMITE DE LIKES ALCANZADO. Reintentar en otro momento. ", "Proceso Terminado", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Hora_total)[:-7] + ' (H:MM:SS)', "Tiempo de Ejecución del Bot", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Likes) + ' Likes.', "Likes total a Fotos", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados) + ' Perfiles.', "Cantidad de Perfiles Visitados", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Cant_perfiles_visitados - Priv) + ' Perfiles.', "Cantidad de Perfiles Disponibles para Likes", 0)
                    ctypes.windll.user32.MessageBoxW(0,str(Priv) + ' Perfiles Privados.', "Cantidad de Perfiles Privados", 0)  
                    ctypes.windll.user32.MessageBoxW(0,str(Seguidos) + ' Perfiles Follow y Unfollow.', "Total de Follow/Unfollow", 0)                 
                    driver.close()




    loop += 1
    ciclo += 1                

    print(loop+Empezar_Loop,' - ', i, ' - Hora ', str(Hora_en_curso)[:-7] ) #Imprimo numero perfil procesado y la hora en consola para que se muestren los usuarios visitados

    if ciclo > Ciclos_Descanso:
        print("Descansando... " , str(Hora_en_curso)[:-7])
        time.sleep(Descanso)
        ciclo = 0


#Detalles finales cuando el BOT termina de ejecutarse



Cant_perfiles_visitados = loop
Hora_final = datetime.now()
Hora_total = (Hora_final - Hora_historica)

ctypes.windll.user32.MessageBoxW(0,f'''- Tiempo de Ejecución : {str(Hora_total)[:-7]} (H:MM:SS)
- Likes total a Fotos : {str(Likes)}
- Cantidad de Perfiles Disponibles para Likes : {str(Cant_perfiles_visitados - Priv)}
- Cantidad de Perfiles Privados : {str(Priv)}
- Cantidad de Perfiles en total : {str(Cant_perfiles_visitados)}''', "Proceso Terminado!", 0)


driver.close()