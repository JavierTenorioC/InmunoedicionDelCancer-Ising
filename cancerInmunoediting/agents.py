import mesa
import numpy as np


class CancerCell(mesa.Agent):
    width = 0
    height = 0
    def __init__(self, unique_id, model, mu, sigma, k, t0):
        super().__init__(unique_id, model)
        self.prAntiProd = np.random.normal(mu,sigma)
        self.Beta = 0
        self.sigma = sigma
        self.mu = mu
        self.t0 = 0.5
        self.k = 4
        self.n = 1
    
    def growth(self,t):
        self.Beta = np.random.normal(self.mu, self.sigma)
        self.a = 10*self.Beta - 1 
        self.noCells = self.noCells + self.a/(1 + np.e**(-self.k *(t-self.t0) ))
        
    def step(self):
        if self.interaction():
            # NKCells = [obj for obj in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(obj, CellNK)][0]
            # print(NKCells)
            # print("Longitud",len(NKCells))
            NKCells = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CellNK']
            NKCellChoice = self.random.choice(NKCells)
            
            if NKCellChoice.interactionAttack:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                
            # print(NKCellChoice.__class__.__name__)
            # print(dir(NKCellChoice))
            # NKCellChoice.attack(self)
            # NKCellChoice.stepConditional()
            
            # CellsM = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CellM']
            # CellMChoice = self.random.choice(CellsM)
            # CellMChoice.stepConditional()
            
            # CellsN = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CellN']
            # CellNChoice = self.random.choice(CellsN)
            # CellNChoice.stepConditional()
            
            # print(NKCells)
            # print(dir(NKCellChoice))
            # print(type(NKCellChoice))
            # print(NKCellChoice.__class__.__name__)
            
        # self.n = self.n * self.a * self.k * ( np.e**(-self.k * (t-self.t0) ))/( 1 + np.e**(-self.k * (t - self.t0)) )**2
            
    def interaction(self):
        return self.prAntiProd >= np.random.normal(0,1)
    

class InIScell(mesa.Agent):
    width = 0
    height = 0
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model)
        self.prRecruit = np.random.normal(mu,sigma)
        self.prAttack = np.random.normal(mu,sigma)
        
        self.sigma = sigma
        self.mu = mu
        
        self.n = 1
    
    def interactionRecruit(self):
        return self.prRecruit >= np.random.normal(0,1)
    
    def interactionAttack(self):
        return self.prAttack >= np.random.normal(0,1)
    
    def attack(self,CancerCellChoice):
        pass
        # print("aaaaaaaaaaaaaaaaaaaaaS")
        # if  self.interactionAttack():
        #     # print(self.model.grid.get_cell_list_contents([self.pos]))
        #     print(self.model.schedule.agents_by_type[CancerCell].keys())
        #     print("antes de eliminar la célula")
        #     # print([elem for elem in self.model.schedule._agents])
        #     print(len(self.model.schedule._agents))
        #     # print(self.model.schedule())
        #     # CancerCells = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(elem, CancerCell)]
        #     # # CancerCells = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CancerCell']
        #     # CancerCellChoice = self.random.choice(CancerCells)
            
        #     self.model.grid.remove_agent(CancerCellChoice)
        #     self.model.schedule.remove(CancerCellChoice)
            
        #     print("Eliminando una célula de cáncer")
        #     print(type(CancerCellChoice))
        #     print(CancerCellChoice.__class__.__name__)
        #     self.model.grid.remove_agent(CancerCellChoice)
        #     self.model.schedule.remove(CancerCellChoice)
        #     print("después de eliminar una célula")
        #     print(len(self.model.schedule._agents))
    
    def step(self):
        # print("Hola")
        # print(self.__class__.__name__)
        pass
        
class CellNK(InIScell):
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model, mu, sigma)
        self.antiTumor = True
        
    def recruit(self):
        if  self.interactionRecruit():
            cell = CellNK(self.model.next_id(), self.model, self.mu, self.sigma)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
        
    def step(self):
        self.recruit()
        # self.attack()
        
        
    
    
class CellM(InIScell):
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2):
        super().__init__(unique_id, model, mu, sigma)
        self.antiTumor = True
        self.prProTumor = np.random.normal(mu2,sigma2)
        self.mu2 = mu2
        self.sigma2 = sigma2
        
    def recruit(self):
        if self.interactionRecruit():
            cell = CellM(self.model.next_id(), self.model, self.mu, self.sigma, self.mu2, self.sigma2)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
            
    def stepConditional(self):
        if self.antiTumor:
            self.recruit()
            self.attack()
            self.becomeM2()
            
    def becomeM2(self):
        if (self.prProTumor >= np.random.normal(0,1)):
            self.antiTumor = False
            

class CellN(InIScell):
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2):
        super().__init__(unique_id, model, mu, sigma)
        self.antiTumor = True
        self.prProTumor = np.random.normal(mu2,sigma2)
        self.mu2 = mu2
        self.sigma2 = sigma2
        
    def recruit(self):
        if self.interactionRecruit():
            cell = CellM(self.model.next_id(), self.model, self.mu, self.sigma, self.mu2, self.sigma2)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
        
    def stepConditional(self):
        if self.antiTumor:
            self.recruit()
            self.attack()
            self.becomeN2()
            
    def becomeN2(self):
        if (self.prProTumor >= np.random.normal(0,1)):
            self.antiTumor = False

class AdIScell(mesa.Agent):
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model)
        self.prRecruit = np.random.normal(mu,sigma)
        
        self.sigma = sigma
        self.mu = mu
        
        self.n = 1
    
    def interactionRecruit(self):
        return self.prRecruit >= np.random.normal(0,1)
    
    def step(self):
        pass

class TCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model, mu, sigma)
        self.prAttack = np.random.normal(mu,sigma)
    
    def recruit(self):
        if self.interactionRecruit():
            cell = TCell(self.model.next_id, self.model, self.mu, self.sigma)
            self.model.schedule.add(cell)
    
    def interactionAttack(self):
        return self.prAttack >= np.random.normal(0,1)
    
    def Attack(self, tumorCell):
        if  self.interactionAttack():
            self.model.schedule.remove(tumorCell)
            self.model.grid.remove_agent(self)

class ThCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model, mu, sigma)
    
    def recruit(self):
        if self.interactionRecruit():
            cell = ThCell(self.model.next_id, self.model, self.mu, self.sigma)
            self.model.schedule.add(cell)

class TregCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma):
        super().__init__(unique_id, model, mu, sigma)
    
    def recruit(self):
        if self.interactionRecruit():
            cell = TregCell(self.model.next_id, self.model, self.mu, self.sigma)
            self.model.schedule.add(cell)