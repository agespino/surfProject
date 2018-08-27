
def shortestPath():
	pass


def findRingStructs(connectivityMatrix, distanceMatrix):
	# Step 1. Take information from a graph with M vertices and N edges.

	# Step 2. Remove all open acyclic nodes with one edge 
	#	(connectivity equal to 1, corresponding to terminal nodes) and repeat the procedure, 
	#	stoping at nodes with a connectivity larger than 1. Now, M and N become m and n, respectively.

	atomsRemove = []

	while True:
		updates = False 
		for i, row in enumerate(connectivityMatrix):
			if np.sum(row) == 1: 
				updates = True 
				# remove this atom from the connectivity matrix 
				atom2 = np.where(row == 1)
				connectivityMatrix[i][atom2] == 0
				connectivityMatrix[atom2][i] == 0
				# updatae the distance matrix:
				distanceMatrix[i] = 0
				distanceMatrix[:, i] = 0
		if updates = False:
			break

	# Step 3. Calculate the theoretical number of SSSR : nSSSR = m − n + 1, If nSSSR = 0, stop process.
	m =  np.count_nonzero(connectivityMatrix) # number of edges 
	n = sum(np.all(arr, axis = 1)) # number of vertices still connected
	nSSSR = m - n + 1

	# Step 4. Calculate the PID matrices Pe and Pe′.

	# Pe stores all of the possible shortest paths with a length of dij between vertices i and j. 
	# Pe′ stores all paths that have one more vertex than the shortest paths with a length of dij + 1

	# Step 5. Create the cycle set([Cnum, Pe[i,j], Pe′[i,j]]) using the PID matrices. 
	#	Cases in which the shortest path number equals zero, or [|Pe[i,j]| = 1 and |Pe′[i,j] = 0] can be omitted.

	# Step 6. Order the cycle set by Cnum number.

	# REpeat steps 7 to 9 
	while True : 
		# Step 7. Construct ring using the PID matrix from the smallest-membered rings.

		# Step 8. Use the XOR operation to find the SSSR from this ring.

		# Step 9. If a ring is a new member of the SSSR, then save it.

		# Step 10. Repeat steps 7 to 9, until nringidx reaches nSSSR, where nringidx is the number of founded SSSR.
		if  nringidx == nSSSR: 
			break

	return sssrList
	pass
