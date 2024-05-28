# Importing numpy library to solve system of equations
import numpy as np

# Defining a function to frame matrix A which is filled with the co-efficients of KCL and KVL equations
def matrixA(v,r,nodeindex,gnd):
    A = np.zeros((len(nodeindex)+len(v),len(nodeindex)+len(v)))
    for a in r:
        A[nodeindex[a['node1']]][nodeindex[a['node1']]]+=(1/a['value'])
        A[nodeindex[a['node1']]][nodeindex[a['node2']]]-=(1/a['value'])
        A[nodeindex[a['node2']]][nodeindex[a['node1']]]-=(1/a['value'])
        A[nodeindex[a['node2']]][nodeindex[a['node2']]]+=(1/a['value'])
    for b in v:
        A[len(nodeindex)+v.index(b)][nodeindex[b['node1']]] = 1.0
        A[len(nodeindex)+v.index(b)][nodeindex[b['node2']]] = -1.0
        A[nodeindex[b['node1']]][len(nodeindex)+v.index(b)] = 1.0
        A[nodeindex[b['node2']]][len(nodeindex)+v.index(b)] = -1.0  
    M = []
    # Removing the row and column corresponding to the Ground node
    for m in range(len(A)):
        temp = []
        if m!=gnd:
            for n in range(len(A[m])):
                if n!=gnd:
                    temp.append(A[m][n])
            M.append(temp)
    return M

# Defining a function to frame matrix B which consists of the RHS values of the equations
def matrixB(v,i,nodeindex,gnd):
    B = np.zeros(len(nodeindex)+len(v))
    for a in v:
        B[len(nodeindex)+v.index(a)] = a['value']
    for b in i:
        B[nodeindex[b['node1']]] = b['value']
        B[nodeindex[b['node2']]] = (-1)*b['value']
    M = []
    for i in range(len(B)):
        if i!=gnd:
            M.append(B[i])
    return M

# Function which solves for node voltages and currents passing through voltage sources
def evalSpice(filename):
    # Creating empty lists and dictionaries to store the information about the circuit components and the nodes
    vsources,isources,resistors = [],[],[]
    nodesckt,nodenums={},{}
    try:
        # Appending the lines in to a list by ignoring the comments
        lines = []
        with open(filename,"r") as f:
            for line in f.readlines():
                lines.append(line.split('#')[0].split('\n')[0])
        
        in_ckt = False
        ckt = []
        # The below code appends the information which is in between '.circuit' and '.end'.
        for i in lines:
            if i == '.circuit':
                in_ckt = True
            elif i == '.end':
                in_ckt = False
            elif in_ckt:
                if len(i)!=0:
                    ckt.append(i)
        
        # Checking whether the circuit description begins with '.circuit' and ends with '.end'
        # If not it is a malformed circuit and hence len(ckt) is equal to zero
        if len(ckt)==0:
            raise ValueError("Malformed circuit file")
            
        # Error: If there is an unnecessary information about a component
        for t in ckt:
            o = t.split()
            if len(o)!=4 and len(o)!=5:
                raise ValueError("Malformed circuit file")
        
        # Adding the data of the components into their respective dictionaries
        for i in ckt:
            words = i.split()
            if words[0][0]!='#':
                if words[0][0]!='V' and words[0][0]!='R' and words[0][0]!='I':
                    raise ValueError("Only V, I, R elements are permitted")
                else:
                    if words[0][0]=='V':
                        vsources.append({'name':words[0],'node1':words[1],'node2':words[2],'value':float(words[4])})
                    elif words[0][0]=='I':
                         isources.append({'name':words[0],'node1':words[1],'node2':words[2],'value':float(words[4])})
                    elif words[0][0]=='R':
                        if words[3]!=0:
                              resistors.append({'name':words[0],'node1':words[1],'node2':words[2],'value':float(words[3])})
                    
                    # Collecting the nodes into a dictionary
                    if words[1] not in nodesckt:
                        nodesckt[words[1]]=0
                    if words[2] not in nodesckt:
                        nodesckt[words[2]]=0
                    
                    # Checking whether the GND is present
                    if 'GND' not in nodesckt:
                        raise ValueError("No Ground Node")
                        
                    # Assigning the indices to the nodes
                    count = 0
                    for num in nodesckt:
                        nodenums[num] = count
                        if num == 'GND': gndnode = count
                        count+=1 
            else:
                raise ValueError("Wrong circuit format")   
        
        # Forming the matrices 'a' and 'b' using the functions defined at the start of the code
        a = matrixA(vsources,resistors,nodenums,gndnode)
        b = matrixB(vsources,isources,nodenums,gndnode)
        
        # Solving for the unknown variables
        # Unknown variables are node voltages and currents through voltage sources
        # It raises an error if 'a' is a singular matrix
        try:
            result = np.linalg.solve(a,b)
            finalresult = np.insert(result,gndnode,0)
        except np.linalg.LinAlgError:
            raise ValueError("Circuit error: no solution")
            
        # The values of the unknown variables are adding into dictionaries with their node name.
        voltages_nodes = {}
        currents_vsources = {}
        for i in nodenums:
            voltages_nodes[i] = finalresult[nodenums[i]]
        for j in vsources:
            currents_vsources[j['name']] = finalresult[len(nodenums)+vsources.index(j)]
            
        return voltages_nodes,currents_vsources
    
    # Raises FileNotFoundError if the python file wouldn't able to find the input file.
    except FileNotFoundError:
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")