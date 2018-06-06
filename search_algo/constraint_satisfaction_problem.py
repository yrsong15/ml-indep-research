from collections import defaultdict
from sys import maxint
import time

globalCount = 0

class Constraint:
    """A constraint of a CSP.  Members include
     - name: a string for debugging
     - domain, a list of variables on which the constraint acts
     - predicate, a boolean function with the same arity as the domain.
     """
    def __init__(self,name,domain,pred):
        self.name = name
        self.domain = domain
        self.predicate = pred
        
    def isSatisfied(self,vars):
        """Given a dictionary of variables, evaluates the predicate.
        If a variable in the domain isn't present, raises a KeyError."""
        args = [vars[v] for v in self.domain]
        return self.predicate(*args)

class CSP:
    """Defines a constraint satisfaction problem.  Contains 4 members:
    - variables: a list of variables
    - domains: a dictionary mapping variables to domains
    - constraints: a list of Constraints.
    - incidentConstraints: a dict mapping each variable to a list of
      constraints acting on it.
    """
    
    def __init__(self,variables=[],domains=[]):
        """Input: a list of variables and a list of domains.

        Note: The variable names must be unique, otherwise undefined behavior
        will result.
        """
        self.variables = variables[:]
        self.domains = dict(zip(variables,domains))
        self.constraints = []
        self.incidentConstraints = dict((v,[]) for v in variables)
        
    def addVariable(self,var,domain):
        """Adds a new variable with a given domain.  var must not already
        be present in the CSP."""
        if var in self.domains:
            raise ValueError("Variable with name "+val+" already exists in CSP")
        self.variables.append(var)
        self.domains[var] = domain
        self.incidentConstraints[var] = []

    def addConstraint(self,varlist,pred,name=None):
        """Adds a constraint with the domain varlist, the predicate pred,
        and optionally a name for printing."""
        if name==None:
            name = "c("+",".join(str(v) for v in varlist)+")"
        self.constraints.append(Constraint(name,varlist,pred))
        for v in varlist:
            self.incidentConstraints[v].append(self.constraints[-1])

    def addUnaryConstraint(self,var,pred,name=None):
        """Adds a unary constraint with the argument var, the predicate pred,
        and optionally a name for printing."""
        self.addConstraint((var,),pred,name)

    def addBinaryConstraint(self,var1,var2,pred,name=None):
        """Adds a unary constraint with the arguments (var1,var2), the
        predicate pred, and optionally a name for printing."""
        self.addConstraint((var1,var2),pred,name)

    def fixValue(self,var,value,name=None):
        """Adds a constraint that states var = value."""
        if name==None:
            name = str(var)+'='+str(value)
        self.addUnaryConstraint(var,lambda x:x==value,name)

    def nAryConstraints(self,n,var=None):
        """Returns a list of all n-ary constraints in the CSP if var==None,
        or if var is given, returns a list of all n-ary constraints involving
        var."""
        if var==None:
            return [c for c in self.constraints if len(c.domain)==n]
        else:
            return [c for c in self.incidentConstraints[var] if len(c.domain)==n]

    def incident(self,*vars):
        """incident(var1,...,varn) will return a list of constraints
        that involve all of var1 to varn."""
        if len(vars)==0: return self.constraints
        res = set(self.incidentConstraints[vars[0]])
        for v in vars[1:]:
            res &= set(self.incidentConstraints[v])
        return [c for c in res]

    def isConstraintSatisfied(self,c,partialAssignment):
        """Checks if the partial assignment satisfies the constraint c.
        If the partial assignment doesn't cover the domain, this returns
        None. """
        try:
            res = c.isSatisfied(partialAssignment)
            return res
        except KeyError:
            return None

    def isValid(self,partialAssignment,*vars):
        """Checks if the assigned variables in a partial assignment
        are mutually compatible.  Only checks those constraints
        involving assigned variables, and ignores any constraints involving
        unassigned ones.

        If no extra arguments are given, checks all constraints relating
        assigned variables.
        
        If extra arguments var1,...,vark are given, this only checks
        constraints that are incident to those given variables."""
        for c in self.incident(*vars):
            #all entries in partialAssignment must be in the domain of c
            #for this to be checked
            if self.isConstraintSatisfied(c,partialAssignment)==False:
                return False
        return True

