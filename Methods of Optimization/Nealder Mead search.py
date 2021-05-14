
import numpy as np

def f0(x,coef):
    return (4*(x[0] - coef[0])**2 + (x[1] - coef[1])**2)
def f1(x,coef):
    return (x[0]-coef[0])**2 + x[0]*x[1] + coef[1]*(x[1]-3)**2

def Nealder_Mead(f, x0, tol, coef):
    al = 1
    beta = 0.5
    gam = 2
    adict = {tuple(x0[0]):f(x0[0], coef), tuple(x0[1]):f(x0[1], coef), tuple(x0[2]):f(x0[2], coef)}
    points = sorted(adict.items(), key=lambda x: x[1])

    b = np.array(points[0][0])
    g = np.array(points[1][0])
    w = np.array(points[2][0])
    sum = 0
    x_mid = (g + b)/2
    
    #square
    for x in x0:
        sum += (f(x, coef) - f(x_mid, coef)) ** 2
    sig = ((1/len(x0)) * sum) ** 0.5
    
    while sig >= tol:
        #print(sig)
        adict = {tuple(x0[0]):f(x0[0], coef), tuple(x0[1]):f(x0[1], coef), tuple(x0[2]):f(x0[2], coef)}
        points = sorted(adict.items(), key=lambda x: x[1])

        b = np.array(points[0][0])
        g = np.array(points[1][0])
        w = np.array(points[2][0])
        sum = 0
        x_mid = (g + b)/2

        #square
        for x in x0:
            sum += (f(x, coef) - f(x_mid, coef)) ** 2
        sig = ((1/len(x0)) * sum) ** 0.5
        
        xr = x_mid + al * (x_mid - w)
        if f(xr, coef) < f(g, coef):
            w = xr
        else:
            if f(xr, coef) < f(w, coef):
                w = xr
            c = (w + x_mid)/2
            if f(c, coef) < f(w, coef):
                w = c
        if f(xr, coef) < f(b, coef):

            # expansion
            xe = x_mid + gam * (xr - x_mid)
            if f(xe, coef) < f(xr, coef):
                w = xe
            else:
                w = xr
        if f(xr, coef) > f(g, coef):
            
            # contraction
            xc = x_mid + beta * (w - x_mid)
            if f(c, coef) < f(w, coef):
                w = xc

        # update points
        x0[0] = w
        x0[1] = g
        x0[2] = b
    return f(b, coef)

type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
x0 = []
for k in range(3):
    x0.append(np.array([i for i in map(float,input().split())]))
tol = float(input())
r1 = Nealder_Mead(f, x0, tol, coef)
print("{:.10f}".format(r1))
