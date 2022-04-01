from prettytable import PrettyTable
from diff import *
from graphs import *
from numpy import sin

funcId = 0

def fun(x):
    if funcId == 2:
        return x ** 3 - x + 4
    elif funcId == 3:
        return x * sin(2 * x)
    else:
        return -2.4 * x ** 3 + 1.27 * x ** 2 + 8.63 * x + 2.31


def f1(x, y):
    return x ** 2 + y ** 2 - 4


def f2(x, y):
    return -3 * x ** 2 + y


def saveResult(table, message):
    print("Сохранить данные в файл <y/n>? В противном случае будет осуществлен выход из программы без сохранения "
          "данных.")
    try:
        s = input()
    except EOFError as e:
        print("EOF triggered")
        return

    if s == "Y" or s == "y":
        try:
            print("Введите название файла:")
            f = open(input(), 'w')
            f.write(table)
            f.write("\n")
            f.write(message)
        except EOFError as e:
            print("EOF triggered")
        except PermissionError as e:
            print("Нет прав на запись!")


# Метод секущих
def solve_secant(a, b, epsilon, digits=3):
    title = ["№", "xk-1", "f(x-1)", "xk", "f(xk)", "xk+1", "f(xk+1)", "|xk-x1|"]
    table = PrettyTable(title)

    # Проверка знаков на концах отрезка
    if fun(a) * fun(b) > 0:
        print("Ошибка! На концах отрезка [a;b] функция имеет разные знаки!")
        return

    # Выбор x0 как в методе Ньютона
    if fun(a) * diff(fun, a, 2) > 0:
        x0 = a
    else:
        x0 = b

    x = x0
    x1 = b
    n = 0

    while abs(x - x1) > epsilon or abs(fun(x)) > epsilon:
        x0 = x
        x = x1
        x1 = x - (x - x0) * fun(x) / (fun(x) - fun(x0))

        table.add_row(
            [n, round(x0, digits), round(fun(x0), digits), round(x, digits), round(fun(x), digits), round(x1, digits),
             round(fun(x1), digits), round(abs(x - x1), digits)])

        n += 1

    draw_plot(fun, x)
    print(table)
    print("Количество итераций:", n)
    saveResult(str(table), "Количество итераций: " + str(n))


def phi(x):
    lambda1 = -1 / diff(fun, x)
    return x + lambda1 * fun(x)


# Метод простых итераций
def solve_iterations(a, b,  epsilon, digits=3):
    title = ["№", "xk", "f(xk)", "xk+1", "g(xk)", "|xk-xk+1|"]
    table = PrettyTable(title)

    if diff(fun, a) > diff(fun, b):
        x0 = a
    else:
        x0 = b

    n = 0
    x = phi(x0)

    if abs(diff(phi, x0)) >= 1:
        print("Расходится!")
        return

    table.add_row([n, round(x0, digits), round(fun(x0), digits), round(x, digits), round(phi(x), digits),
                   round(abs(x0 - x), digits)])

    while abs(x0 - x) >= epsilon:
        x0 = x
        x = phi(x)
        n += 1
        if diff(phi, x) >= 1:
            print("Условие сходимости не выполнено! Коэффициент сжатия должен быть < 1!")
            return
        table.add_row([n, round(x0, digits), round(fun(x0), digits), round(x, digits), round(phi(x), digits),
                       round(abs(x0 - x), digits)])

    print(table)
    print("Количество итераций:", n)
    draw_plot(fun, x)
    saveResult(str(table), "Количество итераций: " + str(n))


def solve_newton(x, y, epsilon, digits=3):
    x0 = x + epsilon
    y0 = y + epsilon
    n = 0

    title = ["№", "x", "y", "|x - x0|", "|y - y0|"]
    table = PrettyTable(title)

    while max(abs(x - x0), abs(y - y0)) > epsilon:
        x0 = x
        y0 = y
        jacobian = diff_dx(f1, x, y) * diff_dy(f2, x, y) - diff_dx(f2, x, y) * diff_dy(f1, x, y)
        x = x0 - (f1(x0, y0) / jacobian) * diff_dy(f2, x0, y0) + (f2(x0, y0) / jacobian) * diff_dy(f1, x0, y0)
        y = y0 + (f1(x0, y0) / jacobian) * diff_dx(f2, x0, y0) - (f2(x0, y0) / jacobian) * diff_dx(f1, x0, y0)
        table.add_row([n, round(x, digits), round(y, digits), round(abs(x - x0), digits), round(abs(y - y0), digits)])
        n += 1

    print(table)
    print("Количество итераций:", n)
    draw_system_plot(f1, f2, x, y)
    saveResult(str(table), "Количество итераций: " + str(n))


