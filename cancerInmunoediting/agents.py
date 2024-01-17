import mesa
import numpy as np
import random 
def contador_llamadas(func):
    def wrapper(*args, **kwargs):
        clase_base = args[0].__class__
        
        # Utilizar el nombre de la clase como clave en lugar del nombre de la función
        clase_base_name = clase_base.__name__
        
        # Inicializar el diccionario interno si aún no existe
        if clase_base_name not in args[0].model.function_counts:
            args[0].model.function_counts[clase_base_name] = {}
        args[0].model.function_counts[clase_base_name][func.__name__] = args[0].model.function_counts[clase_base_name].get(func.__name__, 0) + 1
        
        # Acceder a los valores posicionales
        # print("Valores posicionales (*args):", args)
        # print("Valores posicionales (*args):", args[0].model.function_counts)
        # args[0].model.function_counts[func.__name__] = args[0].model.function_counts.get(func.__name__, 0) + 1
        # wrapper.llamadas += 1
        # print(f"Llamada a '{func.__name__}' de la clase '{args[0].__class__.__name__}' - Número de llamadas: {wrapper.llamadas}")
        return func(*args, **kwargs)
    wrapper.llamadas = 0
    return wrapper

class CancerCell(mesa.Agent):
    """
    Clase que representa una celula cancerosa en el modelo de simulacion.
    """
    def __init__(self, unique_id, model, mu, sigma, pos):
        """
        Inicializa una instancia de la clase CancerCell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar el atributo relacionado a las probabilidades.
            sigma: Desviacion estandar para generar el atributo relacionado a las probabilidades.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model)
        self.antiTumor = False
        self.age = 1
        self.pos = pos
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula cancerosa.
        Incrementa la edad de la celula.
        """
        self.age += 1    

class InIScell(mesa.Agent):
    """
    Clase base para las celulas del sistema inmunologico en el modelo de simulacion.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase InIScell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar el atributo relacionado a las probabilidades.
            sigma: Desviacion estandar para generar el atributo relacionado a las probabilidades.
            maxAge: Diccionario que contiene la edad maxima para cada tipo de celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model)
        self.antiTumor = True
        self.maxAge = maxAge
        self.age = 1
        self.pos = pos

class CellM(InIScell):
    """
    Clase que representa una celula M del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase InIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2, maxAge, pos):
        """
        Inicializa una instancia de la clase CellM.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar los atributos relacionados al tipo de celulas M1.
            sigma: Desviacion estandar para generar los atributos relacionados al tipo de celulas M1.
            mu2: Media para generar los atributos relacionados al tipo de celulas M2.
            sigma2: Desviacion estandar para generar los atributos relacionados al tipo de celulas M2.
            maxAge: Diccionario que contiene la edad maxima para cada tipo de celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
        self.prProTumor = np.random.normal(mu / (mu + mu2), sigma)
        self.mu2 = mu2
        self.sigma2 = sigma2
        self.maxAge = {'M1': maxAge[0], 'M2': maxAge[1]}
        self.CellType = ''
    
    @contador_llamadas
    def polarization(self):
        """
        Realiza la polarizacion de la celula M.
        La polarizacion solo ocurre cuando existen celulas tumorales presentes.
        """
        if self.CellType == '':
            CCs = [agent for agent in self.model.schedule.agents_by_type[CancerCell].values()]
            if len(CCs) > 0 and np.random.uniform(0, 100) < self.model.successInteracMacrTum:
                CC = self.random.choice(CCs)
                self.model.grid.place_agent(self, CC.pos)
                if np.random.uniform(0, 100) < self.model.changeM1ToM2:
                    self.CellType = 'M1'
                    self.model._contM1Cells += 1
                else:
                    self.CellType = 'M2'
                    self.model._contM2Cells += 1
                self.model._contMCells -= 1
    
    @contador_llamadas
    def tumorInteraction(self):
        """
        Interaccion con las celulas tumorales.
        """
        if ( (interac := np.random.uniform(0, 100)) < self.model.successTam1) and self.CellType == 'M1':
            CC = [elem for elem in self.model.grid.get_cell_list_contents((16, 16)) if elem.__class__.__name__ == 'CancerCell']
            randomCC = random.sample(CC, min(len(CC), self.model.MaxDeactivatingCCByM1))
            for cell in randomCC:
                cell.age += 0.1
        elif self.CellType == 'M2' and interac < self.model.successTam2 :
            CC = [elem for elem in self.model.grid.get_cell_list_contents((16, 16)) if elem.__class__.__name__ == 'CancerCell']
            randomCC = random.sample(CC, min(len(CC), self.model.MaxActivatingCCByM2))
            for cell in randomCC:
                cell.age -= 0.1
    
    @contador_llamadas
    def die(self):
        """
        Determina si la celula M debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.CellType != "" and self.maxAge[self.CellType] < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            if self.CellType == "M1":
                self.model._contM1Cells -= 1
            else:
                self.model._contM2Cells -= 1
        self.age += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula M.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.polarization()
        self.tumorInteraction()
        self.die() 

