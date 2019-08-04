#-*-:coding:utf-8-*-
import re
import blindtex
from blindtex import tex2all
import codecs

basura = open('/mnt/d/latextranslator/basura.json', 'r+', encoding='utf-8')
limpiar=''
while True:
	lines = basura.readlines()
	if not lines: break
	for line in lines: limpiar+=line
basura.close()
limpiar=eval(limpiar)

numeracion={
	'2': ('0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
	'3': ('0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX')
}

#Funciones de transformación de texto básico.
#Transforma el Archivo en un string y quíta lo que está antes de \begin{document} y lo siguiente a \end{document}
def string(nombre_archivo, hijo):
	archivo = open(nombre_archivo, 'r+', encoding='utf-8')
	codigo = ''

	dentro_documento = False
	if hijo == True:
		dentro_documento = True
	enumerado = False
	cont = list()
	while True:
		lines = archivo.readlines()
		if not lines: break
		macros=list()
		teoremas=list()
		for line in lines:
			if "\\begin{document}" in line: dentro_documento = True
			if "\\title" in line: dentro_documento = True
			if "\\author" in line: dentro_documento = True
			if "\\date" in line: dentro_documento = True
			if "\\fancy" in line: dentro_documento = True
			if "\\end{document}" in line: dentro_documento = False
			if dentro_documento == True: 
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
				if line.strip() == '':
					codigo += line
				elif line.strip()[0] != "%":
					if '%' not in line:
						codigo += line
					else:
						linea=''
						caracter_especial=False
						for caracter in line:
							if caracter_especial==False and caracter=='%': break
							linea+=caracter
							if caracter_especial==True: caracter_especial=False
							if caracter=='\\': caracter_especial=True
						codigo+=linea
			else:
				patronmacros=re.compile(r'\\newcommand\{\\(?P<nuevocomando>.*)\}\{\\(?P<comando>.*)\}')
				patronteoremas=re.compile(r'\\newtheorem\{(?P<nuevoteorema>.*)\}.*\{(?P<teorema>.*)\}')
				macros+=patronmacros.findall(line)
				teoremas+=patronteoremas.findall(line)
	archivo.close()
	macros=set(macros)
	macros=list(macros)
	macros.sort(key=len)
	macros.reverse()
	teoremas=set(teoremas)
	teoremas=list(teoremas)
	teoremas.sort(key=len)
	teoremas.reverse()
	for macro in macros: codigo=re.sub(r'\\'+macro[0]+'(?P<caracter>[^a-zA-Z])', r'\\'+macro[1]+'\g<caracter>', codigo)
	for teorema in teoremas: codigo=re.sub(r'\\begin\{'+teorema[0]+'\}(.*\[(?P<teorema>.*)\])*', r''+teorema[1]+': \g<teorema>', codigo)
	for teorema in teoremas: codigo=codigo.replace('\\end{'+teorema[0]+'}', '')
	return codigo

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

#Traduce todas las fórmulas

def formulas(codigo):

	#Busca los patrones entre "$"
	global patron
	patron= re.compile("\$+(?P<formula>[^\$]*)\$+")
	#Busca los patrones que comienzan con "begin equation"
	patron2="\\\\begin\{equation\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{equation\**\}"
	#Busca los patrones que comienzan con "begin align"
	patron3="\\\\begin\{align\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{align\**\}"
	patron4="\\\\begin\{eqnarray\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{eqnarray\**\}"
	#Crea una lista "forms" con los resultados de las dos busquedas anteriores
	forms=patron.findall(codigo)+busqueda_avanzada(patron2, codigo)+busqueda_avanzada(patron3, codigo)+busqueda_avanzada(patron4, codigo)
	if '#symbolab' in codigo:
		codigo = ''
		for i in forms:
			codigo = codigo+'$'+i+'$\n'
	#Se ajusta el formato de la lista de salida
	forms=set(forms)
	forms=list(forms)
	forms.sort(key=len)
	forms.reverse()

	#Se comienza con la lectura de los resultados guardados en forms 
	for i in forms:
		#utiliza blindtex para traducir los patrones encontrados anteriormente, reemplazandolos en el archivo original
		try:
			j=i
			j=re.sub(r' {2,}', r' ', j)
			j=j.replace('\\:', 'blindtexespacio')
			j=j.replace('\%', 'blindtexporciento')
			j=j.replace('\%', '')
			j=j.replace('|', 'blindtexbarravertical')
			j=j.replace('#', 'blindtexsignonumero')
			j=j.replace('~', 'blindtextilde')
			j=j.replace('?', 'blindtexcierrainterrogacion')
			j=j.replace('¿', 'blindtexabreinterrogacion')
			j=j.replace('\\ ', '')
			j=j.replace('\\[', '[')
			j=j.replace('−', '-')
			j=j.replace('\n', 'blindtexlinea')
			j = re.sub(r'\\[a-z]space\{[^\{]*m\}', r'', j)
			j=j.replace("\\pause", "")
			j=j.replace("\\medskip", "")
			j=j.replace("\\bigskip", "")
			j=j.replace('\\smallskip', '')
			j=j.replace('\\displaystyle', '')
			j=j.replace('\\limits', '')
			j = re.sub(r'\\not *\\in', r'\\notin', j)
			j=j.replace('\\therefore', 'blindtextherefore')
			j = re.sub(r'\\math[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', j)
			j = re.sub(r'\\bm\{(?P<texto>[^\{]*)\}', r'\g<texto>', j)
			j = re.sub(r'\\begin\{aligned\}\[[a-z]\]', '', j)
			j=j.replace('\\end{aligned}', '')
			j=j.replace('á', 'blindtexatilde')
			j=j.replace('é', 'blindtexetilde')
			j=j.replace('í', 'blindtexitilde')
			j=j.replace('ó', 'blindtexotilde')
			j=j.replace('ú', 'blindtexutilde')
			x=blindtex.tex2all.read_equation(j)
			x = x.replace("arreglo element1_1 b l i n d t e x l i n e a ","blindtexarregloblindtex")
			x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a ', r'blindtexarreglolineablindtex', x)
			x = re.sub(r'element[0-9]*_[0-9]*', r'blindtexarreglocomablindtex', x)
			if 'blindtexarreglocomablindtex = blindtexarreglocomablindtex' in x:
				x = x.replace('blindtexarreglolineablindtex', '\n')
				x = x.replace("blindtexarregloblindtex","")
				x = x.replace("blindtexarreglocomablindtex","")
				x = re.sub(r' *(b l i n d t e x l i n e a)* *finArreglo', r'', x)
				x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a finArreglo', r'', x)
			else:
				x = x.replace('blindtexarreglolineablindtex', '),\n(')
				x = x.replace("blindtexarregloblindtex","((")
				x = x.replace("blindtexarreglocomablindtex",",")
				x = re.sub(r' *(b l i n d t e x l i n e a)* *finArreglo', r'))', x)
				x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a finArreglo', r'))', x)
			patrontextos= re.compile("ç(?P<texto>[^ç]*)endtext", re.MULTILINE)
			textos=patrontextos.findall(x)
			textos=set(textos)
			textos=list(textos)
			textos.sort(key=len)
			textos.reverse()
			for texto in textos:
				texto2=texto.replace('&', 'blindtex&')
				texto2=texto.replace(' ', 'blindtexespacio')
				x=x.replace(texto, texto2)
			x=x.replace(' ', '')
			x=x.replace('ç', ' ')
			x=x.replace('endtext', ' ')
			x=x.replace('linebreak', '')
			x=x.replace('blindtexespacio', ' ')
			x=x.replace('blindtexporciento', '%')
			x=x.replace('blindtexbarravertical', '|')
			x=x.replace('blindtexsignonumero', '#')
			x=x.replace('blindtextilde', '~')
			x=x.replace('blindtexcierrainterrogacion', '?')
			x=x.replace('blindtexabreinterrogacion', '¿')
			x=x.replace('blindtexatilde', 'á')
			x=x.replace('blindtexetilde', 'é')
			x=x.replace('blindtexitilde', 'í')
			x=x.replace('blindtexotilde', 'ó')
			x=x.replace('blindtexutilde', 'ú')
			x=x.replace('&', '')
			x=x.replace('blindtex&', '&')
			x=x.replace('blindtextherefore', '∴')
			x=x.replace('blindtexlinea', '\n')
			#x=re.sub(r'\^\((?P<exponente>.)\)(?P<siguiente>[^a-zA-Z0-9])', r'^\g<exponente>\g<siguiente>', x)
			x=re.sub(r'\^\((?P<exponente>.)\)', r'^\g<exponente>', x)
			codigo=codigo.replace(i, x)
		except:
			pass
	return codigo

