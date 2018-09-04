import numpy as np 

def getPrimSecTert(bondOrderM,rings, atomI):

    primIndices = np.nonzero(bondOrderM[atomI])[0]
    secIndices = []

    for i in primIndices:
        indices = np.nonzero(bondOrderM[i])[0]
        indices = [x for x in indices if (x not in primIndices and x != atomI)]

        #if indices!= []:
        secIndices.append(indices)

    tertIndices = []
    secflat=[x for y in secIndices for x in y]
    for i in secflat:               # flattend
        x = []
# =============================================================================
#         for j in i:
#             indices = np.nonzero(bondOrderM[j])[0]
#             indices = [x for x in indices if (x not in primIndices and x not in np.array(secIndices).flatten() and x != atomI)]
# #            x.append(indices)
# =============================================================================
        indices = np.nonzero(bondOrderM[i])[0]
        indices = [x for x in indices if (x not in primIndices and x not in secflat and x != atomI)]
            #if indices!= []:
        tertIndices.append(indices)


    return primIndices, secIndices, tertIndices


def getAtomBeta(bondOrderM, rings, atomI, atomsList):
    prim, sec, tert = getPrimSecTert(bondOrderM, rings, atomI)
    secflat=[x for y in sec for x in y]
    d_C = {"C-C": {'P': 1.052, "S": 0.999, "T":1.000},
        "C-H": { 'P': 1.028, "S": 0.997, "T":1.000},
        "C=C":{'P': 1.078, "S": 1.000, "T":1.000},
        "C-triple-C":{'P':1.087, 'S':1.000, 'T':1.000}}
    print(sec)
    d_H = {"C-C": { "S": 1.102, "T":0.986},                           # Added parameters for hyrdogen
        "C-H": { "S": 0.993, "T":0.991},
        "H-C": { 'P': 11.625, "S": 0.993, "T":0.991},
        "C=C":{'S': 0.994, "T": 0.989}}
    
    atomEl = atomsList[atomI]
    if atomEl=='C':
        primBondProduct = 1
        for i in prim:
            if bondOrderM[atomI][i]==1:
                iEl = atomsList[i]
                bond = atomEl + "-" + iEl
                primBondProduct *= d_C[bond]['P']
            elif bondOrderM[atomI][i]==2:
                iEl = atomsList[i]
                bond = atomEl + "=" + iEl
                primBondProduct *= d_C[bond]['P']
            elif bondOrderM[atomI][i]==3:
                iEl = atomsList[i]
                bond = atomEl + "-triple-" + iEl
                primBondProduct *= d_C[bond]['P']
        secBondProduct  = 1
        for i, x in enumerate(sec):
            primEl = atomsList[prim[i]]
            for j in x:
                if bondOrderM[prim[i]][j]==1:
                    secEl = atomsList[j]
                    bond = primEl + "-" + secEl 
                    secBondProduct *= d_C[bond]['S']
                if bondOrderM[prim[i]][j]==2:
                    secEl = atomsList[j]
                    bond = primEl + "=" + secEl 
                    secBondProduct *= d_C[bond]['S']
                if bondOrderM[prim[i]][j]==3:
                    secEl = atomsList[j]
                    bond = primEl + "-triple-" + secEl 
                    secBondProduct *= d_C[bond]['S']
        tertBondProduct = 1
        for i, x in enumerate(tert):
            secEl = atomsList[secflat[i]]
            for j in x:
                if bondOrderM[secflat[i]][j]==1:
                    tertEl = atomsList[j]
                    bond = secEl + "-" + tertEl 
                    tertBondProduct *= d_C[bond]['T']
                if bondOrderM[secflat[i]][j]==2:
                    tertEl = atomsList[j]
                    bond = secEl + "=" + tertEl 
                    tertBondProduct *= d_C[bond]['T']
                if bondOrderM[secflat[i]][j]==3:
                    tertEl = atomsList[j]
                    bond = secEl + "-triple-" + tertEl 
                    tertBondProduct *= d_C[bond]['T']                    
    elif atomEl=='H':
        primBondProduct = 1
        for i in prim:
            if bondOrderM[atomI][i]==1:
                iEl = atomsList[i]
                bond = atomEl + "-" + iEl
                primBondProduct *= d_H[bond]['P']
            if bondOrderM[atomI][i]==2:
                iEl = atomsList[i]
                bond = atomEl + "=" + iEl
                primBondProduct *= d_H[bond]['P']                
    
        secBondProduct  = 1
        for i, x in enumerate(sec):
            primEl = atomsList[prim[i]]
            for j in x:
                if bondOrderM[prim[i]][j]==1:
                    secEl = atomsList[j]
                    bond = primEl + "-" + secEl 
                    secBondProduct *= d_H[bond]['S']
                if bondOrderM[prim[i]][j]==2:
                    secEl = atomsList[j]
                    bond = primEl + "=" + secEl 
                    secBondProduct *= d_H[bond]['S']                    
    
        tertBondProduct = 1
        for i, x in enumerate(tert):
            secEl = atomsList[secflat[i]]
            for j in x:
                if bondOrderM[secflat[i]][j]==1:
                    tertEl = atomsList[j]
                    bond = secEl + "-" + tertEl 
                    tertBondProduct *= d_H[bond]['T']
                if bondOrderM[secflat[i]][j]==2:
                    tertEl = atomsList[j]
                    bond = secEl + "=" + tertEl 
                    tertBondProduct *= d_H[bond]['T']
    return primBondProduct * secBondProduct * tertBondProduct


def getBetas(bondOrderM, rings, atomsList):
    betas = []

    for a in range(len(atomsList)):
        b = getAtomBeta(bondOrderM, rings, a, atomsList)
        betas.append(b)

    return betas