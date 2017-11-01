import sys
import json
import time
# Si el script se usa en Windows:
# * Modificar pyperclip_path por el directorio correspondiente.
# * Cambiar las llamadas hacia paste_xsel() por paste()
# * Descomentar las siguientes lineas.
#pyperclip_path=u"/usr/lib/python2.7/site-packages/pyperclip"
#if pyperclip_path not in sys.path: sys.path.append(pyperclip_path)
#from pyperclip import paste
import subprocess

ventana = Pattern("Ingresar texto.png").similar(0.50)
#palabras = ["cat", "dog", "prueba", "sldkkkjorieefezriogdfrg", "algomas"]
#palabras = "esto es una prueba de uso para el script de Spanglish".split(" ")  
ultimo_guardado = time.time()

def paste_xsel():
    p = subprocess.Popen(['xsel', '-b', '-o'],
                         stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode('utf-8')

def traductor(palabra):
    if not exists(ventana):
        rightClick(Pattern("icono del programa.PNG").similar(0.50))
        click("Boton de traduccion.PNG")
    type(Pattern("Ingresar texto.png").similar(0.50).targetOffset(-49,15), Key.DOWN + palabra + Key.ENTER)
    #click(Pattern("Ingresar texto.png").similar(0.50).targetOffset(140,-20))
    if exists("Copiar traduccion.PNG", 1):
        #print "Boton encontrado"
        click("Copiar traduccion.PNG")
    else: return ""
    #click(Pattern("Ingresar texto.png").targetOffset(137,10))
    return "\n".join(paste_xsel().split("\n")[1:-2])

def guardador():
    # Sobreescribe progreso.txt con el diccionario "progreso" actual
    configuraciones.seek(0)
    configuraciones.write(json.dumps(progreso))
    configuraciones.flush()

configuraciones=open("progreso.txt", "r+b")
progreso = json.loads(configuraciones.read())
#progreso={}
palabras = open("/mnt/windows/Archivos promedios/Carpeta de pasaje/vzprp.dic", "r")
linea = palabras.readline()
ultima_encontrada = False
ultimo_guardado=time.time()

# Continuamos donde nos quedamos la ultima vez
if progreso.has_key("ultima"):
    while ultima_encontrada == False:
        if linea == progreso["ultima"]:
            ultima_encontrada = True
        linea = palabras.readline()

while linea != "":
    palabra = linea.strip()
    print "%s Procesando %s: " % (time.strftime("[%d/%m/%Y %H:%M:%S]", time.localtime()), palabra),
    resultado = traductor(palabra)
    if resultado != '+{\xc3\xb1\xc3\xbd3' and resultado != "":
        if progreso.has_key(resultado): progreso[resultado].append(palabra)
        else: progreso[resultado] = [palabra]
        progreso["ultima"] = linea
        print "definicion/es encontrada/s"
    else: print "nada encontrado"
    if time.time() >= (ultimo_guardado + 5*60):
        guardador()
        ultimo_guardado = time.time()
    linea = palabras.readline()
    #print progreso