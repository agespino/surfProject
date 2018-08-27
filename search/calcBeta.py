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

	for i in secIndices:
		x = []
		for j in i:
			indices = np.nonzero(bondOrderM[j])[0]
			indices = [x for x in indices if (x not in primIndices and x not in np.array(secIndices).flatten() and x != atomI)]
			x.append(indices)

			#if indices!= []:
		tertIndices.append(indices)


	return primIndices, secIndices, tertIndices


def getAtomBeta(bondOrderM, rings, atomI, atomsList):
	prim, sec, tert = getPrimSecTert(bondOrderM, rings, atomI)

	d = {"C-C": {'P': 1.052, "S": 0.999, "T":1.000},
		"C-H": { 'P': 1.028, "S": 0.997, "T":1.000},
		"H-C": { 'P': 11.625, "S": 0.993, "T":.0991}}

	atomEl = atomsList[atomI]

	primBondProduct = 1
	for i in prim:
		iEl = atomsList[i]
		bond = atomEl + "-" + iEl
		primBondProduct *= d[bond]['P']

	secBondProduct  = 1
	for i, x in enumerate(sec):
		primEl = atomsList[i]
		for j in x:
			secEl = atomsList[j]
			bond = primEl + "-" + secEl 
			secBondProduct *= d[bond]['S']

	tertBondProduct = 1
	for i, x in enumerate(tert):
		secEl = atomsList[i]
		for j in x:
			tertEl = atomsList[j]
			bond = secEl + "-" + tertEl 
			tertBondProduct *= d[bond]['T']

	return primBondProduct * secBondProduct * tertBondProduct


def getBetas(bondOrderM, rings, atomsList):
	betas = []

	for a in range(len(atomsList)):
		b = getAtomBeta(bondOrderM, rings, a, atomsList)
		betas.append(b)

	return betas
