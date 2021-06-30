from time import time
import pyomo as pyEnv
import numpy as np

class ILP():
    def __init__(self, city):
        self.algorithm_name = 'ilp'
        self.scooters = city.scooters
        self.scenarios = city.scenarios
        self.nr_of_scenarios = city.nr_of_scenarios
        self.scenario_size = city.scenario_size
        
        self.run(self.scenarios)    
        
    def run(self, scenarios):
        t = time()
        n = len(self.scooters) #number of cities
        
        for i in range(len(scenarios)):
            scenarios[i] = list((scenarios[i] + np.ones(len(scenarios[i]))).astype(int))
        k = len(self.nr_of_scenarios)
        s = self.scenario_size
        probabilities = list(np.ones(k)/k)
        
        model2 = pyEnv.ConcreteModel()  
        model2.N = pyEnv.RangeSet(n)
        model2.M = pyEnv.RangeSet(n)
        model2.U = pyEnv.RangeSet(n) #ui = 1,...,10
        model2.P = pyEnv.RangeSet(k) #p = 1,...,3
        
        model2.x = pyEnv.Var(model2.P,model2.N,model2.M, within=pyEnv.Binary)
        model2.y = pyEnv.Var(model2.P,model2.N,model2.M, within=pyEnv.Binary)
        model2.u = pyEnv.Var(model2.U,within=pyEnv.NonNegativeIntegers,bounds=(1,n)) 
        model2.d = pyEnv.Param(model2.N, model2.M, within=pyEnv.Any, initialize = lambda model2, i, j: distance_matrix[i-1][j-1])
        model2.s = pyEnv.Param(model2.P, within=pyEnv.Any, initialize = lambda model2, k: scenarios[k-1])
        model2.p = pyEnv.Param(model2.P, within=pyEnv.Any, initialize = lambda model2, k: probabilities[k-1])
        
        def obj_func(model2):
            distance = 0
            for k in model2.P:
                scenario = model2.s[k]
                distance += sum(model2.p[k] * model2.d[i,j] * model2.x[k,i,j] for i in scenario for j in scenario)
            return distance

        model2.objective = pyEnv.Objective(rule = obj_func,sense=pyEnv.minimize)
         
        model2.S1 = scenarios[0]
        model2.S1_i = scenarios[0]
        model2.S1_j = scenarios[0]

        def s1_cont1(model2, S1_j):
            return sum(model2.x[1,i,S1_j] for i in model2.S1_i if i!=S1_j) == 1

        model2.const1_s1 = pyEnv.Constraint(model2.S1_j, rule=s1_cont1)

        def s1_cont2(model2, S1_i):
            return sum(model2.x[1,S1_i,j] for j in model2.S1_j if j!=S1_i) == 1

        model2.rest2_s1 = pyEnv.Constraint(model2.S1_i, rule=s1_cont2)

        def s1_cont3(model2):
            return sum(model2.y[1,i,j] for i in model2.S1_i for j in model2.S1_j if i!=j) == 1

        model2.rest3_s1 = pyEnv.Constraint(rule=s1_cont3)

        def s1_cont5(model2,i,j):
            if i!=j:
                return model2.u[i] - model2.u[j] + n*model2.x[1,i,j] - n*model2.y[1,i,j] <= n-1 
            else:
                return model2.u[i] - model2.u[i] == 0 

        model2.rest5_s1 = pyEnv.Constraint(model2.S1_i, model2.S1_j, rule=s1_cont5)
        
        model2.S2 = scenarios[1]
        model2.S2_i = scenarios[1]
        model2.S2_j = scenarios[1]        

        def s2_cont1(model2, S2_j):
            return sum(model2.x[2,i,S2_j] for i in model2.S2_i if i!=S2_j) == 1

        model2.const1_s2 = pyEnv.Constraint(model2.S2_j, rule=s2_cont1)

        def s2_cont2(model2, S2_i):
            return sum(model2.x[2,S2_i,j] for j in model2.S2_j if j!=S2_i) == 1

        model2.rest2_s2 = pyEnv.Constraint(model2.S2_i, rule=s2_cont2)

        def s2_cont3(model2):
            return sum(model2.y[2,i,j] for i in model2.S2_i for j in model2.S2_j if i!=j) == 1

        model2.rest3_s2 = pyEnv.Constraint(rule=s2_cont3)

        def s2_cont5(model2, i, j):
            if i != j:
                return model2.u[i] - model2.u[j] + n*model2.x[2,i,j] - n*model2.y[2,i,j] <= n-1 
            else:
                return model2.u[i] - model2.u[i] == 0 

        model2.rest5_s2 = pyEnv.Constraint(model2.S2_i, model2.S2_j, rule=s2_cont5)

        solver = pyEnv.SolverFactory('glpk')
        result = solver.solve(model2,tee = False)

        path_temp=[i for i in l if model2.x[i]() not in [0, None]]
                
        path_temp = list(set(path_temp))
        self.tour = path_temp
        self.stsp_length = model2.objective()