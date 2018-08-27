import re
import sys
import numpy as np
from rdkit import Chem

# returns a list of atoms orderd by how htey are numbered using InChI convention 
# ex: ethanol ( InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3.  ) retunrs the list 
# ['C', 'C', 'O', 'H', 'H', 'H', 'H', 'H', 'H' ]
# use this with our matrices to map index. to atom 
def atomsList(inchiString):
	layers = inchiString.split('/')
	form = layers[1]
	# the molecular formula layer of the inchi
	splitForm = re.findall('[A-Z][a-z]*|\d*', form)
	# string of formula split into elements and numbers
	# ex: C5H11BrO would give us the list ['C', '5', 'H', '11', 'Br', 'O', '']

	hFreqs = 0

	afterElem = False # Tells us whther the item cause directly after an element 
	lastElem = ''

	atoms = []
	elemFreqTups = {}

	for item in splitForm: 
		if(item.isdigit()):
			# its a frequency 
			if(lastElem == 'H' ):
				hFreqs += int(item)
			else: 
				atoms.extend([lastElem] * int(item))
				elemFreqTups[lastElem] = int(item)
			afterElem = False
		else: 
			# its an element!
			if(afterElem == True and lastElem == 'H'):
			# it comes after a H not a number 
				hFreqs += 1
			elif(afterElem == True):
			# it comes after an element not a number 
				atoms.append(lastElem)

			if(item == 'H'):
				afterH = True
			
			lastElem = item
			afterElem = True

	# add in H's at the end
	atoms.extend(['H']*hFreqs)
	elemFreqTups['H'] =  hFreqs
	return atoms

def getConnectivityMatrix(inchiStr):
	mol = Chem.inchi.MolFromInchi(inchiStr)
	matrixHs = Chem.rdmolops.GetAdjacencyMatrix(Chem.AddHs(mol))
	return matrixHs

def getDistanceMatrix(inchiStr):
	mol = Chem.inchi.MolFromInchi(inchiStr)
	matrixHs = Chem.rdmolops.GetAdjacencyMatrix(mol) # ignore hydroges to make SSSR finding easier 
	return matrixHs

def getLabeledM(matrix, labels, showHs, printTriangleMatrix):
		if showHs:
			atoms = labels
		else:
			firstH = labels.index("H")
			atoms = labels[0:firstH]
			matrix = matrix[:firstH,:firstH]


		toPrint = np.char.mod('%d', matrix)
		if printTriangleMatrix: 
			for i in range(len(toPrint)):
				for j in range(len(toPrint)):
					if i > j:
						toPrint[i][j] = " "
		toPrint = np.insert(toPrint, 0, atoms, axis = 0)

		
		
		rowLabels = [' ']
		rowLabels.extend(atoms)
		toPrint = np.insert(toPrint, 0, rowLabels, axis = 1)
	
		return(toPrint)

def getRowSums(matrix, atoms):
	sums = []
	i = 0
	for row in matrix:
		sums.append(np.sum(row))
	return sums

elemBondsD = {"C": 4, "N": 4, "O": 4, "H": 1}


def countsPartnersMissingBonds(atomRow, atomIndex, toFix):
	count = 0
	for i in range(len(atomRow)):
		partner = atomRow[i]
		if partner != 0:
			# theres actually a bond between partner and atomIndex
			if i in toFix:
				# partner is also missing bonds: 
				count += 1
	return count

def getPartnersMissingBonds(toFix, matrix):

	partnersLsts = []

	for i in range(len(matrix)):
		if i not in toFix:
			partnersLsts.append([])
		else:
			atomRow = matrix[i]
			temp = [] 
			for j in range(len(atomRow)):
				if atomRow[j] != 0 and j in toFix:
					temp.append(j)
			partnersLsts.append(temp)
	return partnersLsts


def removeFromPartnersList(partnersLsts, toRemoveIndx):
	partnersLsts[toRemoveIndx] = []
	for i in range(len(partnersLsts)): 
		partnersLsts[i] = list(filter(lambda x: x!= 2, partnersLsts[i]))
	return partnersLsts


