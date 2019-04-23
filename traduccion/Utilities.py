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
		for line in lines:
			if "\\begin{document}" in line: dentro_documento = True
			if "\\title" in line: dentro_documento = True
			if "\\author" in line: dentro_documento = True
			if "\\date" in line: dentro_documento = True
			if "\\fancy" in line: dentro_documento = True
			if "\\begin{enumerate}" in line:
				cont.append(1)
				itemize = 0
			if "\\end{enumerate}" in line: cont.remove(cont[-1])
			if "\\end{document}" in line: dentro_documento = False
			if dentro_documento == True: 
				# Verificando que solo se reemplace item de itemize/description y no de enumerate
				if cont != list() and "\\begin{itemize}" in line: itemize+=1
				if cont != list() and "\\end{itemize}" in line: itemize=itemize-1
				if cont != list() and "\\begin{description}" in line: itemize+=1
				if cont != list() and "\\end{description}" in line: itemize=itemize-1
				if cont != list() and "\\item" in line and itemize==0:
					line = re.sub(r'\\item', r''+str(cont[-1])+'.\tblindtexenumeracion', line)
					cont[-1] += 1
				#line=re.sub("\\\\begin\{align\**\}.*\s*", '$', line)
				#line=re.sub("\s*\\\\end\{align\**\}", '$', line)
				codigo += line
	return codigo

#Traduce todas las fórmulas

def formulas(codigo):

	#Busca los patrones entre "$"
	global patron
	patron= re.compile("\$+(?P<formula>[^\$]*)\$+")
	#Busca los patrones que comienzan con "begin equation"
	global patron2
	patron2=re.compile("\\\\begin\{equation\**\}[^\n]*\s*(?P<formula>.*)\s*\\\\end\{equation\**\}")
	#Busca los patrones que comienzan con "begin align"
	#global patron3
	#patron3=re.compile("(\\\\begin\{align\*?\}.*\s*)(?P<formula>.*)(\s*\\\\end\{align\*?\})$", re.S)
	#Crea una lista "forms" con los resultados de las dos busquedas anteriores
	forms=patron.findall(codigo)+patron2.findall(codigo)
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
			j=j.replace('\\:', 'blindtexespacio')
			j=j.replace('%', 'blindtexporciento')
			j=j.replace('|', 'blindtexbarravertical')
			j=j.replace('#', 'blindtexsignonumero')
			j=j.replace('~', 'blindtextilde')
			j=j.replace('?', 'blindtexcierrainterrogacion')
			j=j.replace('¿', 'blindtexabreinterrogacion')
			j=j.replace('\\ ', '')
			j=j.replace('\\[', '[')
			j=j.replace('−', '-')
			j=j.replace('\n', 'blindtexlinea')
			j=j.replace('\\\\', 'blindtexlinea')
			j = re.sub(r'\\[a-z]space\{[^\{]*m\}', r'', j)
			j=j.replace("\\medskip", "")
			j=j.replace("\\bigskip", "")
			j=j.replace('\\smallskip', '')
			j=j.replace('\\displaystyle', '')
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
			x = re.sub(r'element[0-9]*_1 b l i n d t e x l i n e a ', r'),\n(', x)
			x = re.sub(r' b l i n d t e x l i n e a finArreglo', r')', x)
			x = re.sub(r'element[0-9]*_[0-9]*', r',', x)
			patron= re.compile("ç(?P<texto>[^ç]*)endtext", re.MULTILINE)
			textos=patron.findall(x)
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
			codigo=codigo.replace(i, x)
			forms=forms.remove(i)

		except:
			pass
	print(forms)
	return codigo

#Se deshace de los graficos encontrados en el codigo LaTeX
def graficos(codigo):
	patron = re.compile(r"\\includegraphics\[(?P<tiende>.*)\]\{(?P<nombre_grafico>.*)\}")
	codigo = re.sub(patron, r"#################################################################\n#					  DESCRIBIR GRÁFICO					   #	 NOMBRE DEL GRÁFICO: '  \g<nombre_grafico>  '\n#################################################################\n", codigo)
	return codigo

#Extrae los titulos del código LaTeX
def titulos(codigo):
	patron = re.compile(r"\\frametitle\{(?P<titulo>.*)\}")
	codigo = re.sub(patron, r"\g<titulo>", codigo)
	patron = re.compile(r"\\framesubtitle\{(?P<titulo>.*)\}")
	codigo = re.sub(patron, r"\g<titulo>", codigo)
	patron = re.compile(r"\\begin\{block\}\{(?P<titulo_bloque>.*)\}")
	codigo = re.sub(patron, r"\g<titulo_bloque>", codigo)
	patron = re.compile(r"\\begin\{frame\}\{(?P<titulo_cuadro>.*)\}")
	codigo = re.sub(patron, r"\g<titulo_cuadro>", codigo)
	return codigo

#Elimina código de formato y otros en el archivo, para que estos no se muestren en el texto final
def basura(codigo):
	#codigo=codigo.replace('blindtexformula$', '')
	#codigo=codigo.replace('$blindtexformula', '')
	codigo = re.sub(r"(?<![\\])\$", r"", codigo)
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
	codigo = codigo.replace("\\qed", "")
	codigo = re.sub(r'\%*', '', codigo)
	codigo = re.sub(r'\{\\large (?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo = codigo.replace('\\large', '')
	codigo = re.sub(r'\\text[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	#codigo=re.sub(patron, '\g<formula>', codigo)
	codigo=re.sub(patron2, '\g<formula>', codigo)
	#codigo=re.sub(patron3, '\g<formula>', codigo)
	codigo = re.sub(r'\\.space\{[^\{]*m\}', r'', codigo)
	codigo = re.sub(r'\\hfill\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
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


