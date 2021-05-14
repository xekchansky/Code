def f0(x,coef):
    return (coef[0]*x-1)**2+4*(4-coef[1]*x)**4

def df0(x,coef):
    return 2*coef[0]*(coef[0]*x-1)-16*coef[1]*(4-coef[1]*x)**3

def f1(x,coef):
    return coef[0]*(x - coef[1]) + (x - coef[2])**2

def df1(x,coef):
    return coef[0] - 2*coef[2] + 2*x

def secant_search(f, df, x0, x1, coef, tol):
    x_prev = x0
    f_x_prev = f(x_prev, coef)
    df_x_prev = df(x_prev, coef)
    x = x1
    f_x = f(x, coef)
    df_x = df(x, coef)
    while (abs(x - x_prev) > tol) or (x == x0):
        x_new = (df_x * x_prev - df_x_prev * x) / (df_x - df_x_prev)
        x_prev = x
        f_x_prev = f_x
        df_x_prev = df_x
        x = x_new
        f_x = f(x, coef)
        df_x = df(x, coef)
    return x, x_prev
  
type = int(input())
f = f0 if (type == 0) else f1
df = df0 if (type == 0) else df1
coef = [i for i in map(float,input().split())]
x0, x1, tol = map(float, input().split())
r1, r2 = secant_search(f, df, x0, x1,coef, tol)
print("{:.10f}".format(r1))
