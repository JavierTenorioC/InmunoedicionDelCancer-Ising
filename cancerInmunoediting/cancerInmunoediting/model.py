import mesa
import numpy as np

from cancerInmunoediting.scheduler import RandomActivationByTypeFiltered
from cancerInmunoediting.agents import CancerCell, CellNK, CellM, CellN, TCell, ThCell, TregCell


'''
Pendientes:
    Hacer contador y chart de:
        -Tasa de crecimiento del tumor
        -Hamiltoniano de Ising para el TME, células tumorales y anti tumorales
        -Contador para las células tumorales y no tumorales
'''

class CancerInmunoediting(mesa.Model):
    
    description = (
        "A model for simulating cancer inmunoediting, quantified by Ising Hamiltonian"
        )
    verbose = False
    width = 1
    height = 1
    
    def __init__(self,meanIS, stdIS, meanCancer, stdCancer):
        super().__init__()
        self.sigma1 = stdIS
        self.mu1 = meanIS
        self.sigma2 = stdCancer
        self.mu2 = meanCancer
        self.k = 4
        self.t0 = 0.5
        self.contM1Attack = 0
        self.contN1Attack = 0
        self.contNKAttack = 0
        self.contTAttack = 0
        
        # Distribución de probabilidad 
        
        # self.proCancer = 0
        # self.antiCancer = 0
        
        # self.distr = { "d" : [0.2 , 0.3]
        #               "m" : [0.5 , 0.3]
        #               "f" : [0.7, 0.3]
        #     }
        
        # Debe de ser en escala de 0-1?
        # Hay ocasiones donde hay más de 100 células
        
        
        self.t0 = 0.5
        self.k = 4
        self.n = 1
        self.noCells = 1
        self.Beta = np.random.normal(self.mu2, self.sigma2)
        self.a = 10*self.Beta - 1 
        
        self.rateCancerGrowth = 0
        
        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width + 1, self.height + 1, True)
        
        
        self.dictFuction = {'CC' : lambda uniqueID, model, mu, sigma,k ,t0 : CancerCell(uniqueID, model, mu, sigma, k, t0)}
        self.datacollector = mesa.DataCollector(
            {
                "CancerCells" : lambda m : m.schedule.get_type_count(CancerCell),
                "CellsNK": lambda m: m.schedule.get_type_count(CellNK),
                "CellsM1": lambda m: m.schedule.get_type_count(CellM, lambda x: x.antiTumor),
                "CellsM2": lambda m: m.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
                "CellsN1": lambda m: m.schedule.get_type_count(CellN, lambda x: x.antiTumor),
                "CellsN2": lambda m: m.schedule.get_type_count(CellN, lambda x: not(x.antiTumor)),
                "AntiCancer": lambda m : m.schedule.get_count( lambda x: x.antiTumor),
                "ProCancer" : lambda m: m.schedule.get_count( lambda x: not(x.antiTumor))
                }
            )
        
        self.initialCancerCells = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.initialNaturalKillers = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialMacrofagues = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialNeutrophils = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialThCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTregCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        
        self.maxAgeM1 = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.maxAgeN1 = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.maxAgeM2 = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.maxAgeN2 = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.maxAgeNK = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.maxAgeT = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.maxAgeTh = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.maxAgeTreg = int(np.random.normal(self.mu1,self.sigma1)*100)
        
        self.recruitPr = np.random.normal(self.mu1, self.sigma1, 6)
        
        # print(self.current_id)
        
        for i in range(self.initialCancerCells):
            cell = CancerCell(self.next_id(), self, self.mu2, self.sigma2, self.k, self.t0)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialNaturalKillers):
            cell = CellNK(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeNK)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialMacrofagues):
            cell = CellM(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2, [self.maxAgeM1, self.maxAgeM2])
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialNeutrophils):
            cell = CellN(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2, [self.maxAgeN1, self.maxAgeN2])
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialTCells):
            cell = TCell(self.next_id(), self, self.mu1, self.sigma1,self.maxAgeT)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialThCells):
            cell = ThCell(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeTh)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialTregCells):
            cell = TregCell(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeTreg)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        # print(self.current_id)
        self.running = True
        self.datacollector.collect(self)
        
        
    def createInitialCells(self,**args):
        
        for i in range(args['noCells']):
            cell = self.dictFuction['typeCell'](elem for elem in args)
            self.schedule.add(cell)
        
    def cancerGrowth(self):
        self.newCells = int(self.a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
        for i in range(self.newCells):
            cell = CancerCell(self.next_id(), self, self.mu2, self.sigma2, self.k, self.t0)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        return self.newCells
    
    def ISrecuit(self):
        
        if self.random.uniform(0,1) >= self.recruitPr[0]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = CellNK(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeNK)
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
        
        if self.random.uniform(0,1) >= self.recruitPr[1]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = CellM(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2, [self.maxAgeM1, self.maxAgeM2])
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
                
        if self.random.uniform(0,1) >= self.recruitPr[2]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = CellN(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2, [self.maxAgeN1, self.maxAgeN2])
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
                
        if self.random.uniform(0,1) >= self.recruitPr[3]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = TCell(self.next_id(), self, self.mu1, self.sigma1,self.maxAgeT)
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
                
        if self.random.uniform(0,1) >= self.recruitPr[4]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = ThCell(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeTh)
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
                
        if self.random.uniform(0,1) >= self.recruitPr[5]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            for i in range(newCells):
                cell = TregCell(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeTreg)
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))

    def step(self):
        self.cancerGrowth()
        self.ISrecuit()
        # self.contM1Attack = 0
        # self.contN1Attack = 0
        # self.contNKAttack = 0
        # self.contTAttack = 0
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        
        # if self.verbose:
        #     print(
        #         [
        #             self.schedule.time,
        #             self.schedule.get_type_count(CancerCell),
        #             self.schedule.get_type_count(CellNK),
        #             self.schedule.get_type_count(CellM),
        #             self.schedule.get_type_count(CellN),
        #             self.schedule.get_type_count(TCell),
        #             self.schedule.get_type_count(ThCell),
        #             self.schedule.get_type_count(TregCell),
        #             self.schedule.get_type_count(CellM, lambda x: x.antiTumor),
        #             self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
        #         ]
        #     )
            # print([[elem, elem.__class__.__name__] for elem in self.schedule._agents])
            # print("Elementos")
            # print(len(self.schedule._agents), self.current_id)
            # # print([elem for elem in self.schedule._agents])
            # print(type(self.schedule.agents_by_type))
            # for key, value in self.schedule.agents_by_type:
            #     print(key, value)

    def run_model(self, step_count=200):

        # if self.verbose:
        #     print("Initial number CellM: ", self.schedule.get_type_count(CellM))
        #     print("Initial number CellM1: ", self.schedule.get_type_count(CellM, lambda x: x.antiTumor))
        #     print(
        #         "Initial number CellM2: ",
        #         self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
        #     )

        for i in range(step_count):
            self.step()

        # if self.verbose:
        #     print("")
        #     print("Final number CellM: ", self.schedule.get_type_count(CellM))
        #     print("Final number CellM1: ", self.schedule.get_type_count(CellM, lambda x: x.antiTumor))
        #     print(
        #         "Final number CellM2: ",
        #         self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
        #     )