import mesa
import numpy as np

# Cambios
# : se añade el módulo 1 ( % 1 ) a los valores de los parámetros que no pueden ser 
# menores a 0

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
        self.noCells = 1
        self.antiTumor = False
        
        self.Beta = np.random.normal(self.mu, self.sigma)
        self.a = 10*self.Beta - 1 
        
    
    def updateCluster(self):
        self.noCells = (self.noCells * self.a * np.e**(-self.k *(self.model.schedule.time - self.t0) ) )/(1 + np.e**(-self.k *(self.model.schedule.time - self.t0) ))**2
        # print(self.noCells)
        

    def growth(self):
        newCells = int(self.a/(1 + np.e**(-self.k*(self.model.schedule.time - self.t0))))
        for i in range(newCells):
            cell = CancerCell(self.model.next_id(), self.model, self.mu, self.sigma, self.k, self.t0)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
        
    def step(self):
        self.updateCluster()
        # self.growth()
        if self.interaction():
            self.model.contNKAttack += 1
            
    def interaction(self):
        return self.prAntiProd >= np.random.uniform(0,1)
    

class InIScell(mesa.Agent):
    width = 0
    height = 0
    def __init__(self, unique_id, model, mu, sigma, maxAge):
        super().__init__(unique_id, model)
        self.antiTumor = True
        self.prRecruit = np.random.normal(mu,sigma)
        self.prAttack = np.random.normal(mu,sigma)
        
        self.sigma = sigma
        self.mu = mu
        
        self.n = 1
        self.age = int(np.random.normal(50,20))
        self.maxAge = maxAge
    
    def interactionRecruit(self):
        return self.prRecruit >= np.random.uniform(0,1)
    
    def interactionAttack(self):
        return self.prAttack >= np.random.uniform(0,1)
    
    def die(self):
        if self.maxAge <= self.age:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
        