def allDiff(a,b,c,d,e):
    return a!=b and a!=c and a!=d and a!=e and b!=c and b!=d and b!=e and c!=d and c!=e and d!=e

def streetCSP():
    nationalityVars = ['N1','N2','N3','N4','N5']
    colorVars = ['C1','C2','C3','C4','C5']
    drinkVars = ['D1','D2','D3','D4','D5']
    jobVars = ['J1','J2','J3','J4','J5']
    animalVars = ['A1','A2','A3','A4','A5']
    nationalities = ['E','S','J','I','N']
    colors = ['R','G','W','Y','B']
    drinks = ['T','C','M','F','W']
    jobs = ['P','S','Di','V','Do']
    animals = ['D','S','F','H','Z']
               
    csp = CSP(nationalityVars+colorVars+drinkVars+jobVars+animalVars,
              [nationalities]*5+[colors]*5+[drinks]*5+[jobs]*5+[animals]*5)
    
    #1. Englishman lives in the red house
    for Ni,Ci in zip(nationalityVars,colorVars):
        csp.addBinaryConstraint(Ni,Ci,lambda x,y:(x=='E')==(y=='R'),'Englishman lives in the red house')
    #3. Japanese is a painter
    for Ni,Ji in zip(nationalityVars,jobVars):
        csp.addBinaryConstraint(Ni,Ji,lambda x,y:(x=='J')==(y=='P'),'Japanese is a painter')
    #5. Norwegian lives in first house
    csp.fixValue('N1','N','Norwegian lives in the first house')
    #7. green house is to the right of the white house
    for Ci,Cn in zip(colorVars[:-1],colorVars[1:]):
        csp.addBinaryConstraint(Ci,Cn,lambda x,y:(x=='W')==(y=='G'),'Green house is to the right of the white house')
    csp.addUnaryConstraint('C5',lambda x:x!='W','Green house is to the right of the white house')
    csp.addUnaryConstraint('C1',lambda x:x!='G','Green house is to the right of the white house')
    
    #2. The Spaniard has a Dog
    for Ni, Ai in zip(nationalityVars, animalVars):
        csp.addBinaryConstraint(Ni, Ai, lambda x,y:(x=='S')==(y=='D'), 'Spainiard has a dog')
    #4. Italian drinks Tea
    for Ni, Di in zip(nationalityVars, drinkVars):
        csp.addBinaryConstraint(Ni, Di, lambda x,y:(x=='I')==(y=='T'), 'Italian drinks tea')
    #6. Green house owner drinks coffee
    for Ci, Di in zip(colorVars, drinkVars):
        csp.addBinaryConstraint(Ci, Di, lambda x,y:(x=='G')==(y=='C'), 'Green house owner drinks coffee')
    #8. Sculptor breeds snails
    for Ji, Ai in zip(jobVars, animalVars):
        csp.addBinaryConstraint(Ji, Ai, lambda x,y:(x=='S')==(y=='S'), 'Sculptor breeds snails')
    #9. Diplomat lives in yellow house
    for Ji, Ci in zip(jobVars, colorVars):
        csp.addBinaryConstraint(Ji, Ci, lambda x,y:(x=='Di')==(y=='Y'), 'Diplomat lives in yellow house')
    # #10. Middle house owner drinks milk
    csp.fixValue('D3','M','Middle house owner drinks milk')
    # #11. Norwegian lives next to Blue House
    for Ni, Ci1, Ci2 in zip(nationalityVars[1:-1], colorVars[:-2], colorVars[2:]):
        varlist = [Ni, Ci1, Ci2]
        csp.addConstraint(varlist, lambda x,y,z:(x=='N')==(y=='B') or (x=='N')==(z=='B'), 'Norwegian lives next to Blue House')
    csp.addBinaryConstraint('N1','C2',lambda x,y:(x=='N')==(y=='B'), 'Norwegian lives next to blue house')
    csp.addBinaryConstraint('N5','C4', lambda x,y:(x=='N')==(y=='B'), 'Norwegian lives next to blue house')
    # #12. Violinist drinks Fruit Juice
    for Ji, Di in zip(jobVars, drinkVars):
        csp.addBinaryConstraint(Ji, Di, lambda x,y:(x=='V')==(y=='F'),'Violinist drinks Fruit Juice')
    # #13. Fox is next to doctor
    for Ai, Ji1, Ji2 in zip(animalVars[1:-1], jobVars[:-2], jobVars[2:]):
        varlist = [Ai, Ji1, Ji2]
        csp.addConstraint(varlist, lambda x,y,z:(x=='F')==(y=='Do') or (x=='F')==(z=='Do'), 'Fox is next to doctor')
    csp.addBinaryConstraint('A1','J2', lambda x,y:(x=='F')==(y=='Do'), 'Fox is next to doctor')
    csp.addBinaryConstraint('A5','J4', lambda x,y:(x=='F')==(y=='Do'), 'Fox is next to doctor')
    # #14. Horse is next to diplomat
    for Ai, Ji1, Ji2 in zip(animalVars[1:-1], jobVars[:-2], jobVars[2:]):
        varlist = [Ai, Ji1, Ji2]
        csp.addConstraint(varlist, lambda x,y,z:(x=='H')==(y=='Di') or (x=='H')==(z=='Di'), 'Horse is next to diplomat')
    csp.addBinaryConstraint('A1','J2', lambda x,y:(x=='H')==(y=='H'), 'Horse is next to diplomat')
    csp.addBinaryConstraint('A5','J4', lambda x,y:(x=='Di')==(y=='Di'), 'Horse is next to diplomat')
    #allDiff
    csp.addConstraint(nationalityVars, allDiff, 'All elements of list must be unique')
    csp.addConstraint(colorVars, allDiff, 'All elements of list must be unique')
    csp.addConstraint(jobVars, allDiff, 'All elements of list must be unique')
    csp.addConstraint(drinkVars, allDiff, 'All elements of list must be unique')
    csp.addConstraint(animalVars, allDiff, 'All elements of list must be unique')

    print "CSP has",len(csp.constraints),"constraints"
    return csp

