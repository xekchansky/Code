import numpy as np

def f1(x,a,b):
    return a*np.math.sin(x[0]) + b*np.math.cos(x[1])

def f2(x,a,b):
    return (x[0] - a)**2 + x[0]*x[1] + (x[1] - b)**2

def df1_1(x,a,b):
    return a*np.math.cos(x[0])

def df1_2(x,a,b):
    return -b*np.math.sin(x[1])

def df2_1(x,a,b):
    return -2*a+2*x[0]+x[1]

def df2_2(x,a,b):
    return -2*b+x[0]+2*x[1]

def coordinate_descent(f, df, a,b,x00, M, t0, eps1, eps2):
    x = x00
    
    for i in range(M):
        #print('i:', i)
        if np.linalg.norm([df[0](x, a, b), df[1](x, a, b)]) < eps1:
            return f(x, a, b)
        
        for k in range(len(x)):
            #print('    k:', k)
            t = t0
            success = False
            stop_check = False
            
            while (not success):
                #print('        x:', x, f(x, a, b))
                x_new = x.copy()
                x_new[k] = x[k] - t * df[k](x, a, b)
                
                if (f(x_new, a, b) - f(x, a, b) < 0): #or (f(x_new, a, b) - f(x, a, b) < -eps1 * np.linalg.norm([df[0](x, a, b), df[1](x, a, b)]) ** 2):
                    success = True
                else:
                    t /= 2
                    
                if (np.linalg.norm(np.array(x_new) - np.array(x)) < eps2) and (abs(f(x_new, a, b) - f(x, a, b)) < eps2):
                    if stop_check:
                        if success:
                            return f(x_new, a, b)
                        else:
                            return f(x, a, b)
                    else:
                        stop_check = True
                else:
                    stop_check = False
                    
            x = x_new.copy()
                    
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
print(coordinate_descent(f,df,a,b,x,10000,0.5,eps1,eps2))
