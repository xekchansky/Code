import numpy as np

def f1(x,a,b):
    return (x[0]-a)**2 + x[1]**2 + x[0]/(np.math.fabs(x[1])+b)

def f2(x,a,b):
    return (x[0] - a)**2 + x[0]*x[1] + (x[1] - b)**2

def df1_1(x,a,b):
    return -2*a+1/(np.math.fabs(x[1])+b)+2*x[0]

def df1_2(x,a,b):
    return 2*x[1]-(x[0]*x[1])/(np.math.fabs(x[1])*(np.math.fabs(x[1])+b)**2)

def df2_1(x,a,b):
    return -2*a+2*x[0]+x[1]

def df2_2(x,a,b):
    return -2*b+x[0]+2*x[1]

def search_func(t, coef):
    x = coef[0]
    f = coef[1]
    d = coef[2]
    a = coef[3]
    b = coef[4]
    td = t*d
    return f(x + t*d, a, b)

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
    #print(a, y, z, b)
    f_y = f(y, coef)
    f_z = f(z, coef)
    for k in range(1, N - 3):
        if f_y > f_z:
            #print(1)
            a = y
            y = z
            f_y = f_z
            z = a + fib(N - k - 1) * (b - a) / fib(N - k)
            f_z = f(z, coef)
        else:
            #print(2)
            b = z
            z = y
            f_z = f_y
            y = a + fib(N - k - 2) * (b - a) / fib(N - k)
            f_y = f(y, coef)
        #print(a, y, z, b)
    z = y + max_eps
    if f(y, coef) == f(z, coef):
        a = y
    elif f(y, coef) < f(z, coef):
        b = z
    return (a + b) / 2

def fletcher_reeves(f,df, a,b,x0, M, t0, eps1, eps2):
    x = x0.copy()
    x_old = x.copy()
    grad = np.array([df[0](x, a, b), df[1](x, a, b)])
    grad_old = grad
    stop_check = False
    d = 0
    
    for i in range(M):
        #print('i:', i)
        #print('    x:', x, f(x, a ,b))
        #print('    grad:', np.linalg.norm(grad))
        if np.linalg.norm(grad) < eps1:
            return f(x, a, b)
        if i == 0:
            d = -grad
        else:
            B = (np.linalg.norm(grad)**2)/(np.linalg.norm(grad_old)**2)
            #print('    B:', B)
            d = -grad + B * d
        t = fib_search(search_func, bounds=[-0.5, 0.5], tol=eps2, coef=[x, f, d, a, b])
        x_new = x + t*d
        #print('    d:', d)
        #print('    t    :', t, f(x + t*d, a, b))
        #print('    t-0.1:', t - 0.1, f(x + (t-0.1)*d, a, b))
        #print('    t+0.1:', t + 0.1, f(x + (t+0.1)*d, a, b))
        
        #print('    checks:', (np.linalg.norm(np.array(x_new) - np.array(x)) < eps2), (abs(f(x_new, a, b) - f(x, a, b)) < eps2))
        if (np.linalg.norm(np.array(x_new) - np.array(x)) < eps2) and (abs(f(x_new, a, b) - f(x, a, b)) < eps2):
            if stop_check:
                return f(x_new, a, b)
            else:
                stop_check = True
        else:
            stop_check = False
        x_old = x.copy()
        x = x_new.copy()
        grad_old = grad.copy()
        grad = np.array([df[0](x, a, b), df[1](x, a, b)])
        
    return f(x, a, b)
  
type = int(input())
a,b = map(float,input().split(" "))
if type == 0:
    f = f1
    df = [df1_1,df1_2]
else:
    f = f2
    df = [df2_1,df2_2]
eps1,eps2 = map(float,input().split(" "))
x1,x2 = map(float,input().split(" "))
x = [x1,x2]
print(fletcher_reeves(f,df,a,b,x,10000,0.5,eps1,eps2))