def p1():
    csp = streetCSP()
    solution = dict([('A1', 'F'), ('A2', 'H'), ('A3', 'S'), ('A4', 'D'), ('A5', 'Z'),
                     ('C1', 'Y'), ('C2', 'B'), ('C3', 'R'), ('C4', 'W'), ('C5', 'G'),
                     ('D1', 'W'), ('D2', 'T'), ('D3', 'M'), ('D4', 'F'), ('D5', 'C'),
                     ('J1', 'Di'), ('J2', 'Do'), ('J3', 'S'), ('J4', 'V'), ('J5', 'P'),
                     ('N1', 'N'), ('N2', 'I'), ('N3', 'E'), ('N4', 'S'), ('N5', 'J')])
    invalid1 = dict([('A1', 'F'), ('A2', 'H'), ('A3', 'S'), ('A4', 'D'), ('A5', 'Z'),
                     ('C1', 'Y'), ('C2', 'B'), ('C3', 'R'), ('C4', 'W'), ('C5', 'G'),
                     ('D1', 'T'), ('D2', 'W'), ('D3', 'M'), ('D4', 'F'), ('D5', 'C'),
                     ('J1', 'Di'), ('J2', 'Do'), ('J3', 'S'), ('J4', 'V'), ('J5', 'P'),
                     ('N1', 'N'), ('N2', 'I'), ('N3', 'E'), ('N4', 'S'), ('N5', 'J')])
    invalid2 = dict([('A1', 'F'), ('A2', 'F'), ('A3', 'S'), ('A4', 'D'), ('A5', 'Z'),
                     ('C1', 'Y'), ('C2', 'B'), ('C3', 'R'), ('C4', 'W'), ('C5', 'G'),
                     ('D1', 'W'), ('D2', 'T'), ('D3', 'M'), ('D4', 'F'), ('D5', 'C'),
                     ('J1', 'Di'), ('J2', 'Do'), ('J3', 'S'), ('J4', 'V'), ('J5', 'P'),
                     ('N1', 'N'), ('N2', 'I'), ('N3', 'E'), ('N4', 'S'), ('N5', 'J')])
    print "Valid assignment valid?",csp.isValid(solution)
    print "Invalid assignment valid?",csp.isValid(invalid1)
    print "Invalid assignment valid?",csp.isValid(invalid2)