class CellN(InIScell):
    """
    Clase que representa una celula N del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase InIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2, maxAge, pos):
        """
        Inicializa una instancia de la clase CellN.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar los atributos relacionados a las celulas N1.
            sigma: Desviacion estandar para generar los atributos relacionados a las celulas N1.
            mu2: Media para generar los atributos relacionados a las celulas N2.
            sigma2: Desviacion estandar para generar los atributos relacionados a las celulas N2.
            maxAge: Diccionario que contiene la edad maxima para cada tipo de celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
        self.prProTumor = np.random.normal(mu / (mu + mu2), sigma)
        self.mu2 = mu2
        self.sigma2 = sigma2
        self.maxAge = {'N1': maxAge[0], 'N2': maxAge[1]}
        self.CellType = ''
    
    @contador_llamadas
    def polarization(self):
        """
        Realiza la polarizacion de la celula N.
        La polarizacion solo ocurre cuando existen celulas tumorales presentes.
        """
        if self.CellType == '':
            CCs = [agent for agent in self.model.schedule.agents_by_type[CancerCell].values()]
            if len(CCs) > 0 and np.random.uniform(0, 100) < self.model.succesInteracNeutTum:
                CC = self.random.choice(CCs)
                self.model.grid.place_agent(self, CC.pos)
                if np.random.uniform(0, 100) < self.model.changeM1ToM2:
                    self.CellType = 'N1'
                    self.model._contN1Cells += 1
                else:
                    self.CellType = 'N2'
                    self.model._contN2Cells += 1
                self.model._contNCells -= 1

    @contador_llamadas
    def tumorInteraction(self):
        """
        Interaccion con las celulas tumorales.
        """
        if ( (interac := np.random.uniform(0, 100)) < self.model.successTan1) and self.CellType == 'N1':
            CC = [elem for elem in self.model.grid.get_cell_list_contents((16, 16)) if elem.__class__.__name__ == 'CancerCell']
            randomCC = random.sample(CC, min(len(CC), self.model.MaxDeactivatingCCByN1))
            for cell in randomCC:
                cell.age += 0.1
        elif self.CellType == 'N2' and interac < self.model.successTan2:
            CC = [elem for elem in self.model.grid.get_cell_list_contents((16, 16)) if elem.__class__.__name__ == 'CancerCell']
            randomCC = random.sample(CC, min(len(CC), self.model.MaxActivatingCCByN2))
            for cell in randomCC:
                cell.age -= 0.1 
    
    @contador_llamadas
    def die(self):
        """
        Determina si la celula N debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.CellType != "" and self.maxAge[self.CellType] < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            if self.CellType == "N1":
                self.model._contN1Cells -= 1
            else:
                self.model._contN2Cells -= 1
        self.age += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula N.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.polarization()
        self.tumorInteraction()
        self.die() 

class CellNK(InIScell):
    """
    Clase que representa una celula NK del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase InIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase CellNK.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar algunos atributos de la celula.
            sigma: Desviacion estandar para generar algunos atributos de la celula.
            maxAge: Edad maxima de la celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
    
    @contador_llamadas
    def attack(self):
        """
        Ataca a las celulas tumorales.
        """
        # ataque
        killPercent = 5
        if np.random.uniform(0, 100) < self.model.successAttackNk:
            if self.model._contCancerCells > 0:
                CCs = [agent for agent in self.model.schedule.agents_by_type[CancerCell].values()]
                CC = self.random.choice(CCs)
                self.model.grid.place_agent(self, CC.pos)
            
            if self.model._contN2Cells > 0:
                cellsN = [agent for agent in self.model.schedule.agents_by_type[CellN].values()]
                cellN = self.random.choice(cellsN)
                if cellN.CellType == "N2" and cellN.age > self.model.maxAgeN2 and np.random.uniform(0, 100) < killPercent:
                    self.model.grid.remove_agent(cellN)
                    self.model.schedule.remove(cellN)
                    self.model._contN2Cells -= 1
                    # if self.__class__.__name__ not in self.model.contadorMuertes:
                    #     self.model.contadorMuertes[self.__class__.__name__] = {}
                    # self.model.contadorMuertes[self.__class__.__name__] = self.model.contadorMuertes.get(self.__class__.__name__, 0) + 1
            
            if self.model._contM2Cells > 0:
                cellsM = [agent for agent in self.model.schedule.agents_by_type[CellM].values()]
                cellM = self.random.choice(cellsM)
                if cellM.CellType == "M2" and cellM.age > self.model.maxAgeM2 and np.random.uniform(0, 100) < killPercent:
                    self.model.grid.remove_agent(cellM)
                    self.model.schedule.remove(cellM)
                    self.model._contM2Cells -= 1
                    # if self.__class__.__name__ not in self.model.contadorMuertes:
                    #     self.model.contadorMuertes[self.__class__.__name__] = {}
                    # self.model.contadorMuertes[self.__class__.__name__] = self.model.contadorMuertes.get(self.__class__.__name__, 0) + 1
        
    @contador_llamadas
    def die(self):
        """
        Determina si la celula NK debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.maxAge < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model._contNKCells -= 1
        self.age += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula NK.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.attack()
        self.die()
        
class AdIScell(mesa.Agent):
    """
    Clase base para las celulas adicionales del sistema inmunologico en el modelo de simulacion.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase AdIScell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar algunos atributos de la celula.
            sigma: Desviacion estandar para generar algunos atributos de la celula.
            maxAge: Edad maxima de la celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model)
        self.antiTumor = True
        self.age = 1
        self.maxAge = maxAge
        self.pos = pos

