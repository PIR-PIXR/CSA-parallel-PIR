'''2. Call SealPIR on the whole tree h times parallel - O(2n)
3. Each Merkle proof as one element - O(hn)
4. Call SealPIR on each layer and wait for the slowest - O(n)
5. Probabilistic Batch Code SealPIR - O(6n/1.5h)
6. Balanced ancestral coloring - O(2n/h)'''

import matplotlib.pyplot as plt

REP = 1
step = 5
jump = REP*step+1
network_bandwidth = 100000000 #800 Mbps

#2. Call SealPIR on the whole tree h times parallel - O(2n)
WholeTree_Comp = [] #ms
WholeTree_Query = [] #bytes
WholeTree_Anwer = [] #bytes
WholeTree_Comm = [] #bytes
WholeTree_cipher = [] #number
#3. Each Merkle proof as one element - O(hn)
OneProof_Comp = []
OneProof_Query = [] #bytes
OneProof_Anwer = [] #bytes
OneProof_Comm = [] #bytes
OneProof_cipher = [] #number
#4. Call SealPIR on each layer and wait for the slowest - O(n)
Layer_Comp = [] #ms
Layer_Query = [] #bytes
Layer_Anwer = [] #bytes
Layer_Comm = [] #bytes
Layer_cipher = [] #number
#5. Probabilistic Batch Code SealPIR - O(6n/1.5h)
PBC_Comp = [] #ms
PBC_Query = [] #bytes
PBC_Anwer = [] #bytes
PBC_Comm = [] #bytes
PBC_cipher = [] #number
#6. Balanced ancestral coloring - O(2n/h)
Color_Comp = [] #ms
Color_Query = [] #bytes
Color_Anwer = [] #bytes
Color_Comm = [] #bytes
Color_cipher = [] #number

#Read data from text file
with open('output2.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height2 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        height2.append(int(lines[i].strip()))

        for j in range(1, jump, step):
            WholeTree_Comp.append(int(lines[i + j].strip()))
            WholeTree_Query.append(int(lines[i + j + 1].strip()))
            WholeTree_Anwer.append(int(lines[i + j + 2].strip()))
            WholeTree_Comm.append(int(lines[i + j + 3].strip()))
            WholeTree_cipher.append(int(lines[i + j + 4].strip()))

#Read data from text file
with open('output3.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height3 = []

    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        height3.append(int(lines[i].strip()))

        for j in range(1, jump, step):
            OneProof_Comp.append(int(lines[i + j].strip()))
            OneProof_Query.append(int(lines[i + j + 1].strip()))
            OneProof_Anwer.append(int(lines[i + j + 2].strip()))
            OneProof_Comm.append(int(lines[i + j + 3].strip()))
            OneProof_cipher.append(int(lines[i + j + 4].strip()))

#Read data from text file
with open('output4.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height4 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        height4.append(int(lines[i].strip()))

        for j in range(1, jump, step):
            Layer_Comp.append(int(lines[i + j].strip()))
            Layer_Query.append(int(lines[i + j + 1].strip()))
            Layer_Anwer.append(int(lines[i + j + 2].strip()))
            Layer_Comm.append(int(lines[i + j + 3].strip()))
            Layer_cipher.append(int(lines[i + j + 4].strip()))

#Read data from text file
with open('output5.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height5 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        height5.append(int(lines[i].strip()))

        for j in range(1, jump, step):
            PBC_Comp.append(int(lines[i + j].strip()))
            PBC_Query.append(int(lines[i + j + 1].strip()))
            PBC_Anwer.append(int(lines[i + j + 2].strip()))
            PBC_Comm.append(int(lines[i + j + 3].strip()))
            PBC_cipher.append(int(lines[i + j + 4].strip()))

#Read data from text file
with open('output6.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height6 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        height6.append(int(lines[i].strip()))

        for j in range(1, jump, step):
            Color_Comp.append(int(lines[i + j].strip()))
            Color_Query.append(int(lines[i + j + 1].strip()))
            Color_Anwer.append(int(lines[i + j + 2].strip()))
            Color_Comm.append(int(lines[i + j + 3].strip()))
            Color_cipher.append(int(lines[i + j + 4].strip()))

#Average REP times
def average(array):
    result = []
    n = len(array)
    for i in range(0, n, REP):
        chunk = array[i:i+REP]
        avg = sum(chunk) / len(chunk)
        result.append(avg)
    return result

Avg_WholeTree_Comp = average(WholeTree_Comp)
Avg_WholeTree_Comm = average(WholeTree_Comm)
Avg_WholeTree_Query = average(WholeTree_Query)
Avg_WholeTree_Anwer = average(WholeTree_Anwer)
Avg_WholeTree_cipher = average(WholeTree_cipher)

Avg_OneProof_Comp = average(OneProof_Comp)
Avg_OneProof_Comm = average(OneProof_Comm)
Avg_OneProof_Query = average(OneProof_Query)
Avg_OneProof_Anwer = average(OneProof_Anwer)
Avg_OneProof_cipher = average(OneProof_cipher)

Avg_Layer_Comp = average(Layer_Comp)
Avg_Layer_Comm = average(Layer_Comm)
Avg_Layer_Query = average(Layer_Query)
Avg_Layer_Anwer = average(Layer_Anwer)
Avg_Layer_cipher = average(Layer_cipher)

Avg_PBC_Comp = average(PBC_Comp)
Avg_PBC_Comm = average(PBC_Comm)
Avg_PBC_Query = average(PBC_Query)
Avg_PBC_Anwer = average(PBC_Anwer)
Avg_PBC_cipher = average(PBC_cipher)

Avg_Color_Comp = average(Color_Comp)
Avg_Color_Comm = average(Color_Comm)
Avg_Color_Query = average(Color_Query)
Avg_Color_Anwer = average(Color_Anwer)
Avg_Color_cipher = average(Color_cipher)

#Convert bytes to bits and calcualte communication cost in ms
WholeTree_Comm_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_WholeTree_Comm]
WholeTree_Query_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_WholeTree_Query]
WholeTree_Anwer_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_WholeTree_Anwer]

OneProof_Comm_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_OneProof_Comm]
OneProof_Query_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_OneProof_Query]
OneProof_Anwer_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_OneProof_Anwer]

