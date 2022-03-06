#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

/*
 * Решает СЛУ методом Гаусса-Зейделя и выводит количество итераций/вектор погрешностей
 */
double* solve_seidel(double** a, double* b, int n, double epsilon, int max_iterations = 5) {
    int k = 1;
    int M = max_iterations;
    double* previous = new double[n];
    double* result = new double[n];
    double* relative = new double[n];
    double error;

    for (int i = 0; i < n; i++) {
        result[i] = b[i] / a[i][i];
    } // Считаем первое приближение

    do {
        error = 0;

        for (int i = 0; i < n; i++) {
            previous[i] = result[i];
        }

        for (int i = 0; i < n; i++) {
            double s = 0;
            for (int j = 0; j < n; j++) {
                if(j != i) {
                    s += a[i][j] / a[i][i] * result[j];
                }
            }

            result[i] = b[i] / a[i][i] - s;

            relative[i] = fabs(previous[i] - result[i]);

            if(relative[i] > error) {
                error = relative[i];
            }
        }

        if(k < M) {
            k++;
        } else {
            cout << "Превышено допустимое количество итераций" << endl;
            break;
        }
    } while (error > epsilon);

    cout << "Количество итераций: " << k << endl;
    cout << "Вектор погрешностей:" << endl;

    for (int i = 0; i < n; i++) {
        cout << "[" << i << "] - " << relative[i] << endl;
    }

    return result;
}

/*
 * Преводит матрицу к диагональному преобладанию
 */
void transposition(double** a, int n) {
    for (int i = 0; i < n; i++) {
        double sum = 0;
        for (int j = 0; j < n; j++) {
            sum += abs(a[i][j]);
        }
        sum -= abs(a[i][i]);
        if (sum >= a[i][i]) {
            for (int k = 0; k < n; k++) {
                if (a[k][i] > a[i][i]) {
                    double *temp = a[k];
                    a[k] = a[i];
                    a[i] = temp;
                }
            }
        }
    }
}

/*
 * Проверяет матрицу на диагональное обладание и выводит сравнения сообщениями
 */
bool diagonal_dominance(double** a, int n) {
    bool flag = true;
    for (int i = 0; i < n; i++) {
        double sum = 0;
        for (int j = 0; j < n; j++) {
            sum += abs(a[i][j]);
        }
        sum -= abs(a[i][i]);
        if (sum > a[i][i]) {
            flag = false;
            cout << a[i][i] << " < " << sum << endl;
        } else {
            cout << a[i][i] << " > " << sum << endl;
        }
    }

    return flag;
}

/*
 * Выводит на экран СЛУ
 */
void print_SLE(double** a, double* b, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) {
            if (j != n) {
                cout << a[i][j] << "\t";
            } else {
                cout << b[i] << "\t";
            }
        }
        cout << endl;
    }
}

/*
 * Метод для решения СЛУ методом Гаусса-Зейделя
 * Содержит проверку на диагональное преобладание
 * Текстовое сопровождение с процессом выполнения
 */
void solve(double** a, double* b, int n, double epsilon, int max_iterations = 5) {
    cout << "Проверим диагональное преобладание..." << endl;

    if(!diagonal_dominance(a, n)) {
        cout << "Нет диагонального преобладания! Программа попытается привести СЛУ к диагональному преобладанию..." << endl;
        transposition(a, n);
        cout << "Матрица после приведения к диагональному преобладанию:" << endl;
        print_SLE(a, b, n);
    } else {
        cout << "Диагональное преобладание соблюдено!" << endl;
    }

    cout << "Решим систему методом Зейделя..." << endl;

    double* x = solve_seidel(a, b, n, epsilon, max_iterations);

    cout << "Вектора неизвестных:" << endl;

    for (int i = 0; i < n; i++) {
        cout << x[i] << "\t";
    }
}

int main() {
    cout << "Считать СЛУ с файла <y/n>? В противном случае будет осуществлен ввод с клавиатуры." << endl;
    string reading;
    cin >> reading;
    int n;
    double** a; // коэффициенты
    double* b; // правая часть СЛУ
    double epsilon;
    if(reading == "y" || reading == "Y") {
        ifstream input;
        cout << "Введите название файла: ";
        string file;
        cin >> file;

        input.open(file);

        if (!input.is_open()) {
            cout << "Файл не найден!";
            return 1;
        }

        input >> n;
        cout << "Введенный порядок матрицы (n <= 20): " << n << endl;

        if (n > 20) {
            cout << "Максимальный порядок матрицы 20!" << endl;
            return 2;
        }

        input >> epsilon;
        cout << "Введенная желаемая точность вычисления: " << epsilon << endl;

        a = new double*[n];
        b = new double[n];

        for (int i = 0; i < n; i++) {
            a[i] = new double[n];
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j <= n; j++) {
                if (j != n) {
                    input >> a[i][j];
                } else {
                    input >> b[i];
                }
            }
        }
    } else {
        cout << "Введите порядок матрицы (n <= 20): ";
        cin >> n;
        if (n > 20) {
            cout << "Максимальный порядок матрицы 20!" << endl;
            return 2;
        }

        cout << "Введите желаемую точность вычисления: ";
        cin >> epsilon;

        a = new double*[n];
        b = new double[n];

        for (int i = 0; i < n; i++) {
            a[i] = new double[n];
        }

        cout << "Введите коэффициенты матрицы: " << endl;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                cin >> a[i][j];
            }
        }

        cout << "Введите коэфициенты правой части СЛУ: " << endl;
        for (int i = 0; i < n; i++) {
            cin >> b[i];
        }
    }

    cout << "Вы ввели:" << endl;
    print_SLE(a, b, n);

    solve(a, b, n, epsilon);

    return 0;
}
