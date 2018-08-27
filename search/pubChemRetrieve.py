import pubchempy as pcp

# query type is a string, either 'name', 'smiles' or 'inchi'
# returns tuple (iupac name, inchi string, iupac_name)

def getCompound(query, queryType): 
    # retrieve from pub chem by name 
 	results = pcp.get_compounds(query, queryType)
 	print(results)

 	# for now pick the first result 
 	if len(results) == 0:
 		return None
 	c = results[0]

 	return (c.iupac_name, c.inchi, c.canonical_smiles)

def getResults(query, queryType):
	cids = pcp.get_cids(query, queryType, 'substance', list_return='flat')
	results = [pcp.Compound.from_cid(cid) for cid in cids]
	return results