Layer_Comm_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Layer_Comm]
Layer_Query_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Layer_Query]
Layer_Anwer_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Layer_Anwer]

PBC_Comm_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_PBC_Comm]
PBC_Query_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_PBC_Query]
PBC_Anwer_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_PBC_Anwer]

Color_Comm_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Color_Comm]
Color_Query_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Color_Query]
Color_Anwer_Cost = [element * 8 * 1000/network_bandwidth for element in Avg_Color_Anwer]

#Total communication and commupuation costs
Total_WholeTree_Cost = [Avg_WholeTree_Comp[i] + WholeTree_Comm_Cost[i] for i in range(len(WholeTree_Comm_Cost))]
Total_OneProof_Cost = [Avg_OneProof_Comp[i] + OneProof_Comm_Cost[i] for i in range(len(OneProof_Comm_Cost))]
Total_Layer_Cost = [Avg_Layer_Comp[i] + Layer_Comm_Cost[i] for i in range(len(Layer_Comm_Cost))]
Total_PBC_Cost = [Avg_PBC_Comp[i] + PBC_Comm_Cost[i] for i in range(len(PBC_Comm_Cost))]
Total_Color_Cost = [Avg_Color_Comp[i] + Color_Comm_Cost[i] for i in range(len(Color_Comm_Cost))]
#Total communication cost in ms of the trivial solution (Download the whole Merkle tree)
Trival_Comm_Cost = [(2 * (2 ** element) - 2) * 32 * 8 * 1000/network_bandwidth for element in height2]

num_leave = [2 ** element for element in height2]

'''THE PERCENTAGE OF THE COMPUTATION TIME (SERVER + CLIENT) WITH RESPECT TO THE WHOLE RUNNING TIME
(COMPUTATION + COMMUNICATION) IN OUR COLORING-BASED SCHEME ASSUMING THE NETWORK BANDWIDTH
BETWEEN THE SERVER AND CLIENT IS 100 MBPS.'''
Color_TotalComp_per_TotalCompComm = [Avg_Color_Comp[i] * 100/Total_Color_Cost[i] for i in range(len(Total_Color_Cost))]
print(Color_TotalComp_per_TotalCompComm)

# Plotting
plt.plot(num_leave, Trival_Comm_Cost, label='Trivial (100 Mbps)')
plt.plot(num_leave, Total_WholeTree_Cost, label='h-time-WholeTree')
plt.plot(num_leave, Total_OneProof_Cost, label='Proof-as-Element')
plt.plot(num_leave, Total_Layer_Cost, label='Layer-based')
plt.plot(num_leave, Total_PBC_Cost, label='Batch-SealPIR')
plt.plot(num_leave, Total_Color_Cost, label='Coloring-based')

# Chart customization
plt.xlabel('Number of leave (n)')
plt.ylabel('Elapsed time (ms)')
plt.title('A Comparison of the Total Running Times of Different Retrieval Schemes')
plt.legend()

# Display the chart
plt.show()

# Plotting
plt.plot(num_leave, Trival_Comm_Cost, label='Trivial (100 Mbps)')
plt.plot(num_leave, WholeTree_Comm_Cost, label='h-time-WholeTree')
plt.plot(num_leave, OneProof_Comm_Cost, label='Proof-as-Element')
plt.plot(num_leave, Layer_Comm_Cost, label='Layer-based')
plt.plot(num_leave, PBC_Comm_Cost, label='Batch-SealPIR')
plt.plot(num_leave, Color_Comm_Cost, label='Coloring-based')

# Chart customization
plt.xlabel('Number of leave (n)')
plt.ylabel('Elapsed time (ms)')
plt.title('A Comparison of the Communication Costs of Different Retrieval Schemes')
plt.legend()

# Display the chart
plt.show()


#test
