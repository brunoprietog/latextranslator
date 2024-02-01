from test_helper import *

def reading_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# test string to delete all comments
def test_string():
    text_archive = "fixtures/comments.tex"
    result = string(text_archive, False)
    assert result == reading_file("fixtures/comments_fixed.tex")

def test_string_2():
    text_archive = "fixtures/macros.tex"
    result = string(text_archive, False)
    print(result)
    assert result == reading_file("fixtures/macros_fixed.tex")
