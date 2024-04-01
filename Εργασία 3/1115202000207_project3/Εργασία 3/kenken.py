from csp import *

class CAGE :
    def __init__(self, variables, op, result):
        self.variables = variables
        self.op = op
        self.result = result

    def getOp(self):
        return self.op
    
    def getVars(self):
        return self.variables
    
    def get_neighbours_by_cage(self,var):
        return_vars = list(self.variables)
        return_vars.remove(var)
        return return_vars
    
    # returns true if value == result of cage
    def have_solution_eq(self,value):
            if value == self.result :
                return True
            return False
        
    # return true if curr_val and combination of all remain_var[currdomains[i]] for all i have at least one solution of cage puzzle   
    def has_solution_add_mul_eq(self, remain_var, curr_val, currdomains):
        if len(remain_var) == 0:
            return curr_val == self.result
        for value in currdomains[remain_var[0]]:
            if self.getOp() == '+':
                new_value = value + curr_val
                boolvar = self.has_solution_add_mul_eq(remain_var[1:], new_value, currdomains)
                if boolvar == True:  
                    return True
            if self.getOp() == "*":
                new_value = value * curr_val
                boolvar = self.has_solution_add_mul_eq(remain_var[1:], new_value, currdomains)
                if boolvar == True:  
                    return True
        return False
    
    # return true if curr_val and combination of remain_var[currdomains[i]] for all i have at least one solution of cage puzzle  
    def has_solution_div_sub(self, var, curr_val, currdoms):
        if len(var) == 0:
            if self.getOp() == '-':
                return curr_val == self.result
            if self.getOp() == '/':
                return curr_val == float(self.result)
        else:
            for value in currdoms[var[0]]:
                if self.getOp() == '-':
                    return value - curr_val == self.result or curr_val - value == self.result
                if self.getOp() == '/':
                    if value == 0:
                        return value == self.result
                    elif curr_val == 0:
                        return curr_val == self.result
                    else:
                        return value / curr_val == self.result or curr_val / value == self.result
    
class kenken (CSP) :
    def __init__(self,string):
        #get data of kenkel puzzle
        [n,number,operators,cages] = self.split(string)
        self.n = n
        num_of_cages = len(cages)
        num_of_variables = n*n;
        self.variables = [i for i in range(num_of_variables)]
        self.domains = {var: [i+1 for i in range(n)] for var in self.variables}
        
        #initiate cages
        self.Cages = []
        for i in range(num_of_cages):
            self.Cages.append(CAGE(cages[i],operators[i],number[i]))
        # neighbours of colums and rows
        self.neighbors = {var: self.same_cols_vars(var) + self.same_rows_vars(var) for var in self.variables}
        
        # neighbours of cages
        for var in self.variables:
            for cage in self.Cages:
                if var in cage.getVars():
                    self.neighbors[var] = self.neighbors[var] + cage.get_neighbours_by_cage(var)
        CSP.__init__(self,self.variables,self.domains,self.neighbors,self.f)
        self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
        for var in self.variables:
            self.neighbors[var] = list(dict.fromkeys(self.neighbors[var]))
        
    # slpit function decode input kenkel puzzle and return info about it
    def split(self,string):
        lines = []
        with open(string,"r") as f:
            lines = [line.rstrip() for line in f]
        n = int(lines[0])
        lines.pop(0)
        number = []
        operators = []
        cages = []
        for str in lines:
            t = str.split('#', 1)[0]
            number.append(int(t))
            str =  str[len(t):]
            operators.append(str[len(str)-1])
            str = str[1:len(str)-2]
            full_number = ''
            tuple = ()
            for char in str:
                if char != '-':
                    full_number = full_number + char
                else:
                    tuple = tuple + (int(full_number),)
                    full_number = ''
            tuple = tuple + (int(full_number),)
            cages.append(tuple)
        return [n,number,operators,cages]
    
    # return varibales in same row with variable
    def same_rows_vars(self,variable):
        rows = []
        for i in range(self.n):
            rows = self.variables[i*self.n:(i+1)*self.n]
            if (variable in rows):
                rows.remove(variable)
                return rows
    
    # return varibales in same colume with variable          
    def same_cols_vars(self,variable):
        for i in range(self.n):
            cols = []
            for j in range(0,self.n*self.n,self.n):
                cols.append(i+j)
            if (variable in cols):
                cols.remove(variable)
                return cols       

    # find cage of var
    def findCage(self, var):
        for cage in self.Cages:
            if var in cage.getVars():
                return cage
    
    # constaits function
    def f(self,A, a, B, b):
        
        # check if varibales are in same row and col and have the same value
        A_col = self.same_cols_vars(A)
        A_row = self.same_rows_vars(A)
        if (B in A_col or B in A_row) and a == b:
            return False
        
        # check if variables are in equal cage and if at least one of 2 values aren't equal with cage value
        Acage = self.findCage(A)
        Bcage = self.findCage(B)
        Aflag = True
        Bflag = True
        Acagevars = list(Acage.getVars())
        Bcagevars = list(Bcage.getVars())
        if len(Acagevars) == 1:
            Aflag = Acage.have_solution_eq(a)
        if len(Bcagevars) == 1:
            Bflag = Bcage.have_solution_eq(b)
        if len(Acagevars) == 1 or len(Bcagevars) == 1:
            return Aflag and Bflag
        
        # check if variables are in same cage and call right funcitons to check if exist solution
        if Acage == Bcage:
            Acagevars.remove(A)
            Acagevars.remove(B)
            
            if Acage.getOp() == '+':
                return Acage.has_solution_add_mul_eq(Acagevars, a + b, self.curr_domains)
            if Acage.getOp() == '*':
                return Acage.has_solution_add_mul_eq(Acagevars, a * b, self.curr_domains)
            if Acage.getOp() == '-':
                return Acage.has_solution_div_sub(Acagevars, a - b, self.curr_domains) or Acage.has_solution_div_sub(Acagevars, b - a, self.curr_domains)
            if Acage.getOp() == '/':
                return Acage.has_solution_div_sub(Acagevars, a/b, self.curr_domains) or Acage.has_solution_div_sub(Acagevars, b/a, self.curr_domains)
        return True