############################  Problem 2 code below #######################

class CSPBacktrackingSolver:
    """ A CSP solver that uses backtracking.
    A state is a partial assignment dictionary {var1:value1,...,vark:valuek}.
    Also contains a member oneRings that is a dict mapping each variable to
    all variables that share a constraint.
    """
    def __init__(self,csp,doForwardChecking=True,doConstraintPropagation=False):
        self.csp = csp
        self.doForwardChecking = doForwardChecking
        self.doConstraintPropagation = doConstraintPropagation
        #compute 1-rings
        self.oneRings = dict((v,set()) for v in csp.variables)
        for c in csp.constraints:
            cdomain = set(c.domain)
            for v in c.domain:
                self.oneRings[v] |= cdomain
        for v in csp.variables:
            if v in self.oneRings[v]:
                self.oneRings[v].remove(v)

    def solve(self):
        """Solves the CSP, returning an assignment if solved, or False if
        failed."""
        domains = self.initialDomains()
        return self.search({},domains)

    def search(self,partialAssignment,domains):
        global globalCount
        globalCount += 1
        """Runs recursive backtracking search."""
        if len(partialAssignment)==len(self.csp.variables):
            return partialAssignment
        if self.doConstraintPropagation:
            domains = self.constraintPropagation(partialAssignment,domains)
            #contradiction detected
            if any(len(d)==0 for (v,d) in domains.iteritems()):
                return False
        indent = " "*len(partialAssignment)
        X = self.pickVariable(partialAssignment,domains)
        values = self.orderValues(partialAssignment,domains,X)
        for v in values:
            partialAssignment[X] = v
            if self.doForwardChecking:
                print indent+"Trying",X,"=",v
                #do forward checking
                newDomains = self.forwardChecking(partialAssignment,X,domains)
                if any(len(d)==0 for (v,d) in newDomains.iteritems()):
                    #contradiction, go on to next value
                    emptyvars = [v for (v,d) in newDomains.iteritems() if len(d)==0]
                    print indent+" Forward checking found contradiction on",emptyvars[0]
                    del partialAssignment[X] #ADDED
                    continue
                #recursive call
                res = self.search(partialAssignment,newDomains)
                if res!=False: return res
            else:
                #check whether the assignment X=v is valid
                if self.csp.isValid(partialAssignment,X):
                    print indent+"Trying",X,"=",v
                    #recursive call
                    res = self.search(partialAssignment,domains)
                    if res!=False: return res
            #remove the partial assignment to X, backtrack
            del partialAssignment[X]
        return False
        
    def initialDomains(self):
        """Does the basic step of checking all unary constraints"""
        domains = dict()
        for v,domain in self.csp.domains.iteritems():
            #save only valid constraints
            vconstraints = self.csp.nAryConstraints(1,v)
            dvalid = [val for val in domain if all(c.predicate(val) for c in vconstraints)]
            domains[v] = dvalid
        return domains

    def pickVariable(self,partialAssignment,domains):
        """Return an unassigned variable to assign next"""
        minVal = maxint
        candidates = []
        for v,domain in domains.iteritems():
            if len(domain)<minVal and v not in partialAssignment:
                minVal = len(domain)
        for v,domain in domains.iteritems():
            if len(domains[v])==minVal and v not in partialAssignment:
                candidates.append(v)
        if len(candidates)==1:
            return candidates[0]
        notInCurrAssign = [x for x in domains.keys() if x not in partialAssignment.keys()]
        res = -1
        comp = -maxint
        for cand in candidates:
            tempCount = 0;
            for elem in notInCurrAssign:
                for c in self.csp.incidentConstraints[elem]:
                    if cand in c.domain:
                        tempCount = tempCount+1;
            if tempCount > comp:
                comp = tempCount
                res = cand
        return res

    def forwardChecking(self,partialAssignment,var,domains):
        """domains is a dict mapping vars to valid values.  var has just been
        assigned.
        Return a copy of domains but with all invalid values removed"""
        resdomain = dict()
        #do a shallow copy for all unaffected domains, this saves time
        for v,domain in domains.iteritems():
            resdomain[v] = domain
        resdomain[var] = [partialAssignment[var]]
        
        #uncomment this line to perform forward checking
        # return resdomain
        
        for c in self.csp.incidentConstraints[var]:
            #If the domain has size k and exactly k-1 entries are filled, then
            #do forward checking.  If so, 'unassigned' will contain the name of
            #the unassigned variable.
            kassigned = 0
            unassigned = None
            for v in c.domain:
                if v in partialAssignment:
                    kassigned += 1
                else:
                    unassigned = v
            if kassigned+1 == len(c.domain):
                #print "Forward checking",unassigned
                validvalues = []        
                for val in resdomain[unassigned]:
                    partialAssignment[unassigned] = val
                    if self.csp.isConstraintSatisfied(c, partialAssignment):
                        # print "VVV", val
                        validvalues.append(val)
                    else:
                        if val in validvalues:
                            validvalues.remove(val)
                    del partialAssignment[unassigned]
                resdomain[unassigned] = validvalues
                if len(validvalues)==0:
                    #early terminate, this setting is a contradiction
                    return resdomain
        return resdomain

