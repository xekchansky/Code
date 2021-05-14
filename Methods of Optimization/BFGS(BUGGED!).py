import numpy as np

def f1(x,a,b):
    return (x[0]-x[1]**2)**2 + (a-x[0])**2 + b

def f2(x,a,b):
    return (x[0] - a)**2 + x[0]*x[1] + (x[1] - b)**2

def df1_1(x,a,b):
    return -2*(a-2*x[0]+x[1]**2)

def df1_2(x,a,b):
    return -4*x[1]*(x[0]-x[1]**2)

def df2_1(x,a,b):
    return -2*a+2*x[0]+x[1]

def df2_2(x,a,b):
    return -2*b+x[0]+2*x[1]


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


def bfgs_method(f,df,a,b, x0, M, t0, eps):
    x = np.array(x0)
    
    #setup
    #print('    x:', x, f(x, a ,b))
    grad = np.array([df[0](x, a, b), df[1](x, a, b)])
    #print('    grad:', np.linalg.norm(grad))
    C = np.array([[1.0, 0.0], [0.0, 1.0]])
    I = C.copy()
    d = -C.dot(grad)
    x_old = x.copy()
    t = fib_search(search_func, bounds=[0, 0.5], tol=eps, coef=[x, f, d, a, b])
    x += t * d
    grad_old = grad.copy()
    grad = np.array([df[0](x, a, b), df[1](x, a, b)])
    
    for i in range(M):
        print('i:', i)
        print('    x:', x, f(x, a ,b))
        print('    grad:', np.linalg.norm(grad))
        if np.linalg.norm(grad) < eps:
            return f(x, a, b)
        
        s = (x - x_old)
        print('    s:', s)
        y = (grad - grad_old)
        print('    y:', y)
        p = 1 / (y.dot(s))
        print('    p:', p)
        first = I - p * (s[np.newaxis].T.dot(y[np.newaxis]))
        second = first.dot(C)
        third = second.dot(I - p * y.T.dot(s))
        C = third + p * s[np.newaxis].T.dot(s[np.newaxis])
        d = -C.dot(grad)
        print('    d:', d)
        t = fib_search(search_func, bounds=[-0.5, 0.5], tol=eps, coef=[x, f, d, a, b])
        print('    t:', t)
        x_old = x.copy()
        x = x + t * d
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
eps = float(input())
x1,x2 = map(float,input().split(" "))
x = [x1,x2]
print(bfgs_method(f,df,a,b,x,10000,0.5,eps))
