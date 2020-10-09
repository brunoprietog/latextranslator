#-*-:coding:utf-8-*-
import sys
import re
import translator as tl

nombre_archivo = sys.argv[1]
if nombre_archivo[-3:] == '.md':
	codigo=tl.markdown(nombre_archivo)
	tl.traducido(codigo, nombre_archivo[:-3]+' traducido.md')
elif nombre_archivo[-4:] == '.tex':
	codigo = tl.string(nombre_archivo, False)
	#Revisa si hay archivos incrustados en el tex principal para agregarlos a codigo
	patron = re.compile('\\\input\{(?P<archivo>[^\{]*)\}')
	ArchivosHijos = patron.findall(codigo)
	patron=re.compile(r'\.tex$')
	for i in ArchivosHijos:
		if len(patron.findall(i))==0: j=i+'.tex'
		else: j=i
		codigo = codigo.replace('\\input{'+i+'}', tl.string(j, True))
	codigo = tl.graficos(codigo)
	formulas=tl.buscar_formulas(codigo, 1)
	ecuaciones=tl.buscar_formulas(codigo, 2)
	codigos=tl.buscar_codigos(codigo)
	codigo=tl.reemplazar_formulas(codigo, ecuaciones, 'ecuacion', 'r')
	codigo=tl.reemplazar_formulas(codigo, formulas, 'formula', 'r')
	codigo=tl.reemplazar_formulas(codigo, codigos, 'codigo', 'r')
	ecuaciones=tl.traducir_formulas(ecuaciones)
	formulas=tl.traducir_formulas(formulas)
	codigo = tl.titulos(codigo)
	codigo = tl.limpiar_basura(codigo)
	codigo = tl.enumeracion(codigo)
	codigo=tl.reemplazar_formulas(codigo, ecuaciones, 'ecuacion', 'w')
	codigo=tl.reemplazar_formulas(codigo, formulas, 'formula', 'w')
	codigo=tl.reemplazar_formulas(codigo, codigos, 'codigo', 'w')
	codigo=tl.split_codigo(codigo)
	codigo=re.sub(r'\n{3,}', r'\n\n', codigo)
	codigo=codigo.replace('\n', '\r\n')
	tl.traducido(codigo, nombre_archivo[:-4]+' traducido.txt')
else:
	print('Extensión no soportada')
	exit()
print ("Traducido correctamente")