def nQueensCSP(n):
    """Returns a CSP for an n-queens problem"""
    vars = ['Q'+str(i) for i in range(1,n+1)]
    domain = range(1,n+1)
    csp = CSP(vars,[domain]*len(vars))
    for i in range(1,n+1):
        for j in range(1,i):
            Qi = 'Q'+str(i)
            Qj = 'Q'+str(j)
            ofs = i-j
            #this weird default argument thing is needed for lambda closure
            csp.addBinaryConstraint(Qi,Qj,(lambda x,y: x!=y),Qi+"!="+Qj)
            csp.addBinaryConstraint(Qi,Qj,(lambda x,y,ofs=ofs: x!=(y+ofs)),Qi+"!="+Qj+"+"+str(i-j))
            csp.addBinaryConstraint(Qi,Qj,(lambda x,y,ofs=ofs: x!=(y-ofs)),Qi+"!="+Qj+"-"+str(i-j))
    return csp

def p2():
    # start_time = time.time()
    csp = nQueensCSP(4)
    solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=False)
    res = solver.solve()
    print "Result:",sorted(res.items())
    # elapsed_time = time.time() - start_time
    # print "Elapsed time: ", elapsed_time
    # global globalCount
    # print globalCount
    # globalCount = 0
    # print "Reset: ", globalCount
    raw_input()

    #TODO: implement forward checking, change False to True
    # start_time = time.time()
    csp = nQueensCSP(16)
    solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=False)
    res = solver.solve()
    print "Result:",sorted(res.items())
    # elapsed_time = time.time() - start_time
    # print "Elapsed time: ", elapsed_time
    # global globalCount
    # print globalCount
    # globalCount = 0
    # print "Reset: ", globalCount
    raw_input()

    # start_time = time.time()
    csp = nQueensCSP(50)
    solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # # solver = CSPBacktrackingSolver(csp,doForwardChecking=False)
    res = solver.solve()
    print "Result:",sorted(res.items())
    # elapsed_time = time.time() - start_time
    # print "Elapsed time: ", elapsed_time
    # global globalCount
    # print globalCount
    # globalCount = 0
    # print "Reset: ", globalCount
    # raw_input()

    # start_time = time.time()
    # csp = nQueensCSP(200)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # # solver = CSPBacktrackingSolver(csp,doForwardChecking=False)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # elapsed_time = time.time() - start_time
    # print "Elapsed time: ", elapsed_time
    # global globalCount
    # print globalCount
    # globalCount = 0
    # print "Reset: ", globalCount
    # raw_input()

    # csp = nQueensCSP(20)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 20')

    # csp = nQueensCSP(40)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 40')

    # csp = nQueensCSP(80)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 80')

    # csp = nQueensCSP(100)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 100')

    # csp = nQueensCSP(120)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 120')

    # csp = nQueensCSP(120)
    # solver = CSPBacktrackingSolver(csp,doForwardChecking=True)
    # res = solver.solve()
    # print "Result:",sorted(res.items())
    # raw_input('completed 120')