import time

# solve a list of problems and prints an array with results
def solver(problems, algorithmn, select_unassigned_variable, inf=no_inference):
    return_list = []
    for i in range(len(problems)):
        start_problem = time.time()
        AC3(problems[i])
        print(algorithmn(problems[i],select_unassigned_variable, inference=inf))   
        end_problem = time.time()
        return_list.append((end_problem - start_problem,problems[i].nassigns))
    return return_list

# solve problems with min_conflicts func
def solver_min_conflicts(problems):
    return_list = []
    for i in range(len(problems)):
        start_problem = time.time()
        AC3(problems[i])
        print(min_conflicts(problems[i],1000))
        end_problem = time.time()
        return_list.append((end_problem - start_problem,problems[i].nassigns))
    return return_list

e1 = kenken("rqeyqs_folder/Kenkel-3-easy");
e2 = kenken("rqeyqs_folder/Kenken-4-Hard.txt")
e3 = kenken("rqeyqs_folder/Kenken-5-Hard.txt")
e4 = kenken("rqeyqs_folder/Kenken-6-Hard.txt")
e5 = kenken("rqeyqs_folder/Kenken-7-Hard-1.txt")
e6 = kenken("rqeyqs_folder/Kenken-7-Hard-2.txt")
e7 = kenken("rqeyqs_folder/Kenken-8-Hard-1.txt")
e8 = kenken("rqeyqs_folder/Kenken-8-Hard-2.txt")
e9 = kenken("rqeyqs_folder/Kenken-9-Hard-1.txt")
e10 = kenken("rqeyqs_folder/Kenken-9-Hard-2.txt")
problems = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]

results = []
print("mrv,fc")
results.append(solver(problems, backtracking_search, mrv, forward_checking))
print("mrv,mac")
results.append(solver(problems, backtracking_search, mrv, mac))
print("min conficts")
results.append(solver_min_conflicts(problems))


# print array of results by solving all problems
print("      mrv/fc       mrv/mac     min_conflicts")
Total_times = 0
Total_assigns = 0
for i in range(len(problems)):
    print("e" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(results)):
        print(str('%.8f' % results[j][i][0]) + "s ", end='')
        Total_times += results[j][i][0]
    print("")
print("      mrv/fc       mrv/mac     min_conflicts")
for i in range(len(problems)):
    print("e" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(results)):
        print(str(results[j][i][1]) + " assigns ", end='')
        Total_assigns += results[j][i][1]
    print("")