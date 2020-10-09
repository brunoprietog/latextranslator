#-*-:coding:utf-8-*-
import re
import blindtex
from blindtex import tex2all
import codecs
import config as conf

basura = open(conf.basura, 'r+', encoding='utf-8')
limpiar=''
while True:
	lines = basura.readlines()
	if not lines: break
	for line in lines: limpiar+=line
basura.close()
limpiar=eval(limpiar)

translations = open(conf.translations, 'r+', encoding='utf-8')
reemplazar=''
while True:
	lines = translations.readlines()
	if not lines: break
	for line in lines: reemplazar+=line
translations.close()
reemplazar=eval(reemplazar)

numeracion={
	'2': ('0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
	'3': ('0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX')
}

#Funciones de transformación de texto básico.
#Transforma el Archivo en un string y quíta lo que está antes de \begin{document} y lo siguiente a \end{document}
def string(nombre_archivo, hijo):
	archivo = open(nombre_archivo, 'r+', encoding='utf-8')
	codigo_sucio = ''
	codigo = ''
	dentro_documento = False
	if hijo == True: dentro_documento = True
	while True:
		lines = archivo.readlines()
		if not lines: break
		for line in lines: codigo_sucio+=line
	patron = re.compile('\\\input\{(?P<archivo>[^\{]*)\}')
	ArchivosHijos = patron.findall(codigo_sucio)
	patron=re.compile(r'\.tex$')
	for i in ArchivosHijos:
		if len(patron.findall(i))==0: j=i+'.tex'
		else: j=i
		codigo_sucio = codigo_sucio.replace('\\input{'+i+'}', string(j, True))
	codigo_sucio = codigo_sucio.replace('\r\n', '\n')
	lines=codigo_sucio.split('\n')
	preambulo=''
	macros=list()
	teoremas=list()
	patronmacros=re.compile(r'^\\r?e?newcommand *\{ *\\(?P<nuevocomando>[^#]*) *\} *\{ *\\(?P<comando>[^#]*) *\}$')
	patronmacros2=re.compile(r'^\\providecommand *\{ *\\(?P<nuevocomando>[^#]*) *\} *\{ *\\(?P<comando>[^#]*) *\}$')
	patronteoremas=re.compile(r'^\\newtheorem *\{ *(?P<nuevoteorema>.*) *\}.*\{ *(?P<teorema>.*) *\} *$')
	for line in lines:
		edit_line=line
		if dentro_documento == False:
			if "\\begin{document}" in line: dentro_documento = True
			macros+=patronmacros.findall(line)
			macros+=patronmacros2.findall(line)
			teoremas+=patronteoremas.findall(line)
			if line.strip() == '':
				preambulo += line+'\n'
				continue
			elif line.strip()[0] == "%":
				continue
			elif line.strip()[0] != "%" and '%' in line:
				linea=''
				caracter_especial=False
				for caracter in line:
					if caracter_especial==False and caracter=='%': break
					linea+=caracter
					if caracter_especial==True: caracter_especial=False
					if caracter=='\\': caracter_especial=True
				edit_line=linea
			preambulo+=edit_line+'\n'
		if dentro_documento == True:
			if line.strip() == '':
				codigo += line+'\n'
				continue
			elif line.strip()[0] == "%": continue
			elif line.strip()[0] != "%" and '%' in line:
				linea=''
				caracter_especial=False
				for caracter in line:
					if caracter_especial==False and caracter=='%': break
					linea+=caracter
					if caracter_especial==True: caracter_especial=False
					if caracter=='\\': caracter_especial=True
				edit_line=linea
			if "\\end{document}" in line: break
			codigo+=edit_line+'\n'
	archivo.close()
	fancyfootr=busqueda_avanzada(r'\\fancyfoot *\[ *[Rr] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyfootr)==1: codigo=fancyfootr[0]+codigo
	fancyfootc=busqueda_avanzada(r'\\fancyfoot *\[ *[Cc] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyfootc)==1: codigo=fancyfootc[0]+codigo
	fancyfootl=busqueda_avanzada(r'\\fancyfoot *\[ *[Ll] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyfootl)==1: codigo=fancyfootl[0]+codigo
	fancyheadr=busqueda_avanzada('\\\\fancyhead *\[ *[Rr] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyheadr)==1: codigo=fancyheadr[0]+codigo
	fancyheadc=busqueda_avanzada('\\\\fancyhead *\[ *[Cc] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyheadc)==1: codigo=fancyheadc[0]+codigo
	fancyheadl=busqueda_avanzada('\\\\fancyhead *\[ *[Ll] *\] *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(fancyheadl)==1: codigo=fancyheadl[0]+codigo
	date=busqueda_avanzada(r'\\date *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(date)==1: codigo=date[0]+'\n\n'+codigo
	author=busqueda_avanzada(r'\\author *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(author)==1: codigo=author[0]+'\n\n'+codigo
	subtitle=busqueda_avanzada(r'\\subtitle *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(subtitle)==1: codigo=subtitle[0]+'\n\n'+codigo
	title=busqueda_avanzada(r'\\title *\{(?P<texto>.*)\}', preambulo, ('{', '}'))
	if len(title)==1: codigo=title[0]+'\n\n'+codigo
	macros=set(macros)
	macros=list(macros)
	macros.sort(key=len)
	macros.reverse()
	teoremas=set(teoremas)
	teoremas=list(teoremas)
	teoremas.sort(key=len)
	teoremas.reverse()
	for macro in macros:
		macro=(macro[0].replace('\\', '\\\\'), macro[1].replace('\\', '\\\\'))
		codigo=re.sub('\\\\'+macro[0]+'(?P<caracter>[^a-zA-Z])', '\\\\'+macro[1]+'\g<caracter>', codigo)
	for teorema in teoremas:
		teorema=(teorema[0].replace('\\', '\\\\'), teorema[1].replace('\\', '\\\\'))
		codigo=re.sub(r'\\begin\{'+teorema[0]+'\}(.*\[(?P<teorema>.*)\])*', '\n'+teorema[1]+': \g<teorema>\n', codigo)
		codigo=codigo.replace('\\end{'+teorema[0]+'}', '\n')
	codigo=codigo.replace('\r\n', '\n')
	codigo=codigo.replace('\\\\', 'blindtexlineablindtex\\\\blindtexlineablindtex')
	codigo=codigo.replace('\\$', 'blindtexpesoblindtex')
	codigo=codigo.replace('\\(', '$')
	codigo=codigo.replace('\\)', '$')
	codigo=codigo.replace('\\[', '$$')
	codigo=codigo.replace('\\]', '$$')
	codigo=codigo.replace('blindtexlineablindtex\\\\blindtexlineablindtex', '\\\\')
	for i in limpiar['acentos']: codigo=codigo.replace(i[0], i[1])
	if '#symbolab' in codigo:
		patron= re.compile("\${1,2}[^\$]*\${1,2}")
		forms=patron.findall(codigo)
		codigo = ''
		for i in forms:
			codigo = codigo+'$'+i+'$\n'
	return codigo

def markdown(nombre_archivo):
	archivo_markdown = open(nombre_archivo, 'r+', encoding='utf-8')
	codigo_markdown=''
	while True:
		lines = archivo_markdown.readlines()
		if not lines: break
		for line in lines:
			if line.strip() == '': codigo_markdown += line+'\n'
			else: codigo_markdown+=line
	archivo_markdown.close()
	codigo_markdown=codigo_markdown.replace('\r\n', '\n')
	codigo_markdown=codigo_markdown.replace('\\$', 'blindtexpesoblindtex')
	formulas=buscar_formulas(codigo_markdown, 1)
	ecuaciones=buscar_formulas(codigo_markdown, 2)
	codigo_markdown=reemplazar_formulas(codigo_markdown, ecuaciones, 'ecuacion', 'r')
	codigo_markdown=reemplazar_formulas(codigo_markdown, formulas, 'formula', 'r')
	codigo_markdown=re.sub(r'(?P<ecuacion>blindtexecuacion\d+blindtexecuacion)', r'\n\n\g<ecuacion>\n\n', codigo_markdown)
	ecuaciones=traducir_formulas(ecuaciones, True)
	formulas=traducir_formulas(formulas)
	codigo_markdown=reemplazar_formulas(codigo_markdown, ecuaciones, 'ecuacion', 'w')
	codigo_markdown=reemplazar_formulas(codigo_markdown, formulas, 'formula', 'w')
	codigo_markdown=codigo_markdown.replace('blindtexpesoblindtex', '$')
	codigo_markdown=re.sub(r'\n{2,}', r'blindtexlineasblindtex', codigo_markdown)
	codigo_markdown=codigo_markdown.replace('blindtexlineasblindtex', '\n\n')
	codigo_markdown=codigo_markdown.replace('\n', '\r\n')
	return codigo_markdown

def busqueda_avanzada(patron, texto, delimitador=0):
	# Patrón para encontrar grupos en el parámetro que es un patrón
	# Se quitan los grupos para que en la lista de findall aparezca la expresión completa y no solo el grupo
	patron_quitar_grupo=re.compile(r'\(\?P\<\w*\>(?P<grupocontent>.*)\)', re.S)
	# Se aplica el patrón y queda como string
	string_patron_sin_grupo=re.sub(patron_quitar_grupo, r'\g<grupocontent>', patron)
	# Se genera el patrón usando el string anterior, un patrón sin grupos
	patron_sin_grupo=re.compile(r''+string_patron_sin_grupo, re.S)
	# Lista de encontrados que hay que empezar a reducir
	encontrados_preliminar=patron_sin_grupo.findall(texto)
	# Lista vacía para empezar a añadir los encontrados finales
	encontrados=list()
	# Mientras queden cadenas encontradas por analizar y añadir
	while encontrados_preliminar!=[]:
		# encontrados_preliminar puede contener varios elementos con cadenas, y esos elementos pueden tener varias cadenas
		for preliminar in encontrados_preliminar:
			# Si no se encuentran cadenas retorna lista vacía
			if patron_sin_grupo.findall(preliminar)==[]:
				return []
			else:
				# Patrón con 2 grupos, el primero una cadena cualquiera, el segundo, la última cadena que coincide con el patrón buscado
				# La idea es ir reduciendo la parte restante (el primer grupo) y añadir a la lista encontrados la cadena del segundo grupo
				patron_reductivo=re.compile(r'(?P<restante>.+)(?P<ultimo>'+string_patron_sin_grupo+')', re.S)
				# Si solo queda una cadena en uno de los elementos de encontrados_preliminar por añadir a la lista encontrados
				if len(patron_reductivo.findall(preliminar))==0:
					# Ahora el patrón solo contiene el patrón buscado originalmente pero sin grupos, ya que es la última cadena y no hay parte restante que seguir analizando
					patron_reductivo=re.compile(r''+string_patron_sin_grupo, re.S)
					# Esta es la cadena que posteriormente se añade a la lista encontrados
					reduccion=patron_reductivo.findall(preliminar)[0]
					# Si no hay delimitadores
					if delimitador==0:
						encontrados.append(reduccion)
						# Como ya se añadió a la lista encontrados, se elimina de encontrados_preliminar para que no lo vuelva a analizar
						encontrados_preliminar.remove(preliminar)
					# Si hay delimitadores
					else:
						# Si el caracter anterior al delimitador es \ no pasará al contador
						caracter_especial=False
						# Contador que irá sumando y restando cuando encuentre delimitadores
						cont_delimitadores=0
						# Hace lo mismo que reduccion
						reduccion_delimitadores=""
						for caracter in reduccion:
							# Aún no puede haber \
							if len(reduccion_delimitadores)<=1: caracter_especial=False
							# Si el caracter anterior es \\ se hace falso
							elif reduccion_delimitadores[-1]=='\\': caracter_especial=True
							# Si el caracter especial no está, suma o resta dependiendo del delimitador
							if caracter==delimitador[0] and caracter_especial==False: cont_delimitadores+=1
							if caracter==delimitador[1] and caracter_especial==False: cont_delimitadores-=1
							# Si el delimitador es el último correspondiente, no hay extras al medio y no es un caracter especial, se añade a la cadena y se corta el ciclo
							if cont_delimitadores==0 and caracter_especial==False and delimitador[1]==caracter:
								reduccion_delimitadores+=caracter
								break
							# Se continúa añadiendo caracteres
							reduccion_delimitadores+=caracter
							# Se resetea el verificador de caracter especial
							caracter_especial=False
						# Se añade a encontrados la cadena con los delimitadores correctos
						encontrados.append(reduccion_delimitadores)
						# Como ya se añadió a la lista encontrados, se elimina de encontrados_preliminar para que no lo vuelva a analizar
						encontrados_preliminar.remove(preliminar)
				# En este caso encontrados_preliminar contiene más cadenas para analizar
				else:
					# Se usa el patron_reductivo inicial con 2 grupos
					# Esta variable solo contiene el primer elemento encontrado con el patron_reductivo, que a su vez es una lista de 2 elementos, por los 2 grupos que contiene dicho patrón
					reduccion=patron_reductivo.findall(preliminar)[0]
					# Si no hay delimitadores
					if delimitador==0:
						# Se añade a encontrados_preliminar la parte restante para que en una iteración siguiente sea analizada
						encontrados_preliminar.append(reduccion[0])
						# Se añade a encontrados la cadena perteneciente al grupo 2 del patrón
						encontrados.append(reduccion[1])
						# Se elimina la cadena completa analizada, ya que la primera parte se agregó nuevamente a encontrados_preliminar para ser analizada de nuevo, y la última parte es una cadena ya encontrada y que por lo tanto no requiere ser analizada nuevamente
						encontrados_preliminar.remove(preliminar)
					# Si hay delimitadores
					else:
						# Si el caracter anterior al delimitador es \ no pasará al contador
						caracter_especial=False
						# Contador que irá sumando y restando cuando encuentre delimitadores
						cont_delimitadores=0
						# Hace lo mismo que reduccion
						reduccion_delimitadores=""
						for caracter in reduccion[1]:
							# Aún no puede haber \
							if len(reduccion_delimitadores)<=1: caracter_especial=False
							# Si el caracter anterior es \\ se hace falso
							elif reduccion_delimitadores[-1]=='\\': caracter_especial=True
							# Si el caracter especial no está, suma o resta dependiendo del delimitador
							if caracter==delimitador[0] and caracter_especial==False: cont_delimitadores+=1
							if caracter==delimitador[1] and caracter_especial==False: cont_delimitadores-=1
							# Si el delimitador es el último correspondiente, no hay extras al medio y no es un caracter especial, se añade a la cadena y se corta el ciclo
							if cont_delimitadores==0 and caracter_especial==False and delimitador[1]==caracter:
								reduccion_delimitadores+=caracter
								break
							# Se continúa añadiendo caracteres
							reduccion_delimitadores+=caracter
							# Se resetea el verificador de caracter especial
							caracter_especial=False
						# Se añade a encontrados_preliminar la parte restante para que en una iteración siguiente sea analizada
						encontrados_preliminar.append(reduccion[0])
						# Se añade a encontrados la cadena con los delimitadores correctos
						encontrados.append(reduccion_delimitadores)
						# Se elimina la cadena completa analizada, ya que la primera parte se agregó nuevamente a encontrados_preliminar para ser analizada de nuevo, y la última parte es una cadena ya encontrada y que por lo tanto no requiere ser analizada nuevamente
						encontrados_preliminar.remove(preliminar)
	# En estas 4 líneas se borran elementos duplicados y se ordena de mayor longitud a menor para que al traducir no hayan conflictos
	encontrados=set(encontrados)
	encontrados=list(encontrados)
	encontrados.sort(key=len)
	encontrados.reverse()
	encontrados_final=list()
	# Ahora se usa el patron_con_grupo para obtener lo que realmente se buscaba
	patron_con_grupo=re.compile(patron, re.S)
	for encontrado in encontrados:
		encontrados_final.append(patron_con_grupo.findall(encontrado)[0])
	return encontrados_final

def sub_avanzado(patron, patron_sub, lista, texto):
	patron_subear=re.compile(patron, re.S)
	for i in range(len(lista)):
		texto=texto.replace(lista[i], re.sub(patron_subear, patron_sub, lista[i]))
	return texto

def buscar_formulas(codigo, valor):
	if valor==1: patron= re.compile("\${1,1}[^\$]*\${1,1}?", re.M)
	else:
		patron= "\$\$\s*.*\s*\$\$"
		patron2="\\\\begin *\{ *equation *\** *\}[^\n]*\s*.*\s*\\\\end *\{ *equation *\** *\}"
		patron3="\\\\begin *\{ *align *\** *\}[^\n]*\s*.*\s*\\\\end *\{ *align *\** *\}"
		patron4="\\\\begin *\{ *eqnarray *\** *\}[^\n]*\s*.*\s*\\\\end *\{ *eqnarray *\** *\}"
	#Crea una lista "forms" con los resultados de las dos busquedas anteriores
	if valor==1: forms=patron.findall(codigo)
	else: forms=busqueda_avanzada(patron, codigo)+busqueda_avanzada(patron2, codigo)+busqueda_avanzada(patron3, codigo)+busqueda_avanzada(patron4, codigo)
	#Se ajusta el formato de la lista de salida
	forms=set(forms)
	forms=list(forms)
	forms.sort(key=len)
	forms.reverse()
	return forms

def buscar_codigos(codigo):
	patron="\\\\begin *\{ *verbatim *\** *\}[^\n]*\s*.*\s*\\\\end *\{ *verbatim *\** *\}"
	codes=busqueda_avanzada(patron, codigo)
	codes=list(codes)
	codes.sort(key=len)
	codes.reverse()
	return codes

def reemplazar_formulas(codigo, formulas, tipo, valor):
	if valor=='r':
		cont=1
		for formula in formulas:
			codigo=codigo.replace(formula, 'blindtex'+tipo+str(cont)+'blindtex'+tipo)
			cont+=1
	elif valor=='w':
		cont=1
		for formula in formulas:
			codigo=codigo.replace('blindtex'+tipo+str(cont)+'blindtex'+tipo, formula)
			cont+=1
	return codigo

#Traduce todas las fórmulas
def traducir_formulas(formulas, markdown=False):
	for i in formulas:
		patron= re.compile("\${1,1}(?P<formula>[^\$]*)\${1,1}?", re.M)
		patron2="\\\\begin *\{equation *\** *\}[^\n]*\s*(?P<formula>.*)\s*\\\\end *\{equation *\** *\}"
		patron3="\\\\begin *\{align *\** *\}[^\n]*\s*(?P<formula>.*)\s*\\\\end *\{ *align *\** *\}"
		patron4="\\\\begin *\{ *eqnarray *\** *\}[^\n]*\s*(?P<formula>.*)\s*\\\\end *\{ *eqnarray *\** *\}"
		patron5="\$\$\s*(?P<formula>.*)\s*\$\$"
		formula=patron.findall(i)+busqueda_avanzada(patron2, i)+busqueda_avanzada(patron3, i)+busqueda_avanzada(patron4, i)+busqueda_avanzada(patron5, i)
		formula.sort(key=len)
		formula.reverse()
		#utiliza blindtex para traducir los patrones encontrados anteriormente, reemplazandolos en el archivo original
		try:
			j=formula[0]
			j=re.sub(r' {2,}', r' ', j)
			for simbolo in reemplazar['simbolos']: j=j.replace(simbolo[0], simbolo[1])
			for expresion in reemplazar['reemplazos_latex']: j=j.replace(expresion[0], expresion[1])
			j = re.sub(r'\\[a-z]space *\{[^\{\}]*\}', r'', j)
			j = re.sub(r'\\not *\\in', r'\\notin', j)
			j = re.sub(r'\\math[a-z]+ *\{(?P<texto>[^\{\}]*)\}', r'\g<texto>', j)
			j=re.sub(r'\\textnormal *\{', r'\\text{', j)
			j=re.sub(r'\\text[a-z]+ *\{', r'\\text{', j)
			j = re.sub(r'\\bm *\{(?P<texto>[^\{\}]*)\}', r'\g<texto>', j)
			j = re.sub(r'\\begin *\{ *aligned *\} *\[[a-z]\]', '', j)
			j = re.sub(r'\\end *\{ *aligned *\}', '', j)
			for _ in range(5):
				j=sub_avanzado(r'\\mathop *\{(?P<dentro>.*)\}', r'\g<dentro>', busqueda_avanzada(r'\\mathop *\{.*\}', j, ('{', '}')), j)
				j=sub_avanzado(r'\\boxed *\{(?P<dentro>.*)\}', r'\g<dentro>', busqueda_avanzada(r'\\boxed *\{.*\}', j, ('{', '}')), j)
				j=sub_avanzado(r'\\vec *\{(?P<vector>\w)\}', r'\\vec \g<vector>', busqueda_avanzada(r'\\vec *\{\w\}', j, ('{', '}')), j)
				j=sub_avanzado(r'\\vec *\{(?P<vector>.*)\}', r' vecblindtexparentesisblindtex\g<vector>blindtexcierraparentesisblindtex', busqueda_avanzada(r'\\vec *\{.*\}', j, ('{', '}')), j)
				j=sub_avanzado(r'\\overline *\{(?P<overline>.*)\}', r'bar blindtexparentesisblindtex\g<overline>blindtexcierraparentesisblindtex', busqueda_avanzada(r'\\overline *\{.*\}', j, ('{', '}')), j)
			for expresion in reemplazar['basura_latex']: j=j.replace(expresion, '')
			j=re.sub(r'\\.?frac(?P<numerador>[^\{}])(?P<denominador>.)', r'\\frac{\g<numerador>}{\g<denominador>}', j)
			patronmatrices="\\\\begin *\{ *.matrix *\}\s*.+\s*\\\\end *\{ *.matrix *\}"
			patronmatrices2="\\\\begin *\{ *array *\} *\{ *[\| a-z]* *\}\s*.+\s*\\\\end *\{ *array *\}"
			lista_matrices=busqueda_avanzada(patronmatrices, j)+busqueda_avanzada(patronmatrices2, j)
			lista_matrices=set(lista_matrices)
			lista_matrices=list(lista_matrices)
			lista_matrices.sort(key=len)
			lista_matrices.reverse()
			for matriz in lista_matrices:
				matriz_arreglada=matriz
				if ('=' or '\\neq' or '\\ne ' or '<' or '>' or '\\leq' or '\\geq' or '\\le ' or '\\ge ') in matriz:
					matriz_arreglada=re.sub("\\\\begin\{array\} *\{ *[\| a-z]* *\}\s*", r'blindtexlineablindtex', matriz_arreglada)
					matriz_arreglada=re.sub("\s*\\\\end\{array\}", r'blindtexlineablindtex', matriz_arreglada)
					matriz_arreglada=re.sub(r'\s*blindtexlineablindtex\s*', r'blindtexlineablindtex', matriz_arreglada)
					matriz_arreglada=re.sub(r' *& *', r'', matriz_arreglada)
				else:
					matriz_arreglada=re.sub("\\\\begin *\{ *.matrix *\}\s*", r'blindtexparentesisblindtex\nblindtexparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub("\\\\begin *\{ *array *\} *\{ *[\| a-z]* *\}\s*", r'blindtexparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub("\s*\\\\end *\{ *.matrix *\}", r'blindtexcierraparentesisblindtexblindtexcierraparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub("\s*blindtexlineablindtex\s*\\\\end *\{ *array *\}", r'blindtexcierraparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub("\s*\\\\end *\{ *array *\}", r'blindtexcierraparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub(r'\s*blindtexlineablindtex\s*', r'blindtexcierraparentesisblindtex,blindtexlineablindtexblindtexparentesisblindtex', matriz_arreglada)
					matriz_arreglada=re.sub(r' *& *', r',', matriz_arreglada)
				j=j.replace(matriz, matriz_arreglada)
			x=blindtex.tex2all.read_equation(j)
			x=x.replace('b l i n d t e x l i n e a b l i n d t e x', '\n')
			patrontextos= re.compile("ç(?P<texto>[^ç]*)endtext", re.MULTILINE)
			textos=patrontextos.findall(x)
			textos=set(textos)
			textos=list(textos)
			textos.sort(key=len)
			textos.reverse()
			for texto in textos:
				texto2=texto.replace('&', 'blindtex&')
				texto2=texto.replace(' ', 'blindtexespacioblindtex')
				x=x.replace(texto, texto2)
			x=x.replace(' ', '')
			x=x.replace(':', ': ')
			x=x.replace('ç', '')
			x=x.replace('endtext', '')
			x=x.replace('linebreak', '')
			x=x.replace('blindtexparentesisblindtex', '(')
			x=x.replace('blindtexcierraparentesisblindtex', ')')
			x=x.replace('&', '')
			x=x.replace('blindtex&', '&')
			for simbolo in reemplazar['simbolos']: x=x.replace(simbolo[1], simbolo[2])
			for expresion in reemplazar['reemplazos_traduccion']: x=x.replace(expresion[0], expresion[1])
			x=re.sub(r'\^\((?P<exponente>.)\)', r'^\g<exponente>', x)
			x=re.sub(r'_\((?P<subindice>.)\)', r'_\g<subindice>', x)
			x=re.sub(r'√\((?P<raiz>.)\)', r'√\g<raiz>', x)
			if markdown:
				x=x.replace('\n', '\\\n')
				x=x.replace('[', '\\[')
				x=x.replace(']', '\\]')
				x=x.replace('{', '\\{')
				x=x.replace('}', '\\}')
				x=x.replace('^', '\\^')
				x=x.replace('_', '\\_')
			formulas[formulas.index(i)]=x
		except:
			pass
	return formulas

#Se deshace de los graficos encontrados en el codigo LaTeX
def graficos(codigo):
	codigo = re.sub(r"\\includegraphics *\[ *(?P<tiende>.*) *\] *\{ *(?P<nombre_grafico>.*) *\}", r"Gráfico \g<nombre_grafico>", codigo)
	return codigo

#Extrae los titulos del código LaTeX
def titulos(codigo):
	codigo = re.sub(r"\\frametitle\{(?P<titulo>.*)\}", r"\g<titulo>\n", codigo)
	codigo = re.sub(r"\\framesubtitle\{(?P<titulo>.*)\}", r"\g<titulo>\n", codigo)
	codigo = re.sub(r"\\begin\{block\}\{(?P<titulo_bloque>.*)\}", r"\g<titulo_bloque>\n", codigo)
	codigo = re.sub(r"\\begin\{frame\}.*\{*(?P<titulo_cuadro>.*)\}*", r"\g<titulo_cuadro>\n", codigo)
	return codigo

def enumeracion(codigo):
	codigo = re.sub(r'\\item\s*\[(?P<texto>[^\[]*)\]\s*', r'\g<texto>\t', codigo)
	cont = list()
	codigo2=''
	lines_codigo=codigo.split('\n')
	for line in lines_codigo:
		if "\\begin{enumerate}" in line:
			cont.append(1)
			itemize = 0
		if "\\end{enumerate}" in line: cont.remove(cont[-1])
		# Verificando que solo se reemplace item de itemize/description y no de enumerate
		if cont != list() and "\\begin{itemize}" in line: itemize+=1
		if cont != list() and "\\end{itemize}" in line: itemize=itemize-1
		if cont != list() and "\\begin{description}" in line: itemize+=1
		if cont != list() and "\\end{description}" in line: itemize=itemize-1
		if cont != list() and "\\item" in line and itemize==0:
			if len(cont)==1: numero=str(cont[-1])
			if len(cont)==2: numero=str(numeracion['2'][cont[-1]])
			if len(cont)==3: numero=str(numeracion['3'][cont[-1]])
			line = re.sub(r'\\item', r''+numero+'.\tblindtexenumeracion', line)
			cont[-1] += 1
		codigo2+=line+'\n'
	codigo=codigo.replace(codigo, codigo2)
	codigo = re.sub(r'blindtexenumeracion\s*', r'', codigo)
	codigo = re.sub(r'\\item\s*\[(?P<texto>[^\[]*)\]\s*', r'\g<texto>\t', codigo)
	codigo = re.sub(r'\\item\s*', r'•\t', codigo)
	for i in limpiar['enumeracion']: codigo=codigo.replace(i[0], i[1])
	return codigo

def split_codigo(codigo):
	codigo_splited=codigo.split('\n')
	codigo2=''
	for i in codigo_splited: codigo2+=i.strip()+'\n'
	return codigo2

#Elimina código de formato y otros en el archivo, para que estos no se muestren en el texto final
def limpiar_basura(codigo):
	codigo=codigo.replace('blindtexpesoblindtex', '$')
	codigo = re.sub(r'\{ *\\large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{ *\\LARGE *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{ *\\Large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\begin *\{ *textblock *\*? *\}.*', r'', codigo)
	codigo = re.sub(r'\\end *\{ *textblock *\*? *\}', r'', codigo)
	codigo = re.sub(r'\\begin *\{ *minipage *\}.*', r'', codigo)
	codigo = re.sub(r'\\end *\{ *minipage *\}', r'', codigo)
	codigo = re.sub(r'\\setcounter *\{ *enumi *\} *\{ *\d* *\}', r'', codigo)
	codigo = re.sub(r'\\thispagestyle *\{.*\}', r'', codigo)
	codigo = re.sub(r'\\begin *\{ *multicols *\} *\{ *\d* *\}', r'', codigo)
	codigo = re.sub(r'\\.space *\{[^\{\}]*[a-z]+\}', r'', codigo)
	for _ in range(3):
		codigo=sub_avanzado(r'\\only *< *[\d-]* *> *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada('\\\\only *< *[\d-]* *> *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\scshape *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\scshape *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\small *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\small *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\small *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\small *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\[a-z]box *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\[a-z]box *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\[a-z]box *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\[a-z]box *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\text\w* *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\text\w* *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\text\w* *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\text\w* *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\emph *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\emph *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\emph *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\emph *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\large *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\large *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\large *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\large *\{.*\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\{ *\\hfill *\{(?P<texto>.*)\} *\}', r'\g<texto>', busqueda_avanzada(r'\{ *\\hfill *\{.*\} *\}', codigo, ('{', '}')), codigo)
		codigo=sub_avanzado(r'\\hfill *\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada(r'\\hfill *\{.*\}', codigo, ('{', '}')), codigo)
	codigo=split_codigo(codigo)
	codigo=re.sub(r'\n{2,}', r'blindtexlineasblindtex', codigo)
	codigo = re.sub(r'(?P<caracter1>[^\}\\])\n(?P<caracter2>[^\\])', '\g<caracter1> \g<caracter2>', codigo)
	codigo=re.sub(r'(?P<ecuacion>blindtexecuacion\d+blindtexecuacion)', r'\n\g<ecuacion>\n', codigo)
	codigo=codigo.replace('blindtexlineasblindtex', '\n\n')
	codigo=re.sub(r'\\hypertarget *\{[^\{\}]*\} *\{\s*\n*\s*(?P<texto>\\[sub]*section *\{.*\} *\\label *\{.*\}) *\}', r'\g<texto>', codigo)
	for i in limpiar['delimitadores']: codigo=codigo.replace(i[0], i[1])
	for i in limpiar['simples']: codigo=codigo.replace(i[0], i[1])
	codigo=codigo.strip()
	codigo=split_codigo(codigo)
	return codigo

def traducido(codigo, nombre_archivo):
	final=open(nombre_archivo, 'w')
	final.write(codigo)
	final.close()