#Se deshace de los graficos encontrados en el codigo LaTeX
def graficos(codigo):
	codigo = re.sub(r"\\includegraphics\[(?P<tiende>.*)\]\{(?P<nombre_grafico>.*)\}", r"#################################################################\n#					  DESCRIBIR GRÁFICO					   #	 NOMBRE DEL GRÁFICO: '  \g<nombre_grafico>  '\n#################################################################\n", codigo)
	return codigo

#Extrae los titulos del código LaTeX
def titulos(codigo):
	codigo = re.sub(r"\\frametitle\{(?P<titulo>.*)\}", r"\g<titulo>", codigo)
	codigo = re.sub(r"\\framesubtitle\{(?P<titulo>.*)\}", r"\g<titulo>", codigo)
	codigo = re.sub(r"\\begin\{block\}\{(?P<titulo_bloque>.*)\}", r"\g<titulo_bloque>", codigo)
	codigo = re.sub(r"\\begin\{frame\}.*\{*(?P<titulo_cuadro>.*)\}*", r"\g<titulo_cuadro>", codigo)
	return codigo

#Elimina código de formato y otros en el archivo, para que estos no se muestren en el texto final
def limpiar_basura(codigo):
	for i in limpiar['delimitadores']: codigo=codigo.replace(i[0], i[1])
	codigo = re.sub(r'\{\\large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{\\LARGE *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{\\Large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\text[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\begin\{textblock\*?\}\{[\d,.-]*\\textwidth\}\[*[\d,.-]*\]*\([\d,.-]*cm,[\d,.-]*cm\)', r'', codigo)
	codigo = re.sub(r'\\end\{textblock\*?\}', r'', codigo)
	codigo = re.sub(r'\\begin\{minipage\}.*', r'', codigo)
	codigo = re.sub(r'\\end\{minipage\}', r'', codigo)
	codigo = re.sub(r'\\end\{minipage\}', r'', codigo)
	codigo = re.sub(r'\\setcounter\{enumi\}\{\d*\}', r'', codigo)
	codigo = re.sub(r'\\thispagestyle\{.*\}', r'', codigo)
	codigo = re.sub(r'\\begin\{multicols\}\{\d*\}', r'', codigo)
	codigo=re.sub(patron, '\g<formula>', codigo)
	codigo=re.sub("\\\\begin\{equation\**\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{equation\**\}", "", codigo)
	codigo=re.sub("\\\\begin\{align\**\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{align\**\}", "", codigo)
	codigo=re.sub("\\\\begin\{eqnarray\*?\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{eqnarray\**\}", "", codigo)
	codigo = re.sub(r'\\.space\{[^\{]*m\}', r'', codigo)
	codigo = re.sub(r'\\hfill\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\emph\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\only<[\d-]*>\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'blindtexenumeracion\s*', r'', codigo)
	codigo = re.sub(r'\\item\s*\[(?P<texto>[^\[]*)\]\s*', r'\g<texto>\t', codigo)
	codigo = re.sub(r'\\item\s*', r'•\t', codigo)
	codigo=sub_avanzado(r'\\only<[\d-]*>\{(?P<texto>.*)\}', r'\g<texto>', busqueda_avanzada('\\\\only<[\d-]*>\{.*\}', codigo, ('{', '}')), codigo)
	codigo=sub_avanzado(r'\n\{*\\small\{(?P<texto>.*?)\}+', r'\g<texto>', busqueda_avanzada(r'\n\{*\\small\{.*?\}+', codigo, ('{', '}')), codigo)
	for i in limpiar['simples']: codigo=codigo.replace(i[0], i[1])
	for i in limpiar['acentos']: codigo=codigo.replace(i[0], i[1])
	codigo = re.sub(r'\n +\n', '\n\n', codigo)
	codigo = re.sub(r'\n\t*\n', '\n\n', codigo)
	codigo = re.sub(r'^\s+$|(\n\n)+', '\n', codigo)
	codigo=codigo.replace('\n', '\r\n')
	return codigo

def nombre_final(nombre_archivo):
	cont=0
	final=""
	for i in nombre_archivo:
		if cont < len(nombre_archivo)-4: final+=i
		cont+=1
	return final

def traducido(codigo, nombre_archivo):
	final=open(nombre_archivo, 'w')
	final.write(codigo)
	final.close()


