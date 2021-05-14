def f0(x,coef):
    return coef[0]*x**2 + coef[1]*x + coef[2]

def f1(x,coef):
    return coef[0]*x**4 + coef[1]*x**3 + coef[2]*x**2 + coef[3]*x + coef[4]

def fib(n):
    if n in [0,1]:
        return 1
    return fib(n - 1) + fib(n - 2)

def fib_search(f, bounds, tol, coef, max_eps = 0.01):
    a = bounds[0]
    b = bounds[1]
    tol = 0.0007
    N = 0
    F_B = (b - a) / tol
    F_N = 0
    while F_N < F_B:
        N += 1
        F_N = fib(N)
    y = a + fib(N - 2) * (b - a)/F_N
    z = a + fib(N - 1) * (b - a)/F_N
    f_y = f(y, coef)
    f_z = f(z, coef)
    for k in range(1, N - 3):
        if f_y > f_z:
            a = y
            y = z
            f_y = f_z
            z = a + fib(N - k - 1) * (b - a) / fib(N - k)
            f_z = f(z, coef)
        else:
            b = z
            z = y
            f_z = f_y
            y = a + fib(N - k - 2) * (b - a) / fib(N - k)
            f_y = f(y, coef)
    z = y + max_eps
    if f(y, coef) == f(z, coef):
        a = y
    elif f(y, coef) < f(z, coef):
        b = z
    return (a + b) / 2

type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
bounds = [0, 0]
bounds[0], bounds[1], tol = map(float, input().split())
r1 = fib_search(f, bounds, tol, coef)
print("{:.10f}".format(r1))
