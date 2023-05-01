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
        self.contM1Attack = 0
        self.contN1Attack = 0
        self.contNKAttack = 0
        self.contTAttack = 0
        self.HAntiCancer = 0
        self.HProCancer = 0
        self.HTME = 0
        
        self.nProCancer = 0
        self.nAntiCancer = 0
        
        # Contadores para cada una de las céluas
        self._contCancerCells = 0
        self._contNKCells = 0
        self._contM1Cells = 0
        self._contM2Cells = 0
        self._contN1Cells = 0
        self._contN2Cells = 0
        
        
        
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
                "CancerCells2" : lambda m : m._contCancerCells,
                "CellsNK": lambda m: m.schedule.get_type_count(CellNK),
                "CellsNK2": lambda m: m._contNKCells,
                "CellsM1": lambda m: m.schedule.get_type_count(CellM, lambda x: x.antiTumor),
                "CellsM12": lambda m: m._contM1Cells,
                "CellsM2": lambda m: m.schedule.get_type_count(CellM, lambda x: not(x.antiTumor)),
                "CellsM22": lambda m: m._contM2Cells,
                "CellsN1": lambda m: m.schedule.get_type_count(CellN, lambda x: x.antiTumor),
                "CellsN12": lambda m: m._contN1Cells,
                "CellsN2": lambda m: m.schedule.get_type_count(CellN, lambda x: not(x.antiTumor)),
                "CellsN22": lambda m: m._contN2Cells,
                "AntiCancer": lambda m : m.schedule.get_count( lambda x: x.antiTumor),
                "AntiCancer2": lambda m: m._contNKCells + m._contM1Cells + m._contN1Cells,
                "ProCancer" : lambda m: m.schedule.get_count( lambda x: not(x.antiTumor)),
                "ProCancer2": lambda m: m._contCancerCells + m._contM2Cells + m._contN2Cells,
                "HAntiCancer" : lambda m: m.HAntiCancer,
                "HProCancer" : lambda m: m.HProCancer,
                "HTME": lambda m: m.HTME,
                "TumorGrowthRate": lambda m: m.rateCancerGrowth
                # contadores con O(1)
                
                }
            )
        
        # Se generan los contadores para cada uno de los parámetros establecidos en el data collector
        
        self.initialCancerCells = int(np.random.normal(self.mu2,self.sigma2)*100)
        self.initialNaturalKillers = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialMacrofagues = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialNeutrophils = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialThCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        self.initialTregCells = int(np.random.normal(self.mu1,self.sigma1)*100)
        
        self._contCancerCells = self.initialCancerCells
        self._contNKCells = self.initialNaturalKillers
        self._contM1Cells = self.initialMacrofagues
        self._contN1Cells = self.initialNeutrophils
        
        
        # self.maxAgeM1 = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        # self.maxAgeN1 = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        # self.maxAgeM2 = int(np.random.normal(self.mu2,self.sigma2)*50) + 10
        # self.maxAgeN2 = int(np.random.normal(self.mu2,self.sigma2)*50) + 10
        # self.maxAgeNK = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        # self.maxAgeT = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        # self.maxAgeTh = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        # self.maxAgeTreg = int(np.random.normal(self.mu1,self.sigma1)*50) + 10
        
        
        self.maxAgeM1 = 100//10
        self.maxAgeN1 = 100//10
        self.maxAgeM2 = 100//10
        self.maxAgeN2 = 100//10
        self.maxAgeNK = 100//10
        self.maxAgeT = 100//10
        self.maxAgeTh = 100//10
        self.maxAgeTreg = 100//10
        
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
    
    def generateAge(self,mu,sigma,maxim,offset):
        age = 0
        while age < 10 :
            age = int(np.random.normal(mu,sigma)*maxim) + offset
        return age
        
        
    def createInitialCells(self,**args):
        
        for i in range(args['noCells']):
            cell = self.dictFuction['typeCell'](elem for elem in args)
            self.schedule.add(cell)
        
    def cancerGrowth(self):
        self.Beta = np.random.normal(self.mu2, self.sigma2)
        self.a = 10*self.Beta - 1 
        
        self.newCells = int(self.a/(1 + np.e**(-self.k*(self.schedule.time - self.t0)/10)))
        
        self._contCancerCells += self.newCells
        
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
            
            self._contNKCells += newCells
            
            for i in range(newCells):
                cell = CellNK(self.next_id(), self, self.mu1, self.sigma1, self.maxAgeNK)
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
        
        if self.random.uniform(0,1) >= self.recruitPr[1]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            
            self._contM1Cells += newCells
            
            for i in range(newCells):
                cell = CellM(self.next_id(), self, self.mu1, self.sigma1, self.mu2, self.sigma2, [self.maxAgeM1, self.maxAgeM2])
                self.schedule.add(cell)
                self.grid.place_agent(cell, (self.width,self.height))
                
        if self.random.uniform(0,1) >= self.recruitPr[2]:
            a = 10*np.random.normal(self.mu1,self.sigma1)
            newCells = int(a/(1 + np.e**(-self.k*(self.schedule.time - self.t0))))
            
            self._contN1Cells += newCells
            
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
        self.rateCancerGrowth = self.a * self.k * np.e**(-self.k *(self.schedule.time - self.t0)/10 )/(1 + np.e**(-self.k *(self.schedule.time - self.t0)/10 ))**2
        
    
    def updateH(self):
        # xTumor = []
        # xIS = []
        
        # ans = [0,0]
        
        # for idxi, xi in enumerate(self.schedule.agents):
        #     for idxj, xj in enumerate(self.schedule.agents):
        #         if xi < xj:
        #             ans[xi.antiTumor&1] = ans[xi.antiTumor&1] + (int(xi.antiTumor&1)*2 - 1)*10 * (int(xj.antiTumor&1)*2 - 1)*10 
        
        # print(type(self.schedule.agents)) -> list 
        # print(self.schedule.agents[1].antiTumor) -> bool
        
        # ans = [0,0]
        # lenAgents = len(self.schedule.agents)
        # for xi in range(lenAgents):
        #     for xj in range(xi,lenAgents):
        #         if xi != xj:
        #             ans[xi&1] = ans[xi&1] + (int(xi&1)*2 - 1)*10 * (int(xj&1)*2 - 1)*10 
        # HTME = ans[0] + ans[1]
        
        ans = [0,0]
        for xi in range(len(self.schedule.agents)):
            for xj in range(xi,len(self.schedule.agents)):
                if xi != xj:
                    ans[self.schedule.agents[xi].antiTumor&1] = ans[self.schedule.agents[xi].antiTumor&1] + (int(self.schedule.agents[xi].antiTumor&1)*2 - 1)*10 * (int(self.schedule.agents[xj].antiTumor&1)*2 - 1)*10 
        self.HAntiCancer = ans[0]
        self.HProCancer = ans[1]
        self.HTME = ans[0] + ans[1]
        
        # [xTumor.append(agent) if agent.antiTumor else xIS.append(agent) for agent in self.schedule.agents ]
        # ans = 0
        # for xi in xTumor:
        #     for xj in self.schedule.agents:
        #         if xi != xj:
        #             ans = ans + (int(xi.antiTumor)*2 - 1)*xi.n * (int(xj.antiTumor)*2 - 1)*xj.n 
        # self.HAntiCancer= ans*0.5
        
        # ans = 0
        # for xi in xIS:
        #     for xj in self.schedule.agents:
        #         if xi != xj:
        #             ans = ans + (int(xi.antiTumor)*2 - 1)*xi.n * (int(xj.antiTumor)*2 - 1)*xj.n 
        # self.HProCancer = ans*0.5
        # self.HTME = self.HProCancer + self.HAntiCancer

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
                    self._contCancerCells,
                    self.schedule.get_type_count(CellNK),
                    self._contNKCells,
                    self.schedule.get_type_count(CellM),
                    self._contM1Cells,
                    self.schedule.get_type_count(CellN),
                    self._contN1Cells,
                    # self.schedule.get_type_count(TCell),
                    # self.schedule.get_type_count(ThCell),
                    # self.schedule.get_type_count(TregCell),
                    self.schedule.get_type_count(CellM, lambda x: x.antiTumor),
                    self._contM2Cells,
                    self.schedule.get_type_count(CellN, lambda x: not(x.antiTumor)),
                    self._contN2Cells,
                    # self.HAntiCancer,
                    # self.HProCancer,
                    # self.HTME
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