#-*-:coding:utf-8-*-
import re
import blindtex
from blindtex import tex2all
import codecs

#Funciones de transformación de texto básico.

#Transforma el Archivo en un string y quíta lo que está antes de \begin{document} y lo siguiente a \end{document}
def string(nombre_archivo):
	archivo = open(nombre_archivo, 'r+', encoding='utf-8')
	codigo = ''

	dentro_documento = False
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
				# Verificando que solo se reemplace item de itemize y no de enumerate
				if cont != list() and "\\begin{itemize}" in line: itemize+=1
				if cont != list() and "\\end{itemize}" in line: itemize=itemize-1
				if cont != list() and "\\item" in line and itemize==0:
					line = re.sub(r'\\item', r''+str(cont[-1])+'.\tblindtexenumeracion', line)
					cont[-1] += 1
				codigo += line
	return codigo

#Traduce todas las fórmulas

def formulas(codigo):
	patron= re.compile("\$+(?P<formula>[^\$]*)\$+")
	patron2=re.compile("\\\\begin\{equation\}.*\s*(?P<formula>.*)\s*\\\\end\{equation\}")
	forms=patron.findall(codigo)+patron2.findall(codigo)
	forms=set(forms)
	forms=list(forms)
	forms.sort(key=len)
	forms.reverse()
	for i in forms:
	
		try:
			j=i
			j=j.replace('%', 'blindtexporciento')
			j=j.replace('|', 'blindtexbarravertical')
			j=j.replace('#', 'blindtexsignonumero')
			#j=j.replace(' ', '')
			j=j.replace('\\ ', '')
			j=j.replace('\\[', '[')
			j=j.replace('−', '-')
			j=j.replace('\n', 'blindtexlinea')
			j = re.sub(r'\\.space\{[^\{]*m\}', r'', j)
			j=j.replace("\\medskip", "")
			j=j.replace("\\bigskip", "")
			j=j.replace('\\smallskip', '')
			j=j.replace('\\displaystyle', '')
			j = re.sub(r'\\math[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', j)
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
				espacios=texto.replace(' ', 'blindtexespacio')
				print(espacios)
				x=x.replace(texto, espacios)
			x=x.replace(' ', '')
			x=x.replace('ç', ' ')
			x=x.replace('endtext', ' ')
			x=x.replace('blindtexespacio', ' ')
			x=x.replace('blindtexporciento', '%')
			x=x.replace('blindtexbarravertical', '|')
			x=x.replace('blindtexsignonumero', '#')
			x=x.replace('blindtexlinea', '\n')
			codigo=codigo.replace(i, x)
		except:
			pass
	return codigo

def graficos(codigo):
	patron = re.compile(r"\\includegraphics\[(?P<tiende>.*)\]\{(?P<nombre_grafico>.*)\}")
	codigo = re.sub(patron, r"#################################################################\n#					  DESCRIBIR GRÁFICO					   #	 NOMBRE DEL GRÁFICO: '  \g<nombre_grafico>  '\n#################################################################\n", codigo)
	return codigo

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

def basura(codigo):
	codigo = re.sub(r"(?<![\\])\$", r"", codigo)
	codigo = codigo.replace("\\begin{document}","")
	codigo = codigo.replace("\\titlepage", "")
	codigo = codigo.replace("\\begin{frame}","")
	codigo = codigo.replace("\\end{frame}", "")
	codigo = codigo.replace("\\end{block}", "")
	codigo = codigo.replace("\\begin{center}", "")
	codigo = codigo.replace("\\end{center}", "")
	codigo = codigo.replace("\\newpage", "")
	codigo = codigo.replace("\\medskip", "")
	codigo = codigo.replace("\\bigskip", "")
	codigo = codigo.replace('\\smallskip', '')
	codigo = codigo.replace('\\large', '')
	codigo = codigo.replace("\\pause", "")
	codigo = re.sub(r'\%*', '', codigo)
	codigo = re.sub(r'\\text[a-z]*\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
	codigo = re.sub(r'\{\\large (?P<texto>.*)\}', r'\g<texto>', codigo)
	codigo=re.sub(r"\\\\begin\{equation\}.*\s*(?P<formula>.*)\s*\\\\end\{equation\}", r'\g<formula>', codigo)
	codigo=re.sub(r"\\\\begin\{equation\}.*\s*", '', codigo)
	codigo=codigo.replace('\\end{equation}', '')
	codigo=codigo.replace('\\begin{equation}', '')
	codigo = re.sub(r'\\.space\{[^\{]*m\}', r'', codigo)
	codigo = re.sub(r'\\hfill\{(?P<texto>[^\{]*)\}', r'\g<texto>', codigo)
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
	#codigo = re.sub(r'\$[^\$]*\n', r'\n', codigo)

	#Revisar
	codigo = codigo.replace("\\begin{itemize}", "")
	codigo = codigo.replace("\\begin{enumerate}", "")
	codigo = re.sub(r'blindtexenumeracion\s*', r'', codigo)
	codigo = re.sub(r'\\item\s*', r'•\t', codigo)
	codigo = codigo.replace("\\end{itemize}", "")
	codigo = codigo.replace("\\end{enumerate}", "")
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


