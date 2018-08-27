
from rdkit import Chem

class Molecule:
	def __init__(inchiStr):
		self.mol = Chem.inchi.MolFromInchi(inchiStr)
		self.symmEquivalence = Chem.CanonicalRankAtoms(self.mol)

	def getConnectivityMatrix():
		matrixHs = Chem.rdmolops.GetAdjacencyMatrix(Chem.AddHs(mol))
		return matrixHs



