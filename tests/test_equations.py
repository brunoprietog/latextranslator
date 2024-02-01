from test_helper import *

# Caso de prueba con límite
def test_equation():
    formulas = ["$\\lim_{x \\to 0} \\frac{1}{x}$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["lim_(x→0)(1/x)"]

def test_equation_2():
    formulas = ["$f'(a)  \\sim \\frac{f(x) - f(a)}{x-a}$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["f'(a)∼(f(x)−f(a))/(x−a)"]

def test_equation_3():
    formulas = ["$E=mc^2$", "$a^2 + b^2 = c^2$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["E=mc^2", "a^2+b^2=c^2"]

def test_equation_4():
    formulas = ["$\\int_{0}^{1} x^2 dx$", "$\\sum_{n=1}^{5} \\frac{1}{n}$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∫[0, 1] x^2dx", "∑[n=1, 5] (1/n)"]

def test_equation_5():
    formulas = ["$\\lim_{x\\to\\infty} \\frac{1}{x}=0$", "$\\sqrt{9}=3$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["lim_(x→∞)(1/x)=0", "√9=3"]

def test_equation_6():
    formulas = ["$\\int_{0}^{5} x^2 + \\sqrt{x} * \\frac{1}{x} dx$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∫[0, 5] x^2+√x*(1/x)dx"]

def test_equation_7():
    formulas = ["$\\Sigma_{i=1}^{n} a_i$", "$\\int_{a}^{b} \\frac{1}{\\sqrt{x}} dx$", "$\\sqrt{x+1}$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["Σ^n_(i=1)a_i", "∫[a, b] (1)/(√x)dx", "√(x+1)"]

def test_equation_8():
    formulas = ["$\\nabla\\cdot\\vec{F}$", "$A\\cup B$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∇·F⃗", "A∪B"]

def test_equation_9():
    formulas = ["$\\forall x, \\exists y : P(x, y)$", "$\\neg (A \\land B)$", "$\\mathcal{L}(x)$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∀x,∃y: P(x,y)", "¬(A∧B)", "L(x)"]

def test_equation_10():
    formulas = ["$\\psi(\\theta) = A\\sin(\\theta) + B\\cos(\\theta)$", "$f''(x) + f(x) = 0$", "$\\partial F/\\partial t$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["ψ(θ)=Asin(θ)+Bcos(θ)", "f''(x)+f(x)=0", "∂F÷∂t"]

def test_equation_11():
    formulas = ["$\\Phi(x) \\leftrightarrow \\exists y : Q(y)$", "$\\alpha, \\beta, \\gamma$", "$\\Delta x = \\frac{b-a}{n}$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["Φ(x)↔∃y: Q(y)", "α,β,γ", "∆x=(b−a)/(n)"]

def test_equation_12():
    formulas = ["$x_(i+1)^{n}$", "$A\\subset B$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["x_(i+1)^n", "A⊂B"]

def test_equation_13():
    formulas = ["$\\sum_{n=1}^{\\infty} \\lim_{{x\\to\\infty}} f_n(x)$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∑[n=1, ∞] lim_(x→∞)f_n(x)"]
    
def test_equation_14():
    formulas = ["$\\sum_{n=1}^{\\infty}$", "$\\lim_{{x\\to\\infty}}$", "$f_n(x)$"]
    resultado = traducir_formulas(formulas)
    assert resultado == ["∑[n=1, ∞] ", "lim_(x→∞)", "f_n(x)"]
