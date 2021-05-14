import numpy as np

def f0(x,coef):
    return coef[0]*x[0]**4 + coef[1]*x[1]**3 + coef[2]*x[1]**2 + coef[3]*x[0] + coef[4]
def f1(x,coef):
    return x[0]**2 + coef[0]*x[0]*x[1] + coef[1]*(x[1]-3)**2

def Hooke_Jeeves(f, x0, tol, coef):
    delta = np.array([1.0, 1.0])
    al = 2
    lam = 1
    x0 = x0.astype(np.float)
    # Your Code
    while delta[0] > tol:
        #print(x0)
        f_x0 = f(x0, coef)
        y_min = x0
        f_y_min = f_x0
        changed = False
        for i in range(len(x0)):
            y = x0.copy()
            y[i] = x0[i] + delta[i]
            f_y = f(y, coef)
            #print('y=', y, 'f(y)=',f_y)
            if f_y < f_y_min:
                y_min = y.copy()
                f_y_min = f_y
                changed = True
            y = x0.copy()
            y[i] = x0[i] - delta[i]
            f_y = f(y, coef)
            #print('y=', y, 'f(y)=',f_y)
            if f_y < f_y_min:
                y_min = y.copy()
                f_y_min = f_y
                changed = True
                
        #print('y_min=', y_min, 'f(y_min)=',f_y_min)
        if changed:
            #print('change')
            x0 += lam * (y_min - x0)
        else:
            #print('shrink')
            delta /= al
            #print('delta=', delta)
    
    return x0

type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
x0 = np.array([i for i in map(float,input().split())])
tol = float(input())
r1 = Hooke_Jeeves(f, x0, tol, coef)
print("{:.10f} {:.10f}".format(r1[0], r1[1]))
