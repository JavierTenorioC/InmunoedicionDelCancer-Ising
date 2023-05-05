import mesa
import numpy as np
import math

# Cambios
# : se añade el módulo 1 ( % 1 ) a los valores de los parámetros que no pueden ser 
# menores a 0

def normpdf(x, args): # mean, sd
    var = float(args[1])**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(args[0]))**2/(2*var))
    return num/denom

class CancerCell(mesa.Agent):
    width = 0
    height = 0
    
    def __init__(self, unique_id, model, mu, sigma, k, t0):
        super().__init__(unique_id, model)
        # mu debe de ser pequeña, menor a 1
        # NOTA: dcambiar antigeno por neoantigeno
        self.prAntiProd = np.random.normal(mu,sigma)
        self.Beta = 0
        self.sigma = sigma
        self.mu = mu
        self.t0 = 0.5
        self.k = 4
        self.n = 1
        self.noCells = int(np.random.normal(mu,sigma)*10)
        self.antiTumor = False
        
        self.Beta = np.random.normal(self.mu, self.sigma)
        self.a = 10*self.Beta - 1 
        
    
    def updateCluster(self):
        self.Beta = np.random.normal(self.mu, self.sigma)
        self.noCells = (self.noCells * self.a * self.k * np.e**(-self.k *(self.model.schedule.time - self.t0) ) )/(1 + np.e**(-self.k *(self.model.schedule.time - self.t0) ))**2
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
        self.sigma = 0
        self.mu = 0 
        self.maxAge = maxAge
        
        # se calcula la edad según la fortaleza del sistema inmune
        # print(f'sigma {sigma}')
        # self.age = (int(np.random.normal(mu,1.05 - sigma)) % 1) + 1
        self.age = int(np.random.uniform(1,20))
        
        # se calcula  la distribución de probabilidad asociada a su edad
        # self.upDateDist()
        
        self.prRecruit = np.random.normal(mu,sigma)
        self.prAttack = np.random.normal(mu,sigma)
        
        self.n = 1
        
        
    
    def upDateDist(self):
        maxim = [0,'']
        for index in [*self.model.dictDistr]:
            try:
                n = normpdf(self.age/self.maxAge,self.model.dictDistr[index][0])
                if((n) >= maxim[0]):
                    maxim = [n, index]
            # print(f'age {self.age}')
            # print(f'{n} {type(n)} n')
            # print(f'{maxim[0]} {type(maxim[0])} maxim')
            except:
                print(f'edad Máxima: {self.maxAge}')
                print(f'edad: {self.age}')
            
        self.mu, self.sigma = self.model.dictDistr[maxim[1]][0]
    
    def interactionRecruit(self):
        return self.prRecruit >= np.random.uniform(0,1)
    
    def interactionAttack(self):
        return self.prAttack >= np.random.uniform(0,1)
    
    def die(self):
        flag = False
        if self.maxAge <= self.age:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            flag = True
        self.age += 1
        # self.upDateDist()
        return flag
        
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
            # ver si en lugar de hacer un contador, que la variable fuera booleana
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
        if self.die():
            self.model._contNKCells -= 1
        
class CellM(InIScell):
    def __init__(self, unique_id, model, mu, sigma, mu2, sigma2, maxAge):
        super().__init__(unique_id, model, mu, sigma, maxAge)
        self.prProTumor = np.random.normal(mu/(mu+mu2),sigma)
        self.mu2 = mu2
        self.sigma2 = sigma2
        self.maxAge = {True:maxAge[0],False:maxAge[1]}
        
    def recruit(self):
        if self.interactionRecruit():
            cell = CellM(self.model.next_id(), self.model, self.mu, self.sigma, self.mu2, self.sigma2, self.maxAge)
            self.model.schedule.add(cell)
            self.model.grid.place_agent(cell, (self.width,self.height))
            
    def upDateDist(self):
        maxim = [0,'']
        for index in [*self.model.dictDistr]:
            try :
                n = normpdf(self.age/self.maxAge[self.antiTumor],self.model.dictDistr[index][0])
                if((n) >= maxim[0]):
                    maxim = [n, index]
            # print(f'age {self.age}')
            # print(f'{n} {type(n)} n')
            # print(f'{maxim[0]} {type(maxim[0])} maxim')
            except:
                print(f'edad Máxima: {self.maxAge[self.antiTumor]}')
                print(f'edad: {self.age}')
            
        self.mu, self.sigma = self.model.dictDistr[maxim[1]][0]
    
    # La codificación sigue la tabla 4 para la probabilidad de 
    # que se convierta a pro tumoral
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
        self.prProTumor = np.random.normal(mu/(mu+mu2),sigma)
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
    
    def upDateDist(self):
        maxim = [0,'']
        for index in [*self.model.dictDistr]:
            try:
                n = normpdf(self.age/self.maxAge[self.antiTumor],self.model.dictDistr[index][0])
                if((n) >= maxim[0]):
                    maxim = [n, index]
            # print(f'age {self.age}')
            # print(f'{n} {type(n)} n')
            # print(f'{maxim[0]} {type(maxim[0])} maxim')
            except:
                print(f'edad Máxima: {self.maxAge}')
                print(f'edad: {self.age}')
            
        self.mu, self.sigma = self.model.dictDistr[maxim[1]][0]

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
        self.age = int(np.random.uniform(1,20))
        # self.age = int(np.random.normal(mu,sigma))
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