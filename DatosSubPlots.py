import pandas
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib.colors as mc
import matplotlib as mpl

# Cancer: rojo
# IS: azul
# mpl.style.use(sty)
def plotOverride(df,title):
    plt.figure()
    plt.title(title)
    plt.grid(True)
    plt.plot(df['Step'][:],df['AntiCancer'][:],label="Sistema Inmune",color = "#eab676" )
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.plot(df['Step'][:],df['ProCancer'][:],label="Cancer", color = "#76b5c5")
    plt.legend()
    plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")


df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/DatosSimulaciones/model_data[Thu Jun  8 23:47:55 2023].csv')
# cancer IS
debilDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` <= 0.35 ")
debilMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` <= 0.35 ")
debilFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35 ")

# cancer IS
medioDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
medioMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
medioFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75  ")

# cancer IS
fuerteDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35")
fuerteMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
fuerteFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.75 ")

fig = plt.figure(figsize=(8, 6))
ax1 = plt.subplot(3, 3, 1) 
ax1.plot(debilDebil)
ax1.set_title('Cancer: Debil, IS:Debil')
ax2 = plt.subplot(3, 3, 2)
ax2.plot(debilMedio)
ax2.set_title('Cancer: Debil, IS:Medio')
ax3 = plt.subplot(3, 3, 3)
ax3.plot(debilFuerte)
ax3.set_title('Cancer: Debil, IS:Fuerte')
ax4 = plt.subplot(3, 3, 4) 
ax4.plot(debilDebil)
ax4.set_title('Cancer: Debil, IS:Debil')
ax5 = plt.subplot(3, 3, 5)
ax5.plot(debilMedio)
ax5.set_title('Cancer: Debil, IS:Medio')
ax6 = plt.subplot(3, 3, 6)
ax6.plot(debilFuerte)
ax6.set_title('Cancer: Debil, IS:Fuerte')
ax1 = plt.subplot(3, 3, 7) 
ax1.plot(debilDebil)
ax1.set_title('Cancer: Debil, IS:Debil')
ax2 = plt.subplot(3, 3, 8)
ax2.plot(debilMedio)
ax2.set_title('Cancer: Debil, IS:Medio')
ax3 = plt.subplot(3, 3, 9)
ax3.plot(debilFuerte)
ax3.set_title('Cancer: Debil, IS:Fuerte')


fig.tight_layout()

plotOverride(debilDebil,"Cancer: Débil, IS: Débil")
plotOverride(debilMedio,"Cancer: Débil, IS: Medio")
plotOverride(debilFuerte,"Cancer: Débil, IS: Fuerte")

plotOverride(medioDebil,"Cancer: Medio, IS: Débil")
plotOverride(medioMedio,"Cancer: Medio, IS: Medio")
plotOverride(medioFuerte,"Cancer: Medio, IS: Fuerte")

plotOverride(fuerteDebil,"Cancer: Fuerte, IS: Débil")
plotOverride(fuerteMedio,"Cancer: Fuerte, IS: Medio")
plotOverride(fuerteFuerte,"Cancer: Fuerte, IS: Fuerte")