def marginalize(probabilities,index):
    """Given a probability distribution P(X1,...,Xi,...,Xn),
    return the distribution P(X1,...,Xi-1,Xi+1,...,Xn).
    - probabilities: a probability table, given as a map from tuples
      of variable assignments to values
    - index: the value of i.
    """
    #TODO (Problem 3): you may hard-code two routines for n=2 and n=3, but there's an
    #elegant solution that uses defaultdict(float)
    tupleSize = len(probabilities.keys()[0])
    newDict = {}
    if tupleSize==2:
        probTrue = 0
        probFalse = 0
        for key in probabilities.keys():
            if index==0:
                if key[1]: probTrue += probabilities[key]
                else: probFalse += probabilities[key]
            elif index ==1:
                if key[0]: probTrue += probabilities[key]
                else: probFalse += probabilities[key]
            else: raise ValueError('Incorrect index')
        newDict[(0,)] = probFalse
        newDict[(1,)] = probTrue

    elif tupleSize==3:
        pTT = 0
        pTF = 0
        pFT = 0
        pFF = 0
        for key in probabilities.keys():
            if index==0:
                if key[1] and key[2]: pTT += probabilities[key]
                elif key[1] and not key[2]: pTF += probabilities[key]
                elif not key[1] and key[2]: pFT += probabilities[key]
                else: pFF += probabilities[key]
            elif index==1:
                if key[0] and key[2]: pTT += probabilities[key]
                elif key[0] and not key[2]: pTF += probabilities[key]
                elif not key[0] and key[2]: pFT += probabilities[key]
                else: pFF += probabilities[key]
            elif index==2:
                if key[0] and key[1]: pTT += probabilities[key]
                elif key[0] and not key[1]: pTF += probabilities[key]
                elif not key[0] and key[1]: pFT += probabilities[key]
                else: pFF += probabilities[key]
            else: raise ValueError('incorrect index')
        newDict[(0,0)] = pFF
        newDict[(0,1)] = pFT
        newDict[(1,0)] = pTF
        newDict[(1,1)] = pTT
    else: raise ValueError('Key tuple size must be 2 or 3')
    return newDict

def marginalize_multiple(probabilities,indices):
    """Safely marginalizes multiple indices"""
    pmarg = probabilities
    for index in reversed(sorted(indices)):
        pmarg = marginalize(pmarg,index)
    return pmarg

def condition1(probabilities,index,value):
    """Given a probability distribution P(X1,...,Xi,...,Xn),
    return the distribution P(X1,...,Xi-1,Xi+1,...,Xn | Xi=v).
    - probabilities: a probability table, given as a map from tuples
      of variable assignments to values
    - index: the value of i.
    - value: the value of v
    """
    #TODO (Problem 3)
    #Compute the denominator by marginalizing over everything but Xi
    tupleSize = len(probabilities.keys()[0])
    indices = range(0, tupleSize)
    del indices[index]
    marg = marginalize_multiple(probabilities, indices)
    denom = marg[(value,)]
    newDict = {}
    if tupleSize==2:
        pT = 0
        pF = 0
        for key in probabilities.keys():
            if key[index]==value:
                if index==0:
                    if key[1]: pT += probabilities[key]
                    else: pF += probabilities[key]
                elif index==1:
                    if key[0]: pT += probabilities[key]
                    else: pF += probabilities[key]
                else: raise ValueError('Incorrect index')
        newDict[(0,)] = pF/denom
        newDict[(1,)] = pT/denom
    elif tupleSize==3:
        pTT = 0
        pTF = 0
        pFT = 0
        pFF = 0
        for key in probabilities.keys():
            if key[index]==value:
                if index==0:
                    if key[1] and key[2]: pTT += probabilities[key]
                    elif key[1] and not key[2]: pTF += probabilities[key]
                    elif not key[1] and key[2]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                elif index==1:
                    if key[0] and key[2]: pTT += probabilities[key]
                    elif key[0] and not key[2]: pTF += probabilities[key]
                    elif not key[0] and key[2]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                elif index==2:
                    if key[0] and key[1]: pTT += probabilities[key]
                    elif key[0] and not key[1]: pTF += probabilities[key]
                    elif not key[0] and key[1]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                else: raise ValueError9('Incorrect index')
        newDict[(0,0)] = pFF/denom
        newDict[(0,1)] = pFT/denom
        newDict[(1,0)] = pTF/denom
        newDict[(1,1)] = pTT/denom
    else: raise ValueError('Key tuple size must be 2 or 3')
    return newDict

