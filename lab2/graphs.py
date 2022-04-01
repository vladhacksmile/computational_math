import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def draw_plot(f, value):
    plt.title("График функции")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()

    x = np.linspace(-5, 5, 100)
    y = [f(i) for i in x]

    plt.plot(x, y)

    gca = plt.gca()

    gca.axvline(x=0, color="black")
    gca.axhline(y=0, color="black")

    gca.plot(value, 0, "x")

    plt.show()

def draw_system_plot(f1, f2, value1, value2):
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    equation1 = sp.Eq(f1(x, y), 0)
    equation2 = sp.Eq(f2(x, y), 0)
    points = [{'args': [value1, value2, 'ro']}]
    p = sp.plot_implicit(sp.Or(equation1, equation2), title="График системы", markers=points)