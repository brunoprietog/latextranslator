from latextranslator.translator import titulos

codigo = """

Este es el contenido de la diapositiva 1.
\\frametitle{Título de la diapositiva 2}
Este es el contenido de la diapositiva 2.
"""

def test_titulos_1():
    assert titulos("\\frametitle{Título de la diapositiva 1}") == "Título de la diapositiva 1\n"

def test_titulos_2():
    assert titulos("\\frametitle{\\frametitle\\frametitle}") == "\\frametitle\\frametitle\n"

# Caso de prueba para '\frametitle'
def test_frametitle():
    codigo = "\\frametitle{Título de la diapositiva}\nEste es el contenido de la diapositiva."
    resultado = titulos(codigo)
    assert resultado == "Título de la diapositiva\n\nEste es el contenido de la diapositiva."

# Caso de prueba para '\framesubtitle'
def test_framesubtitle():
    codigo = "\\framesubtitle{Subtítulo de la diapositiva}\nEste es el contenido de la diapositiva."
    resultado = titulos(codigo)
    assert resultado == "Subtítulo de la diapositiva\n\nEste es el contenido de la diapositiva."

# Caso de prueba para '\begin{block}'
def test_begin_block():
    codigo = "\\begin{block}{Título del bloque}\nContenido del bloque.\n\\end{block}"
    resultado = titulos(codigo)
    assert resultado == "Título del bloque\n\nContenido del bloque.\n\\end{block}"

# Caso de prueba para '\begin{frame}'
def test_begin_frame():
    codigo = "\\begin{frame}{Título del cuadro}\nContenido del cuadro.\n\\end{frame}"
    resultado = titulos(codigo)
    assert resultado == "\n\nContenido del cuadro.\n\\end{frame}"

# Caso de prueba para múltiples ocurrencias
def test_multiple_ocurrencias():
    codigo = "\\frametitle{Título 1}\nContenido 1.\n\\frametitle{Título 2}\nContenido 2."
    resultado = titulos(codigo)
    assert resultado == "Título 1\n\nContenido 1.\nTítulo 2\n\nContenido 2."

# Caso de prueba para un código sin patrones
def test_sin_patrones():
    codigo = "Este es un código sin patrones de título."
    resultado = titulos(codigo)
    assert resultado == codigo