class TCell(AdIScell):
    """
    Clase que representa una celula T del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase AdIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase TCell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar algunos atributos de la celula.
            sigma: Desviacion estandar para generar algunos atributos de la celula.
            maxAge: Edad maxima de la celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
        self.successAttackT = self.model.successAttackT
    
    @contador_llamadas
    def die(self):
        """
        Determina si la celula T debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.maxAge < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
    
    @contador_llamadas
    def Attack(self):
        """
        Ataca a las celulas tumorales.
        """
        # ataque
        killPercent = 7
        
        CCs = [agent for agent in self.model.schedule.agents_by_type[CancerCell].values()]
        if len(CCs) and np.random.uniform(0, 100) < self.model.successOfInteracTCellsTumor:
            CC = self.random.choice(CCs)    
            self.model.grid.place_agent(self, CC.pos)
        
        CCs = [elem for elem in self.model.grid.get_cell_list_contents(self.pos) if elem.__class__.__name__ == 'CancerCell']
        for agent in CCs:
        
            if np.random.uniform(0, 100) < self.successAttackT and ((self.model.maxAgeM2 + self.model.maxAgeN2) / 2) < agent.age:
                #print(f"edad:{agent.age} > {(self.model.maxAgeM2 + self.model.maxAgeN2) / 10}")
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                self.model._contCancerCells -= 1 
                # if self.__class__.__name__ not in self.model.contadorMuertes:
                #     self.model.contadorMuertes[self.__class__.__name__] = {}
                # self.model.contadorMuertes[self.__class__.__name__] = self.model.contadorMuertes.get(self.__class__.__name__, 0) + 1
                # self.model._muertesCCporT += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula T.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.Attack()
        self.die()
    