class CellNK(InIScell):
    def __init__(self, unique_id, model, mu, sigma,maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.t0 = 0.5
        self.k = 4
        self.noCells = 1
        
    def recruit(self):
        if  self.interactionRecruit():
            cell = CellNK(self.model.next_id(), self.model, self.mu, self.sigma, self.maxAge)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
    
    def attack(self):
        if self.model.contNKAttack > 0 :
            self.model.contN1Attack += 1
            self.model.contM1Attack += 1
            if self.interactionAttack():
                CCs = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CancerCell']
                if len(CCs):
                    CC = self.random.choice(CCs)
                    CC.noCells -= 1 
                    # CC.noCells = CC.noCells - CC.a/(1 + np.e**(-CC.k *(CC.model.schedule.time - CC.t0) ))
                    if CC.noCells < 1:
                        self.model.grid.remove_agent(CC)
                        self.model.schedule.remove(CC)
        self.model.contNKAttack = (self.model.contNKAttack - 1) % 1
    
    def step(self):
        if 33 < self.age < 77:
            # self.recruit()
            self.attack()
        self.die()
        
class CellM(InIScell):
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2, maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.prProTumor = np.random.normal(mu2,sigma2)
        self.mu2 = mu2
        self.sigma2 = sigma2
        self.maxAge = {True:maxAge[0],False:maxAge[1]}
        
    def recruit(self):
        if self.interactionRecruit():
            cell = CellM(self.model.next_id(), self.model, self.mu, self.sigma, self.mu2, self.sigma2, self.maxAge)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
            
    def becomeM2(self):
        if (self.prProTumor >= np.random.uniform(0,1)):
            self.antiTumor = False
            
    def attack(self):
        if self.model.contM1Attack > 0 & self.interactionAttack():
            CCs = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CancerCell']
            if len(CCs):
                CC = self.random.choice(CCs)
                CC.noCells -= 1
                if CC.noCells < 1:
                    self.model.grid.remove_agent(CC)
                    self.model.schedule.remove(CC)
        self.model.contM1Attack = (self.model.contM1Attack - 1) % 1
    
    def die(self):
        if self.maxAge[self.antiTumor] <= self.age:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
    
    def step(self):
        if self.antiTumor:
            if 33 < self.age < 77:
                # self.recruit()
                self.attack()
            self.becomeM2()
        self.die()
        
            

class CellN(InIScell):
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2, maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.prProTumor = np.random.normal(mu2,sigma2)
        self.mu2 = mu2
        self.sigma2 = sigma2
        self.maxAge = {True:maxAge[0],False:maxAge[1]}
        
    def recruit(self):
        if self.interactionRecruit():
            cell = CellM(self.model.next_id(), self.model, self.mu, self.sigma, self.mu2, self.sigma2, self.maxAge)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
    
    def attack(self):
        if self.model.contN1Attack > 0 & self.interactionAttack():
            CCs = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CancerCell']
            if len(CCs):
                CC = self.random.choice(CCs)
                CC.noCells -= 1
                if CC.noCells < 1:
                    self.model.grid.remove_agent(CC)
                    self.model.schedule.remove(CC)
        self.model.contN1Attack = (self.model.contN1Attack - 1) % 1
    
    def die(self):
        if self.maxAge[self.antiTumor] <= self.age:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
    
    def step(self):
        if self.antiTumor:
            if 33 < self.age < 77:
                self.recruit()
                self.attack()
                self.becomeN2()
        self.die()
            
    def becomeN2(self):
        if (self.prProTumor >= np.random.normal(0,1)):
            self.antiTumor = False

class AdIScell(mesa.Agent):
    width = 0
    height = 0
    def __init__(self, unique_id, model, mu, sigma, maxAge):
        super().__init__(unique_id, model)
        self.antiTumor = True
        self.prRecruit = np.random.normal(mu,sigma)
        
        self.sigma = sigma
        self.mu = mu
        
        self.n = 1
        self.age = int(np.random.normal(50,20))
        self.maxAge = maxAge
        
    def die(self):
        if self.maxAge <= self.age:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        self.age += 1
    
    def interactionRecruit(self):
        return self.prRecruit >= np.random.uniform(0,1)


class TCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma,maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.prAttack = np.random.normal(mu,sigma)
    
    def recruit(self):
        if self.interactionRecruit():
            cell = TCell(self.model.next_id, self.model, self.mu, self.sigma, self.maxAge)
            self.model.schedule.add(cell)
    
    def interactionAttack(self):
        return self.prAttack >= np.random.uniform(0,1)
    
    def Attack(self):
        if self.model.contTAttack > 0 & self.interactionAttack():
            CCs = [elem for elem in self.model.grid.get_cell_list_contents([self.pos]) if elem.__class__.__name__ == 'CancerCell']
            if len(CCs):
                CC = self.random.choice(CCs)
                CC.noCells -= 1
                if CC.noCells < 1:
                    self.model.grid.remove_agent(CC)
                    self.model.schedule.remove(CC)
        self.model.contTAttack = (self.model.contTAttack - 1) % 1 

    def step(self):
        if 33 < self.age < 77:
            self.Attack()
        self.die()
        # self.recruit()
            
    
class ThCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma,maxAge):
        super().__init__(unique_id, model, mu, sigma,maxAge)
        self.prStrenght = np.random.normal(mu,sigma)
        
    
    def recruit(self):
        if self.interactionRecruit():
            cell = ThCell(self.model.next_id, self.model, self.mu, self.sigma, self.maxAge)
            self.model.schedule.add(cell)
            
    def strengthening(self):
        if self.prStrenght >= np.random.uniform(0,1):
            self.model.contTAttack += 1
    
    def step(self):
        # self.recruit()
        if 33 < self.age < 77:
            self.strengthening()
        self.die()

class TregCell(AdIScell):
    def __init__(self, unique_id, model, mu, sigma, maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.prStrenght = np.random.normal(mu,sigma)
    
    def recruit(self):
        if self.interactionRecruit():
            cell = TregCell(self.model.next_id, self.model, self.mu, self.sigma, self.maxAge)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
            
    def strengthening(self):
        if self.prStrenght >= np.random.uniform(0,1):
            self.model.contTAttack += 1
    
    def step(self):
        if 33 < self.age < 77:
            self.strengthening()
        # self.recruit()
        self.die()