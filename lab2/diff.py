from scipy.misc import derivative

# Метод для вычисления производной N-го порядка
def diff(f, value, n=1):
    return derivative(f, value, 0.0001, n)

# Метод для вычисления частной производной dx
def diff_dx(f, x, y):
    return (f(x + 0.0001, y) - f(x - 0.0001, y)) / (2 * 0.0001)

# Метод для вычисления частной производной dy
def diff_dy(f, x, y):
    return (f(x, y + 0.0001) - f(x, y - 0.0001)) / (2 * 0.0001)