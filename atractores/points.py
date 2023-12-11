import math
import random

def buscar_atractores(n=5):
    atractores = []

    encontrados = 0
    while encontrados < n:
        x = random.uniform(-0.5, 0.5)
        y = random.uniform(-0.5, 0.5)

        xe = x + random.uniform(-0.5, 0.5) / 1000
        ye = y + random.uniform(-0.5, 0.5) / 1000

        dx = xe - x
        dy = ye - y 
        d0 = math.sqrt(dx*dx + dy*dy)

        a = [random.uniform(-2, 2) for i in range(12)]

        x_lista = [x]
        y_lista = [y]

        convergiendo = False
        lyapunov = 0

        for i in range(100000):
            xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
            ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y

            if xnew > 1e10 or ynew > 1e10 or xnew < -1e10 or ynew < -1e10:
                convergiendo = True
                break
            
            if abs(x - xnew) < 1e-10 and abs(y - ynew) < 1e-10:
                convergiendo = True
                break

            if i > 1000:
                xenew = a[0] + a[1]*xe + a[2]*xe*xe + a[3]*ye + a[4]*ye*ye + a[5]*xe*ye
                yenew = a[6] + a[7]*xe + a[8]*xe*xe + a[9]*ye + a[10]*ye*ye + a[11]*xe*ye

                dx = xenew - xnew
                dy = yenew - ynew
                d = math.sqrt(dx*dx + dy*dy)

                lyapunov += math.log(abs(d/d0))

                xe = xnew + d0*dx/d
                ye = ynew + d0*dy/d

            x = xnew
            y = ynew

            x_lista.append(x)
            y_lista.append(y)

        if not convergiendo and lyapunov >= 10:
            encontrados += 1
            atractores.append((x_lista[100:], y_lista[100:]))

        parametros = (x_lista[0],y_lista[0],a)

    return atractores,parametros
