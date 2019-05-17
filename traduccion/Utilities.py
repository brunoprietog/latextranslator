#-*-:coding:utf-8-*-
import re
import blindtex
from blindtex import tex2all
import codecs

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
		if not lines:
			break
		macros=list()
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
					line = re.sub(r'\\item', r''+str(cont[-1])+'.\tblindtexenumeracion', line)
					cont[-1] += 1
				if line.strip() == '':
					codigo += line
				elif line.strip()[0] != "%":
					codigo += line
			else:
				patronmacros=re.compile(r'\\newcommand\{\\(?P<nuevocomando>.*)\}\{\\(?P<comando>.*)\}')
				macros+=patronmacros.findall(line)
	macros=set(macros)
	macros=list(macros)
	macros.sort(key=len)
	macros.reverse()
	for macro in macros:
		codigo=re.sub(r'\\'+macro[0]+'(?P<caracter>[^a-zA-Z])', r'\\'+macro[1]+'\g<caracter>', codigo)
	return codigo

def busqueda_avanzada(patron, texto):
	patron_quitar_grupo=re.compile(r'\(\?P\<\w*\>(?P<grupocontent>.*)\)', re.S)
	string_patron_sin_grupo=re.sub(patron_quitar_grupo, r'\g<grupocontent>', patron)
	patron_sin_grupo=re.compile(r''+string_patron_sin_grupo, re.S)
	encontrados_preliminar=patron_sin_grupo.findall(texto)
	encontrados=list()
	while encontrados_preliminar!=[]:
		for preliminar in encontrados_preliminar:
			if patron_sin_grupo.findall(preliminar)==[]:
				return []
			else:
				patron_reductivo=re.compile(r'(?P<restante>.+)(?P<ultimo>'+string_patron_sin_grupo+')', re.S)
				if len(patron_reductivo.findall(preliminar))==0:
					patron_reductivo=re.compile(r''+string_patron_sin_grupo, re.S)
					reduccion=patron_reductivo.findall(preliminar)[0]
					encontrados.append(reduccion)
					encontrados_preliminar.remove(preliminar)
				else:
					reduccion=patron_reductivo.findall(preliminar)[0]
					encontrados_preliminar.append(reduccion[0])
					encontrados.append(reduccion[1])
					encontrados_preliminar.remove(preliminar)
	encontrados=set(encontrados)
	encontrados=list(encontrados)
	encontrados.sort(key=len)
	encontrados.reverse()
	encontrados_final=list()
	patron_con_grupo=re.compile(patron, re.S)
	for encontrado in encontrados:
		encontrados_final.append(patron_con_grupo.findall(encontrado)[0])
	return encontrados_final


#Traduce todas las fórmulas

