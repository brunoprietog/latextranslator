#-*-:coding:utf-8-*-
import sys
import re
import Utilities as ut

#Se carga el archivo del usuario
nombre_archivo = sys.argv[1]
#Carga el texto a el programa de traduccion
codigo = ut.string(nombre_archivo, False)
#Revisa si hay archivos incrustados en el tex principal para agregarlos a codigo
patron = re.compile('\\\input\{(?P<archivo>.*\.tex)\}')
ArchivosHijos = patron.findall(codigo)
for i in ArchivosHijos:
	codigo = codigo.replace('\\input{'+i+'}', ut.string(i, True))
codigo = ut.graficos(codigo)
codigo = ut.formulas(codigo)
codigo = ut.titulos(codigo)
codigo = ut.basura(codigo)
ut.traducido(codigo, ut.nombre_final(nombre_archivo)+' traducido.txt')
print ("Traducido correctamente")