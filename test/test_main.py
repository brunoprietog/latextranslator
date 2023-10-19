import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import translate

def testing_name_1():
    assert translate('john.xd') == False

def testing_name_2():
    assert translate('john.tex.te') == False


