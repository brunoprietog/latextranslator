from test_helper import *

def test_advance_search():
    archive_tex = """
    \\date{Septiembre 2018}
    """
    resultado = busqueda_avanzada(r"\\date *\{(?P<texto>.*)\}",archive_tex)
    assert resultado == ['Septiembre 2018']

def test_advance_search_2():
    archive_tex = """
    \\title{La Diferencial}
    \\author{Verónica Brice\\~no V.}
    \\date{septiembre 2018}
    """
    resultado = busqueda_avanzada(r"\\author *\{(?P<texto>.*)\}",archive_tex, ('{', '}'))
    assert resultado == ['Verónica Brice\\~no V.']


def test_advance_search_3():
    archive_tex = """
    \\section{Introducción}
    \\subsection{El cierre llave es\\}}
    """
    resultado = busqueda_avanzada(r"\\subsection\{(?P<texto>.*)\}", archive_tex, ('{', '}'))
    assert resultado == ['El cierre llave es\\}']

def test_advance_search_4():
    archive_tex = """
    \\date{\\em{Septiembre del año 2018}}
    \\date{\\em{Septiembre 2018}}
    \\date{Septiembre 2018}
    """
    resultado = busqueda_avanzada(r"\\date *\{(?P<texto>.*)\}", archive_tex, ('{', '}'))
    print(resultado)
    assert resultado == ['\\em{Septiembre del año 2018}', '\\em{Septiembre 2018}', 'Septiembre 2018']

def test_advance_search_5():
    archive_tex = """
    \\subsection*{Sin numeración}
    """
    resultado = busqueda_avanzada(r"\\subsection\*\{(?P<texto>.*)\}", archive_tex, ('{', '}'))
    assert resultado == ['Sin numeración']


# def test_busqueda_avanzada6():
#     archive_tex = """
#     \\date{\\em{Septiembre 2018}}
#     \\date{\\em{Septiembre 2018}}
#     \\date{Septiembre 2018}
#     """
#     resultado = busqueda_avanzada(r"\\date *\{(?P<texto>.*)\}", archive_tex, ('{', '}'))
#     print(resultado)
#     assert resultado == ['\\em{Septiembre 2018}', '\\em{Septiembre 2018}', 'Septiembre 2018']