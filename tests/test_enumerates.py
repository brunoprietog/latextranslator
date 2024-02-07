from test_helper import *

def test_enumerates():
    text_archive = """\\begin{enumerate}\n\\item cosa_1\n\\item cosa_2\n\\end{enumerate}"""
    result = enumeracion(text_archive)
    assert result == "\n1.\tcosa_1\n2.\tcosa_2\n\n"

def test_enumerates_2():
    text_archive = "\\begin{itemize}\n\\item Un elemento de lista largo\n\\item Otro elemento muy largo\n\\end{itemize}"
    result = enumeracion(text_archive)
    assert result == "\n•\tUn elemento de lista largo\n•\tOtro elemento muy largo\n\n"

def test_enumerates_3():
    text_archive = "\\begin{enumerate}\n\\item cosa_1\n\\item cosa_2\n\\end{enumerate}\n\\begin{enumerate}\n\\item cosa_3\n\\item cosa_4\n\\end{enumerate}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tcosa_1\n2.\tcosa_2\n\n\n1.\tcosa_3\n2.\tcosa_4\n\n"

def test_enumerates_4():
    text_archive = "\\begin{enumerate}\n\\item cosa_1\n\\item cosa_2\n\\end{enumerate}\n\\begin{itemize}\n\\item cosa_3\n\\item cosa_4\n\\end{itemize}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tcosa_1\n2.\tcosa_2\n\n\n•\tcosa_3\n•\tcosa_4\n\n"

def test_enumerates_5():
    text_archive = "\\begin{enumerate}\n\\item cosa_1\n\\item cosa_2\n\\end{enumerate}\n\\begin{enumerate}\n\\item cosa_3\n\\item cosa_4\n\\end{enumerate}\n\\begin{itemize}\n\\item cosa_5\n\\item cosa_6\n\\end{itemize}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tcosa_1\n2.\tcosa_2\n\n\n1.\tcosa_3\n2.\tcosa_4\n\n\n•\tcosa_5\n•\tcosa_6\n\n"

def test_enumerates_6():
    text_archive = "\\begin{enumerate}\n\\item cosa_1\n\\item cosa_2\n\\end{enumerate}\n\\begin{itemize}\n\\item cosa_3\n\\item cosa_4\n\\end{itemize}\n\\begin{enumerate}\n\\item cosa_5\n\\item cosa_6\n\\end{enumerate}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tcosa_1\n2.\tcosa_2\n\n\n•\tcosa_3\n•\tcosa_4\n\n\n1.\tcosa_5\n2.\tcosa_6\n\n"

def test_enumerates_7():
    text_archive = "\\begin{enumerate}\n\\item Primer elemento\n\\begin{enumerate}\n\\item Subelemento 1\n\\item Subelemento 2\n\\end{enumerate}\n\\item Segundo elemento\n\\end{enumerate}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tPrimer elemento\n\nA.\tSubelemento 1\nB.\tSubelemento 2\n\n2.\tSegundo elemento\n\n"

def test_enumerates_8():
    text_archive = "\\begin{enumerate}\n\\item Primer elemento\n\\begin{enumerate}\n\\item Subelemento 1\n\\item Subelemento 2\n\\begin{enumerate}\n\\item Subsubelemento 1\n\\item Subsubelemento 2\n\\end{enumerate}\n\\end{enumerate}\n\\item Segundo elemento\n\\end{enumerate}\n\\begin{enumerate}\n\\item Tercer elemento\n\\item Cuarto elemento\n\\end{enumerate}"
    result = enumeracion(text_archive)
    assert result == "\n1.\tPrimer elemento\n\nA.\tSubelemento 1\nB.\tSubelemento 2\n\nI.\tSubsubelemento 1\nII.\tSubsubelemento 2\n\n\n2.\tSegundo elemento\n\n\n1.\tTercer elemento\n2.\tCuarto elemento\n\n"