def formulas(codigo):

	#Busca los patrones entre "$"
	global patron
	patron= re.compile("\$+(?P<formula>[^\$]*)\$+")
	#Busca los patrones que comienzan con "begin equation"
	global patron2
	#patron2=re.compile("\\\\begin\{equation\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{equation\**\}")
	patron2="\\\\begin\{equation\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{equation\**\}"
	#Busca los patrones que comienzan con "begin align"
	#global patron3
	#patron3=re.compile("(\\\\begin\{align\*?\}.*\s*)(?P<formula>.*)(\s*\\\\end\{align\*?\})$", re.S)
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
			x = x.replace("arreglo element1_1 b l i n d t e x l i n e a ","(")
			x = re.sub(r' b l i n d t e x l i n e a finArreglo', r')', x)
			x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a ', r'),\n(', x)
			x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a finArreglo', r')', x)
			x = re.sub(r'element[0-9]*_[0-9]*', r',', x)
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
			#x=x.replace(' ', '')
			x=x.replace('ç', ' ')
			x=x.replace('endtext', ' ')
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
			x=re.sub(r'\^\((?P<exponente>.)\)(?P<siguiente>[^a-zA-Z0-9])', r'^\g<exponente>\g<siguiente>', x)
			x=re.sub(r'\^\((?P<exponente>.)\)$', r'^\g<exponente>', x)
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
def basura(codigo):
	codigo = codigo.replace("\\begin{document}","")
	codigo = codigo.replace("\\titlepage", "")
	codigo = codigo.replace("\\begin{frame}","")
	codigo = codigo.replace("\\end{frame}", "")
	codigo = codigo.replace("\\end{block}", "")
	codigo = codigo.replace("\\begin{center}", "")
	codigo = codigo.replace("\\end{center}", "")
	codigo = codigo.replace("\\frame[allowframebreaks]", "")
	codigo = codigo.replace("\\framebreak", "")
	codigo = codigo.replace("\\newpage", "")
	codigo = codigo.replace("\\medskip", "")
	codigo = codigo.replace("\\bigskip", "")
	codigo = codigo.replace('\\smallskip', '')
	codigo = codigo.replace('\\small', '')
	codigo = codigo.replace("\\pause", "")
	codigo = codigo.replace("\\quad", "")
	codigo = codigo.replace("\\qquad", "")
	codigo = codigo.replace("\\qed", "")
	codigo = re.sub(r'\%*', '', codigo)
	codigo = re.sub(r'\{\\large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{\\LARGE *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{\\Large *(?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = codigo.replace('\\large', '')
	codigo = codigo.replace('\\LARGE', '')
	codigo = codigo.replace('\\Large', '')
	codigo = re.sub(r'\\text[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\begin\{textblock\*?\}\{[\d,.-]*\\textwidth\}\[*[\d,.-]*\]*\([\d,.-]*cm,[\d,.-]*cm\)', r'', codigo)
	codigo = re.sub(r'\\end\{textblock\*?\}', r'', codigo)
	codigo = re.sub(r'\\begin\{minipage\}.*', r'', codigo)
	codigo = re.sub(r'\\end\{minipage\}', r'', codigo)
	codigo = re.sub(r'\\only<[\d-]*>\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\\setcounter\{enumi\}\{\d*\}', r'', codigo)
	codigo = re.sub(r'\\thispagestyle\{.*\}', r'', codigo)
	codigo = re.sub(r'\\begin\{multicols\}\{\d*\}', r'', codigo)
	codigo=codigo.replace('\\end{multicols}', '')
	codigo=re.sub(patron, '\g<formula>', codigo)
	codigo=re.sub("\\\\begin\{equation\**\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{equation\**\}", "", codigo)
	codigo=re.sub("\\\\begin\{align\**\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{align\**\}", "", codigo)
	codigo=re.sub("\\\\begin\{eqnarray\**\}[^\n]*\s*", "", codigo)
	codigo=re.sub("\s*\\\\end\{eqnarray\**\}", "", codigo)
	codigo=re.sub(patron2, '\g<formula>', codigo)
	#codigo=re.sub(patron3, '\g<formula>', codigo)
	codigo = re.sub(r'\\.space\{[^\{]*m\}', r'', codigo)
	codigo = re.sub(r'\\hfill\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo=codigo.replace('\\hfill', '')
	codigo = re.sub(r'\\emph\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo=codigo.replace('\\bf', '')
	codigo=codigo.replace('\\sf', '')
	codigo=codigo.replace('\\;', ' ')
	codigo=codigo.replace("\\'a", 'á')
	codigo=codigo.replace("\\'e", 'é')
	codigo=codigo.replace("\\'i", 'í')
	codigo=codigo.replace("\\'o", 'ó')
	codigo=codigo.replace("\\'u", 'ú')
	codigo=codigo.replace("\\'{a}", 'á')
	codigo=codigo.replace("\\'{e}", 'é')
	codigo=codigo.replace("\\'{i}", 'í')
	codigo=codigo.replace("\\'{o}", 'ó')
	codigo=codigo.replace("\\'{u}", 'ú')

	#			¿Revisar?
	codigo = codigo.replace("\\begin{itemize}", "")
	codigo = codigo.replace("\\begin{enumerate}", "")
	codigo = codigo.replace("\\begin{description}", "")
	codigo = re.sub(r'blindtexenumeracion\s*', r'', codigo)
	codigo = re.sub(r'\\item\s*\[(?P<texto>[^\[]*)\]\s*', r'\g<texto>\t', codigo)
	codigo = re.sub(r'\\item\s*', r'•\t', codigo)
	codigo = codigo.replace("\\end{itemize}", "")
	codigo = codigo.replace("\\end{enumerate}", "")
	codigo = codigo.replace("\\end{description}", "")
	codigo=codigo.replace('\\\\', '\n')
	codigo = re.sub(r'\n *\n', '\n\n', codigo)
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


