#-*-:coding:utf-8-*-
import sys
import re
import translator as tl

#Se carga el archivo del usuario
nombre_archivo = sys.argv[1]
#Carga el texto a el programa de traduccion
codigo = tl.string(nombre_archivo, False)
#Revisa si hay archivos incrustados en el tex principal para agregarlos a codigo
patron = re.compile('\\\input\{(?P<archivo>.*\.tex)\}')
ArchivosHijos = patron.findall(codigo)
for i in ArchivosHijos:
	codigo = codigo.replace('\\input{'+i+'}', ut.string(i, True))
codigo = tl.graficos(codigo)
codigo = tl.formulas(codigo)
codigo = tl.titulos(codigo)
codigo = tl.limpiar_basura(codigo)
tl.traducido(codigo, tl.nombre_final(nombre_archivo)+' traducido.txt')
print ("Traducido correctamente")