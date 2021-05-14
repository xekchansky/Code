import numpy as np

def f(x,a,b):
    return (x[0]-x[1]**2)**2 + (a-x[0])**2 + b

def df_1(x,a,b):
    return -2*(a-2*x[0]+x[1]**2)

def df_2(x,a,b):
    return -4*x[1]*(x[0]-x[1]**2)

def df_1_1(x,a,b):
    return 4

def df_1_2(x,a,b):
    return -4*x[1]

def df_2_2(x,a,b):
    return -4*(x[0]-3*x[1]**2)

def df_2_1(x,a,b):
    return -4*x[1]

def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)

def ft(t,dk,x,f,a,b):
    x += t * dk
    return f(x,a,b)

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

def newton_method(f, df, H,a,b, x0, M, t0, eps1, eps2):
    x = x0.copy()
    grad = np.array([df[0](x, a, b), df[1](x, a, b)])
    stop_check = False
    for i in range(M):
        #print('i:', i)
        #print('    x:', x, f(x, a ,b))
        #print('    grad:', np.linalg.norm(grad))
        if np.linalg.norm(grad) < eps1:
            return f(x, a, b)
        
        Hx = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                Hx[i][j] = H[i][j](x, a, b)
        if is_pos_def(Hx):
            Hi = np.linalg.inv(Hx)
            d = -Hi.dot(grad)
            t = 1
        else:
            d = -grad
            t = fib_search(search_func, bounds=[-0.5, 0.5], tol=eps2, coef=[x, f, d, a, b])
            
        x_new = x + t * d
        
        if (np.linalg.norm(np.array(x_new) - np.array(x)) < eps2) and (abs(f(x_new, a, b) - f(x, a, b)) < eps2):
            if stop_check:
                return f(x_new, a, b)
            else:
                stop_check = True
        else:
            stop_check = False
            
        x = x_new.copy()
        grad = np.array([df[0](x, a, b), df[1](x, a, b)])
    return f(x, a, b)
  
a,b = map(float,input().split(" "))
f = f
df = [df_1,df_2]
H = [[df_1_1,df_1_2],[df_2_1,df_2_2]]
eps1,eps2 = map(float,input().split(" "))
x1,x2 = map(float,input().split(" "))
x = [x1,x2]
print(newton_method(f,df,H,a,b,x,10000,0.5,eps1,eps2))
