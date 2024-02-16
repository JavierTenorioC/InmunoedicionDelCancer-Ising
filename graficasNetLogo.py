import matplotlib.pyplot as plt
import numpy as np
def logistic(x,a,b):
    k=4
    res = []
    for i in x:
        res.append(1 + a/(1 + b*(np.e**(-k*(i-0.5)))))
    return res
x = np.arange(-10,50)

# cuando se tiene mayor definición el error aumenta
# x = np.arange(-10,50,0.01)
def gaussAprox(x,a):
    c=0.19 # desviación estándar 
    b=0.5  # valor máximo
    aux = a*(np.e**(-(x-b)**2))/(2*c**2)
    print(f"aux: {aux}, a: {a}")
    return aux#a*(np.e**(-(x-b)**2))/(2*c**2)

def recruitCC(tiempo, celulasIniciales, a, growthFactor):
    tickSpread = 50
    dx = 1/(tickSpread -1 )
    celulas = [celulasIniciales]
    for i in range(len(tiempo)):
        recluta=int(gaussAprox(dx*tiempo[i], a))
        result= celulas[-1]*recluta
        if result == 0 and np.random.uniform(0,100) < growthFactor:
            result=3
        print(f"recluta: {recluta}, result: {result}")
        celulas.append(result+celulas[-1])
    return celulas

def derLogistic(x,a,b):
    tickSpread = 50
    xx=x/(tickSpread-1)
    x1=logistic(xx,a,1)[1:]
    x2=logistic(xx,a,1)[0:-1]
    # fig, ax = plt.subplots()
    # ax.plot(x[1:], x1, label=f"a={a}" )
    # ax.plot(x[0:-1], x2, label=f"a={a}" )
    # ax.legend(loc = 'upper right')
    # ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    # ax.set_xlabel("Días")
    # ax.set_ylabel("")
    # plt.show()
    res = []
    for i in range(len(x1)):
        # print(x1[i],x2[i])
        try:
            res.append(x1[i]/x2[i])
        except:
            print(x1[i],x2[i])
    # plt.figure()
    # plt.plot(x, x1, label="" )
    return res
# -------------------------------------------------------------------
# fig, ax = plt.subplots()
# # Dibujar puntos

# # a puede variar de -1 a 9
# # b es 1
# # ax.plot(x, derLogistic(x,-1,1), label="a=-1" )
# # ax.plot(x, derLogistic(x,5,1), label="a=5" )
# # ax.plot(x, derLogistic(x,9,1), label="a=9" )

# # Valores de la función logística
# # a debe de ser mayor a 0 la de la ecuación 
# # la a de esta función debe de ser mayor a -1

# # Valores de prueba
# # a = 4.484040290031926
# # ax.plot(x[0:-1], derLogistic(x,a-1,1), label="a=5" )
# # print(f"el máximo es {max(derLogistic(x,a-1,1))}")


# ax.plot(x[0:-1], derLogistic(x,2,-1), label="a=-1" )
# ax.plot(x[0:-1], derLogistic(x,5,1), label="a=5" )
# ax.plot(x[0:-1], derLogistic(x,9,1), label="a=9" )
# # ax.plot(x, logistic(x,-1,1), label="a=-1" )
# # ax.plot(x, logistic(x,5,1), label="a=5" )
# # ax.plot(x, logistic(x,9,1), label="a=9" )
# ax.legend(loc = 'upper right')
# ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
# ax.set_xlabel("Días")
# ax.set_ylabel("")
# # Guardar el gráfico en formato png
# # plt.savefig('diagrama-dispersion.png')
# # Mostrar el gráfico
# plt.show()
#----------------------------------------------------------------
fig, ax = plt.subplots()
a = 0.010308558104216381
growthFactor = 14.652003782573209
# ax.plot(x, gaussAprox(x,a), label=f"a={a}" )
celulasIniciales = 12
ax.plot(x, recruitCC(x, celulasIniciales, a, growthFactor)[1:], label=f"a={a}" )
# ax.plot(x[0:-1], derLogistic(x,5,1), label="a=5" )
# ax.plot(x[0:-1], derLogistic(x,9,1), label="a=9" )
ax.legend(loc = 'upper right')
ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
ax.set_xlabel("Días")
ax.set_ylabel("")
# Guardar el gráfico en formato png
# plt.savefig('diagrama-dispersion.png')
# Mostrar el gráfico
plt.show()