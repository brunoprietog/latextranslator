from test_helper import *

# Test case to '\frametitle'
def test_titles():
    text_archive = "\\frametitle{Título de la diapositiva 1}"
    result = titulos(text_archive)
    assert result == "Título de la diapositiva 1\n"

# Test case to '\frametitle with \frametitle'
def test_titles_2():
    text_archive = "\\frametitle{\\frametitle\\frametitle}"
    result = titulos(text_archive)
    assert result == "\\frametitle\\frametitle\n"

# Test case to '\frametitle with content'
def test_titles_3():
    text_archive = """\\frametitle{Título de la diapositiva}\nEste es el contenido de la diapositiva."""
    result = titulos(text_archive)
    print(result)
    assert result == "Título de la diapositiva\n\nEste es el contenido de la diapositiva."

# Test case to '\begin{block}'
def test_titles_4():
    text_archive = "\\begin{block}{Título del bloque}\nContenido del bloque.\n\\end{block}"
    result = titulos(text_archive)
    print(result)
    assert result == "Título del bloque\n\nContenido del bloque.\n"

# Caso de prueba para '\begin{frame}'
def test_titles_5():
    text_archive = "\\begin{frame}{Título del cuadro}\nContenido del cuadro.\n\\end{frame}"
    result = titulos(text_archive)
    assert result == "Título del cuadro\n\nContenido del cuadro.\n"

# Caso de prueba para '\begin{frame}'
def test_titles_6():
    text_archive = "\\begin{frame}{Título del cuadro}\nContenido del cuadro.\n\\begin{itemize}\n\\item{Im an item}\\end{itemize}\\n\\end{frame}"
    result = titulos(text_archive)
    assert result == "Título del cuadro\n\nContenido del cuadro.\n\\begin{itemize}\n\\item{Im an item}\\end{itemize}\\n"


def test_titles_7():
    text_archive = "\\begin{block}{Título del cuadro}\nContenido del cuadro.\n\\begin{itemize}\n\\item{Im a beautifull item}\\end{itemize}\\n\\end{block}"
    result = titulos(text_archive)
    assert result == "Título del cuadro\n\nContenido del cuadro.\n\\begin{itemize}\n\\item{Im a beautifull item}\\end{itemize}\\n"


def test_titles_8():
    text_archive = "\\begin{block}{Título del cuadro}\nContenido del cuadro.\n\\end{block}\n\\begin{block}{Título del cuadro número 2}\nContenido del cuadro 2.\n\\end{block}"
    result = titulos(text_archive)
    assert result == "Título del cuadro\n\nContenido del cuadro.\n\nTítulo del cuadro número 2\n\nContenido del cuadro 2.\n"

# Caso de prueba para múltiples ocurrencias
def test_titles_9():
    text_archive = "\\frametitle{Título 1}\nContenido 1.\n\\frametitle{Título 2}\nContenido 2."
    result = titulos(text_archive)
    assert result == "Título 1\n\nContenido 1.\nTítulo 2\n\nContenido 2."

# Caso de prueba para un código sin patrones
def test_titles_10():
    text_archive = "Este es un código sin patrones de título."
    result = titulos(text_archive)
    assert result == "Este es un código sin patrones de título."