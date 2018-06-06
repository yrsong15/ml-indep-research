

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
    

if __name__=='__main__':
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
    
