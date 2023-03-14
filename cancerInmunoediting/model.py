import mesa
import numpy as np

from cancerInmunoediting.scheduler import RandomActivationByTypeFiltered
from cancerInmunoediting.agents import CancerCell, CellNK, CellM, CellN, TCell, ThCell, TregCell


'''
Pendientes:
    Hacer contador y chart de:
        -Tasa de crecimiento del tumor
'''

def getVar(model):
    model.HAntiCancer = len([agent for agent in model.schedule.agents if isinstance(agent, CancerCell)])
    print(f"{model.HAntiCancer} total de células")
    
    return model.HAntiCancer

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
        self.HAntiCancer = 0
        self.HProCancer = 0
        self.HTME = 0
        
        self.nProCancer = 0
        self.nAntiCancer = 0
        
        # Distribución de probabilidad 
        
        self.dictDistr = { "weak" : [[.25 , .15], 0.5],
                      "medium" : [[.45 , np.random.normal(self.mu1,self.sigma1)], 1],
                      "strong" : [[.75, .15],0.6]
            }
        
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
                "ProCancer" : lambda m: m.schedule.get_count( lambda x: not(x.antiTumor)),
                "HAntiCancer" : lambda m: m.HAntiCancer,
                "HProCancer" : lambda m: m.HProCancer,
                "HTME": lambda m: m.HTME,
                "TumorGrowthRate": lambda m: m.rateCancerGrowth
                }
            )
        
        self.initialCancerCells = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.initialNaturalKillers = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialMacrofagues = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialNeutrophils = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialThCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTregCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        
        self.maxAgeM1 = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        self.maxAgeN1 = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        self.maxAgeM2 = int(np.random.normal(self.mu2,self.sigma2)*100) + 1
        self.maxAgeN2 = int(np.random.normal(self.mu2,self.sigma2)*100) + 1
        self.maxAgeNK = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        self.maxAgeT = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        self.maxAgeTh = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        self.maxAgeTreg = int(np.random.normal(self.mu1,self.sigma1)*100) + 1
        
        self.ages = [self.maxAgeM1, self.maxAgeN1,
                     self.maxAgeM2, self.maxAgeN2,
                     self.maxAgeNK, self.maxAgeT,
                     self.maxAgeTh, self.maxAgeTreg]
        
        # print(f'Edades máximas {self.ages}')
        
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
        self.Beta = np.random.normal(self.mu2, self.sigma2)
        self.a = 10*self.Beta - 1 
        
        self.newCells = int(self.a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
        for i in range(self.newCells):
            cell = CancerCell(self.next_id(), self, self.mu2, self.sigma2, self.k, self.t0)
            self.schedule.add(cell)
            self.grid.place_agent(cell, (self.width,self.height))
        # print(self.newCells)
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
    
    # for agent in self.agent_buffer(shuffled=False):
    
    def nUpdate(self):
        # self.nAntiCancer = len([elem for elem in self.grid.get_cell_list_contents([[0,0]]) if elem.antiTumor])
        # self.nProCancer = len([elem for elem in self.grid.get_cell_list_contents([[0,0]]) if not(elem.antiTumor)])
        self.nAntiCancer = self.schedule.get_count( lambda x: not(x.antiTumor))
        self.nProCancer = self.schedule.get_count( lambda x: x.antiTumor)
        # print(f'{self.schedule.get_count( lambda x: x)} elementos')
        # print(self.nAntiCancer, self.nProCancer)
    
    def updateH(self):
        xTumor = []
        xIS = []
        [xTumor.append(agent) if agent.antiTumor else xIS.append(agent) for agent in self.schedule.agents ]
        ans = 0
        for xi in xTumor:
            for xj in xTumor:
                if xi != xj:
                    ans = ans + (int(xi.antiTumor)*2 - 1)*xi.n * (int(xj.antiTumor)*2 - 1)*xj.n 
        self.HAntiCancer= ans*0.5
        
        ans = 0
        for xi in xIS:
            for xj in xIS:
                if xi != xj:
                    ans = ans + (int(xi.antiTumor)*2 - 1)*xi.n * (int(xj.antiTumor)*2 - 1)*xj.n 
        self.HProCancer = ans*0.5
        self.HTME = self.HProCancer - self.HAntiCancer

    def step(self):
        self.nUpdate()
        self.cancerGrowth()
        self.ISrecuit()
        self.updateH()
        
        # self.contM1Attack = 0
        # self.contN1Attack = 0
        # self.contNKAttack = 0
        # self.contTAttack = 0
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
                    self.HAntiCancer,
                    self.HProCancer,
                    self.HTME
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