class ThCell(AdIScell):
    """
    Clase que representa una celula Th del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase AdIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase ThCell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar algunos atributos de la celula.
            sigma: Desviacion estandar para generar algunos atributos de la celula.
            maxAge: Edad maxima de la celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
        
    @contador_llamadas
    def strengthening(self):
        """
        Fortalece a las celulas T existentes.
        """
        TCs = [agent for agent in self.model.schedule.agents_by_type[TCell].values()]
        if len(TCs) and np.random.uniform(1, 100) < self.model.succesInteracThCellTC:
            TC = self.random.choice(TCs)
            self.model.grid.place_agent(self, TC.pos)
        
        TCs = [elem for elem in self.model.grid.get_cell_list_contents(self.pos) if elem.__class__.__name__ == 'TCell']
        for TC in TCs:
            TC.successAttackT += 0.2
    
    @contador_llamadas
    def die(self):
        """
        Determina si la celula Th debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.maxAge < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula Th.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.strengthening()
        self.die()

class TregCell(AdIScell):
    """
    Clase que representa una celula Treg del sistema inmunologico en el modelo de simulacion.
    Hereda de la clase AdIScell.
    """
    def __init__(self, unique_id, model, mu, sigma, maxAge, pos):
        """
        Inicializa una instancia de la clase TregCell.

        Args:
            unique_id: ID unico para la celula.
            model: Instancia del modelo de simulacion.
            mu: Media para generar algunos atributos de la celula.
            sigma: Desviacion estandar para generar algunos atributos de la celula.
            maxAge: Edad maxima de la celula.
            pos: Posicion inicial de la celula en el espacio.
        """
        super().__init__(unique_id, model, mu, sigma, maxAge, pos)
    
    @contador_llamadas
    def strengthening(self):
        """
        Fortalece a las celulas T y Th existentes.
        """
        if np.random.uniform(0, 100) < 50:
            TCs = [agent for agent in self.model.schedule.agents_by_type[TCell].values()]
            if len(TCs) and np.random.uniform(0, 100) < self.model.successOfInteracTregCellsTCells:
                TC = self.random.choice(TCs)
                self.model.grid.place_agent(self, TC.pos)
            
            TCs = [elem for elem in self.model.grid.get_cell_list_contents(self.pos) if elem.__class__.__name__ == 'TCell']
            for TC in TCs:
                TC.age -= 0.1
        else:
            ThCs = [agent for agent in self.model.schedule.agents_by_type[ThCell].values()]
            if len(ThCs) and np.random.uniform(0, 100) < self.model.successOfInteracTregCellsThCells:
                ThC = self.random.choice(ThCs)
                self.model.grid.place_agent(self, ThC.pos)
            
            ThCs = [agent for agent in self.model.schedule.agents_by_type[ThCell].values()]
            # if len(ThCs) and np.random.uniform(0, 100) < self.model.successOfInteracTregCellsThCells:
            #     ThC = self.random.choice(ThCs)
            #     self.model.grid.place_agent(self, ThC.pos)
            # ThCs = [elem for elem in self.model.grid.get_cell_list_contents(self.pos) if elem.__class__.__name__ == 'ThCell']
            for ThC in ThCs:
                ThC.age -= 0.1
    
    @contador_llamadas
    def die(self):
        """
        Determina si la celula Treg debe morir y la elimina del modelo.
        """
        probKill = 4
        if self.maxAge < self.age and np.random.uniform(0, 100) < probKill:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            
        self.age += 1
    
    @contador_llamadas
    def step(self):
        """
        Metodo que representa el paso de tiempo para la celula Treg.
        Ejecuta los diferentes procesos que ocurren durante un paso de tiempo.
        """
        self.strengthening()
        self.die()