def normalize(probabilities):
    """Given an unnormalized distribution, returns a normalized copy that
    sums to 1."""
    vtotal = sum(probabilities.values())
    return dict((k,v/vtotal) for k,v in probabilities.iteritems())

def condition2(probabilities,index,value):
    """Given a probability distribution P(X1,...,Xi,...,Xn),
    return the distribution P(X1,...,Xi-1,Xi+1,...,Xn | Xi=v).
    - probabilities: a probability table, given as a map from tuples
      of variable assignments to values
    - index: the value of i.
    - value: the value of v
    """
    #TODO (Problem 3)
    #Compute the result by normalizing
    tupleSize = len(probabilities.keys()[0])
    newDict = {}
    if tupleSize==2:
        pT = 0
        pF = 0
        for key in probabilities.keys():
            if key[index]==value:
                if index==0:
                    if key[1]: pT += probabilities[key]
                    else: pF += probabilities[key]
                elif index==1:
                    if key[0]: pT += probabilities[key]
                    else: pF += probabilities[key]
                else: raise ValueError('Incorrect index')
        newDict[(0,)] = pF
        newDict[(1,)] = pT
    elif tupleSize==3:
        pTT = 0
        pTF = 0
        pFT = 0
        pFF = 0
        for key in probabilities.keys():
            if key[index]==value:
                if index==0:
                    if key[1] and key[2]: pTT += probabilities[key]
                    elif key[1] and not key[2]: pTF += probabilities[key]
                    elif not key[1] and key[2]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                elif index==1:
                    if key[0] and key[2]: pTT += probabilities[key]
                    elif key[0] and not key[2]: pTF += probabilities[key]
                    elif not key[0] and key[2]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                elif index==2:
                    if key[0] and key[1]: pTT += probabilities[key]
                    elif key[0] and not key[1]: pTF += probabilities[key]
                    elif not key[0] and key[1]: pFT += probabilities[key]
                    else: pFF += probabilities[key]
                else: raise ValueError9('Incorrect index')
        newDict[(0,0)] = pFF
        newDict[(0,1)] = pFT
        newDict[(1,0)] = pTF
        newDict[(1,1)] = pTT
    else: raise ValueError('Key tuple size must be 2 or 3')
    return normalize(newDict)
    

def p4():
    pAB = {(0,0):0.5,
           (0,1):0.3,
           (1,0):0.1,
           (1,1):0.1}
    pA = marginalize(pAB,1)
    print (pA[(0,)],pA[(1,)]),"should be",(0.8,0.2)

    pABC = {(0,0,0):0.2,
            (0,0,1):0.3,
            (0,1,0):0.06,
            (0,1,1):0.24,
            (1,0,0):0.02,
            (1,0,1):0.08,
            (1,1,0):0.06,
            (1,1,1):0.04}

    print "marginalized p(A,B): ",dict(marginalize(pABC,2))
    pA = marginalize(marginalize(pABC,2),1)
    print (pA[(0,)],pA[(1,)]),"should be",(0.8,0.2)

    pA_B = condition1(pAB,1,1)
    print (pA_B[(0,)],pA_B[(1,)]),"should be",(0.75,0.25)
    pA_B = condition2(pAB,1,1)
    print (pA_B[(0,)],pA_B[(1,)]),"should be",(0.75,0.25)

    pAB_C = condition1(pABC,2,1)
    print "p(A,B|C): ",dict(pAB_C)
    pAB_C = condition2(pABC,2,1)
    print "p(A,B|C): ",dict(pAB_C)

    pA_BC = condition1(condition1(pABC,2,1),1,1)
    print "p(A|B,C): ",dict(pA_BC)
    pA_BC = condition2(condition2(pABC,2,1),1,1)
    print "p(A|BC): ",dict(pA_BC)

if __name__=='__main__':
    print "###### Problem 1 ######"
    p1()
    raw_input()
    print
    print "###### Problem 2 ######"
    p2()
    raw_input()
    print
    print "###### Problem 4 ######"
    p4()
    