def readFloat():
    try:
        return float(str.replace(input(), ",", "."))
    except ValueError as e:
        print("Ошибка ввода данных! Проверьте данные!")
        exit(-1)
    except EOFError as e:
        print("EOF triggered")
        exit(0)

def readFloatFromFile(f):
    try:
        return float(str.replace(f.readline(), ",", "."))
    except ValueError as e:
        print("Ошибка ввода данных! Проверьте данные!")
        exit(-1)
    except EOFError as e:
        print("EOF triggered")
        exit(0)

print("Считать данные с файла <y/n>? В противном случае будет осуществлен ввод с клавиатуры.")
s = ""
try:
    s = input()
except EOFError as e:
    print("EOF triggered")
    exit(0)

n = 0
a = 0
b = 0
epsilon = 0
x0 = 0
x = 0
y = 0

if s == "Y" or s == "y":
    print("Введите название файла:")
    try:
        file = open(input(), 'r')
        funcId = int(readFloatFromFile(file))
        if funcId == 4:
            x = readFloatFromFile(file)
            y = readFloatFromFile(file)
            epsilon = readFloatFromFile(file)
            solve_newton(x, y, epsilon)
            exit(0)

        n = int(readFloatFromFile(file))
        if n == 1:
            a = readFloatFromFile(file)
            b = readFloatFromFile(file)
            if b < a:
                print("Что с вами не так? Вы не выспались? Как правая граница может быть больше левой?")
                print("*тихонько меняю местами*")
                c = a
                a = b
                b = c

            epsilon = readFloatFromFile(file)
        elif n == 2:
            a = readFloatFromFile(file)
            b = readFloatFromFile(file)
            if b < a:
                print("Что с вами не так? Вы не выспались? Как правая граница может быть больше левой?")
                print("*тихонько меняю местами*")
                c = a
                a = b
                b = c

            epsilon = readFloatFromFile(file)
    except EOFError as e:
        print("EOF triggered")
    except FileNotFoundError as e:
        print("Файл не найден!")
        exit(0)
    except PermissionError as e:
        print("Нет прав на чтение!")
        exit(0)
else:
    print("Выберите функцию/метод Ньютона для СНУ:")
    print("1. -2.4 * x^3 + 1.27 * x^2 + 8.63 * x + 2.31")
    print("2. x^3 - x + 4")
    print("3. x * sin(2x)")
    print("4. Метод Ньютона для Системы уравнений")

    funcId = int(readFloat())

    if funcId == 4:
        print("Введите начальный X:")
        x = readFloat()
        print("Введите начальный Y:")
        y = readFloat()
        print("Введите погрешность:")
        epsilon = readFloat()
        solve_newton(x, y, epsilon)
        exit(0)

    if funcId != 1 and funcId != 2 and funcId != 3:
        print("Некорректный номер функции! По умолчанию будет использоваться 1-я!")
        funcId = 1

    print("Выберите метод решения:")
    print("1 - Метод секущих")
    print("2 - Метод простой итерации")

    n = readFloat()

    if n == 1:
        print("Введите левую границу:")
        a = readFloat()
        print("Введите правую границу:")
        b = readFloat()
        if b < a:
            print("Что с вами не так? Вы не выспались? Как правая граница может быть больше левой?")
            print("*тихонько меняю местами*")
            c = a
            a = b
            b = c

        print("Введите погрешность:")
        epsilon = readFloat()
    elif n == 2:
        print("Введите левую границу:")
        a = readFloat()
        print("Введите правую границу:")
        b = readFloat()
        if b < a:
            print("Что с вами не так? Вы не выспались? Как правая граница может быть больше левой?")
            print("*тихонько меняю местами*")
            c = a
            a = b
            b = c
        print("Введите погрешность:")
        epsilon = readFloat()
    else:
        print("Ввод некорректен!")
        exit(0)

if epsilon > 0:
    if n == 1:
        solve_secant(a, b, epsilon)
    elif n == 2:
        solve_iterations(a, b, epsilon)
    else:
        print("Ошибка! Метод не найден!")
else:
    print("Значение погрешности должно быть положительным числом!")
