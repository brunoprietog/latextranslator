#-*-:coding:utf-8-*-
import sys
import re
import Utilities as ut

nombre_archivo = sys.argv[1]

codigo = ut.string(nombre_archivo)



codigo = ut.graficos(codigo)
codigo = ut.formulas(codigo)
codigo = ut.titulos(codigo)
codigo = ut.basura(codigo)
ut.traducido(codigo, ut.nombre_final(nombre_archivo)+' traducido.txt')
print ("Traducido correctamente")