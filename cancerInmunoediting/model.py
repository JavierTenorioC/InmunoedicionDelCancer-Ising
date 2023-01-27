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
    verbose = True
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
                }
            )
        
        self.initialCancerCells = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.initialNaturalKillers = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialMacrofagues = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialNeutrophils = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialThCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTregCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        # print(self.current_id)
        
        for i in range(self.initialCancerCells):
            cell = CancerCell(self.next_id(), self, self.mu2, self.sigma2, self.k, self.t0)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialNaturalKillers):
            cell = CellNK(self.next_id(), self, self.mu1, self.sigma1)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialMacrofagues):
            cell = CellM(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialNeutrophils):
            cell = CellN(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialTCells):
            cell = TCell(self.next_id(), self, self.mu1, self.sigma1)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
            
        for i in range(self.initialThCells):
            cell = ThCell(self.next_id(), self, self.mu1, self.sigma1)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        for i in range(self.initialTregCells):
            cell = TregCell(self.next_id(), self, self.mu1, self.sigma1)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        
        # print(self.current_id)
        self.running = True
        self.datacollector.collect(self)
        
        
    def createInitialCells(self,**args):
        
        for i in range(args['noCells']):
            cell = self.dictFuction['typeCell'](elem for elem in args)
            self.schedule.add(cell)
        
        

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(CancerCell),
                    self.schedule.get_type_count(CellNK),
                    self.schedule.get_type_count(CellM),
                    self.schedule.get_type_count(CellN),
                    self.schedule.get_type_count(TCell),
                    self.schedule.get_type_count(ThCell),
                    self.schedule.get_type_count(TregCell),
                    self.schedule.get_type_count(CellM, lambda x: x.antiTumor),
                    self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
                ]
            )
            # print([[elem, elem.__class__.__name__] for elem in self.schedule._agents])
            # print("Elementos")
            # print(len(self.schedule._agents), self.current_id)
            # # print([elem for elem in self.schedule._agents])
            # print(type(self.schedule.agents_by_type))
            # for key, value in self.schedule.agents_by_type:
            #     print(key, value)

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number CellM: ", self.schedule.get_type_count(CellM))
            print("Initial number CellM1: ", self.schedule.get_type_count(CellM, lambda x: x.antiTumor))
            print(
                "Initial number CellM2: ",
                self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number CellM: ", self.schedule.get_type_count(CellM))
            print("Final number CellM1: ", self.schedule.get_type_count(CellM, lambda x: x.antiTumor))
            print(
                "Final number CellM2: ",
                self.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
            )