def markAromatic(rings, connectivityMatrix, atoms):
	markers = [''] * np.shape(connectivityMatrix)[0]

	for r in rings:
		allMissingBonds = True 
		for atm in r: 
			if np.sum(connectivityMatrix[atm]) ==  elemBondsD[atoms[atm]]:
				allMissingBonds = False
		if allMissingBonds == True:
			for atm in r: 
				markers[atm] += "\AR=y"
	return markers 


def getRings(mol):
	sssr =  Chem.GetSymmSSSR(mol)

	rings = []

	for i in range(len(sssr)):
		rings.append(set(sssr[i]))

	return rings

def getRingSys(rings):
	pass

def getSymmClasses(mol):

	ranks = list(Chem.CanonicalRankAtoms(mol, breakTies=False))
	print('ranks: ', ranks)
	rankUniVals = set(ranks)

	if len(ranks) == len(rankUniVals):
		print("no equivalents")
		return []


	symmGroups = []

	for rankVal in rankUniVals:
		symmGroup = [i for i, x in enumerate(ranks) if x == rankVal]
		symmGroups.append(list(symmGroup))

	return symmGroups


def findBondWeightsM(matrix, atoms, inchiStr):
	atomProps = [''] * len(atoms) 
	# keeps track of special properties of an atoms(participates in a aromatic ring, double bond, etc)
	# ADD
	bondsM = np.copy(matrix)
	atomSums = getRowSums(matrix, atoms)
	rings = getRings(Chem.inchi.MolFromInchi(inchiStr))
	markers = markAromatic(rings, matrix, atoms)
	print("mARKERS", markers)

	toFix = []

	for i, bondCount in enumerate(atomSums): 
		currElem = atoms[i]
		# print('currElem: ', currElem)
		if currElem in elemBondsD:
			if elemBondsD[currElem] != bondCount:
				toFix.append(i)

	# iterate over the atoms involved in an aromatic ring and 
	# remove these from toFix
	print(toFix)

	for i, mark in enumerate(markers):
		if re.search('\\\\AR=y', mark):
			toFix.remove(i)


	if len(toFix) == 0:
		return bondsM 

	partnersMissingBondsLists = getPartnersMissingBonds(toFix, bondsM)
	# contains i lists of atoms that atom i is bonded to that are also missing bonds

	counts = [(i, len(item)) for i, item in enumerate(partnersMissingBondsLists) if len(item) > 0]
	# will fill with tuples (index of atom to fix, count of partners with missing bonds > 0
	hasOnePartnerMissingBonds = [ i for i, item in enumerate(partnersMissingBondsLists) if len(item) == 1]
	# indices of atoms toFix that have only one partner that is also  missing bonds 
	#print()
	#print(toFix)
	#print(partnersMissingBondsLists)
	#print(hasOnePartnerMissingBonds)
	
	done  = False
	lastToFix = None
	while not done:
		for atomIndx in list.copy(hasOnePartnerMissingBonds): 
			if(len(partnersMissingBondsLists[atomIndx]) == 0): 
				# at some point in this for loop the current atom became full 
				continue 
			# add bonds to atom until full
			bondCount = atomSums[atomIndx]
			toAdd = elemBondsD[atoms[atomIndx]] - bondCount
			atomSums[atomIndx] += toAdd
			# Update the partner 
			partnerIndx = partnersMissingBondsLists[atomIndx][0]
			atomSums[partnerIndx] += toAdd
			# Update bonds Matrix 
			bondsM[atomIndx][partnerIndx] += toAdd
			bondsM[partnerIndx][atomIndx] += toAdd
			# update partnerMissingBondLists (remove instances of atomIndx in partnersMissingBondsLists and update counts)
			# also remove things from toFix
			partnersMissingBondsLists = removeFromPartnersList(partnersMissingBondsLists, atomIndx)
			toFix.remove(atomIndx)

			if( atomSums[partnerIndx] ==  elemBondsD[atoms[partnerIndx]]):
				partnersMissingBondsList = removeFromPartnersList(partnersMissingBondsLists, partnerIndx)
				toFix.remove(partnerIndx)
			hasOnePartnerMissingBonds = [ i for i, item in enumerate(partnersMissingBondsLists) if len(item) == 1]


		if(len(toFix) == 0) or len(toFix) == 1:
			done = True 

		if lastToFix == toFix:
			done = True

		lastToFix = toFix

		print(atoms, toFix)

	return bondsM



