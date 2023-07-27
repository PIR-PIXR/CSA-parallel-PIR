'''2. Call SealPIR on the whole tree h times parallel.
3. Each Merkle proof as one element.
4. Call SealPIR on each layer and wait for the slowest.
5. Probabilistic Batch Code SealPIR.
6. Balanced ancestral coloring.'''

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch, Ellipse

REP = 10
jump = 6
network_bandwidth_100 = 100000000 #100 Mbps
network_bandwidth_1G = 1000000000 #1 Gbps

#2. Call SealPIR on the whole tree h times parallel
WholeTree_Comp_Client = [] #ms
WholeTree_Comp_Server = [] #ms
WholeTree_Query_size = [] #bytes
WholeTree_Anwer_size = [] #bytes
WholeTree_Comm_total = [] #bytes
#3. Each Merkle proof as one element
OneProof_Comp_Client = [] #ms
OneProof_Comp_Server = [] #ms
OneProof_Query_size = [] #bytes
OneProof_Anwer_size = [] #bytes
OneProof_Comm_total = [] #bytes
#4. Call SealPIR on each layer and wait for the slowest
Layer_Comp_Client = [] #ms
Layer_Comp_Server = [] #ms
Layer_Query_size = [] #bytes
Layer_Anwer_size = [] #bytes
Layer_Comm_total = [] #bytes
#5. Probabilistic Batch Code SealPIR
PBC_Comp_Client = [] #ms
PBC_Comp_Server = [] #ms
PBC_Query_size = [] #bytes
PBC_Anwer_size = [] #bytes
PBC_Comm_total = [] #bytes
#6. Balanced ancestral coloring
Color_Comp_Client = [] #ms
Color_Comp_Server = [] #ms
Color_Query_size = [] #bytes
Color_Anwer_size = [] #bytes
Color_Comm_total = [] #bytes

#Read data from text file
with open('output2.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height2 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        height2.append(int(lines[i].strip()))
        WholeTree_Comp_Client.append(int(lines[i + 1].strip()) + int(lines[i + 5].strip()))
        WholeTree_Comp_Server.append(int(lines[i + 3].strip()))
        WholeTree_Query_size.append(int(lines[i + 2].strip()))
        WholeTree_Anwer_size.append(int(lines[i + 4].strip()))
        WholeTree_Comm_total.append(int(lines[i + 2].strip()) + int(lines[i + 4].strip()))


#Read data from text file
with open('output3.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height3 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        height3.append(int(lines[i].strip()))
        OneProof_Comp_Client.append(int(lines[i + 1].strip()) + int(lines[i + 5].strip()))
        OneProof_Comp_Server.append(int(lines[i + 3].strip()))
        OneProof_Query_size.append(int(lines[i + 2].strip()))
        OneProof_Anwer_size.append(int(lines[i + 4].strip()))
        OneProof_Comm_total.append(int(lines[i + 2].strip()) + int(lines[i + 4].strip()))

#Read data from text file
with open('output4.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height4 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        height4.append(int(lines[i].strip()))
        Layer_Comp_Client.append(int(lines[i + 1].strip()) + int(lines[i + 5].strip()))
        Layer_Comp_Server.append(int(lines[i + 3].strip()))
        Layer_Query_size.append(int(lines[i + 2].strip()))
        Layer_Anwer_size.append(int(lines[i + 4].strip()))
        Layer_Comm_total.append(int(lines[i + 2].strip()) + int(lines[i + 4].strip()))

#Read data from text file
with open('output5.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height5 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        height5.append(int(lines[i].strip()))
        PBC_Comp_Client.append(int(lines[i + 1].strip()) + int(lines[i + 5].strip()))
        PBC_Comp_Server.append(int(lines[i + 3].strip()))
        PBC_Query_size.append(int(lines[i + 2].strip()))
        PBC_Anwer_size.append(int(lines[i + 4].strip()))
        PBC_Comm_total.append(int(lines[i + 2].strip()) + int(lines[i + 4].strip()))

#Read data from text file
with open('output6.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    height6 = []
    # Iterate over each line
    for i in range(0, len(lines), jump):
        height6.append(int(lines[i].strip()))
        Color_Comp_Client.append(int(lines[i + 1].strip()) + int(lines[i + 5].strip()))
        Color_Comp_Server.append(int(lines[i + 3].strip()))
        Color_Query_size.append(int(lines[i + 2].strip()))
        Color_Anwer_size.append(int(lines[i + 4].strip()))
        Color_Comm_total.append(int(lines[i + 2].strip()) + int(lines[i + 4].strip()))

#Average REP times
def average(array):
    result = []
    for i in range(0, len(array), REP):
        chunk = array[i:i+REP]
        avg = sum(chunk) / len(chunk)
        result.append(avg)
    return result

#Average Convert milliseconds to seconds
def average_convert(array):
    result = []
    for i in range(0, len(array), REP):
        chunk = array[i:i+REP]
        avg = sum(chunk) / len(chunk)
        result.append(avg/1000)
    return result

Avg_WholeTree_Comp_Client = average_convert(WholeTree_Comp_Client)
Avg_WholeTree_Comp_Server = average_convert(WholeTree_Comp_Server)
Avg_WholeTree_Query_size = average(WholeTree_Query_size)
Avg_WholeTree_Anwer_size = average(WholeTree_Anwer_size)
Avg_WholeTree_Comm_total = average(WholeTree_Comm_total)

Avg_OneProof_Comp_Client = average_convert(OneProof_Comp_Client)
Avg_OneProof_Comp_Server = average_convert(OneProof_Comp_Server)
Avg_OneProof_Query_size = average(OneProof_Query_size)
Avg_OneProof_Anwer_size = average(OneProof_Anwer_size)
Avg_OneProof_Comm_total = average(OneProof_Comm_total)

Avg_Layer_Comp_Client = average_convert(Layer_Comp_Client)
Avg_Layer_Comp_Server = average_convert(Layer_Comp_Server)
Avg_Layer_Query_size = average(Layer_Query_size)
Avg_Layer_Anwer_size = average(Layer_Anwer_size)
Avg_Layer_Comm_total = average(Layer_Comm_total)

Avg_PBC_Comp_Client = average_convert(PBC_Comp_Client)
Avg_PBC_Comp_Server = average_convert(PBC_Comp_Server)
Avg_PBC_Query_size = average(PBC_Query_size)
Avg_PBC_Anwer_size = average(PBC_Anwer_size)
Avg_PBC_Comm_total = average(PBC_Comm_total)

Avg_Color_Comp_Client = average_convert(Color_Comp_Client)
Avg_Color_Comp_Server = average_convert(Color_Comp_Server)
Avg_Color_Query_size = average(Color_Query_size)
Avg_Color_Anwer_size = average(Color_Anwer_size)
Avg_Color_Comm_total = average(Color_Comm_total)

#Convert bytes to bits and calcualte communication cost in seconds
WholeTree_Total_Comm_Cost = [element * 8 /network_bandwidth_100 for element in Avg_WholeTree_Comm_total]
WholeTree_Query_Cost = [element * 8 /network_bandwidth_100 for element in Avg_WholeTree_Query_size]
WholeTree_Anwer_Cost = [element * 8 /network_bandwidth_100 for element in Avg_WholeTree_Anwer_size]
#Total computation costs
WholeTree_Total_Comp_Cost = [Avg_WholeTree_Comp_Client[i] + Avg_WholeTree_Comp_Server[i] for i in range(len(WholeTree_Total_Comm_Cost))]

#Convert bytes to bits and calcualte communication cost in seconds
OneProof_Total_Comm_Cost = [element * 8 /network_bandwidth_100 for element in Avg_OneProof_Comm_total]
OneProof_Query_Cost = [element * 8 /network_bandwidth_100 for element in Avg_OneProof_Query_size]
OneProof_Anwer_Cost = [element * 8 /network_bandwidth_100 for element in Avg_OneProof_Anwer_size]
#Total commupuation costs
OneProof_Total_Comp_Cost = [Avg_OneProof_Comp_Client[i] + Avg_OneProof_Comp_Server[i] for i in range(len(OneProof_Total_Comm_Cost))]

#Convert bytes to bits and calcualte communication cost in seconds
Layer_Total_Comm_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Layer_Comm_total]
Layer_Query_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Layer_Query_size]
Layer_Anwer_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Layer_Anwer_size]
#Total commupuation costs
Layer_Total_Comp_Cost = [Avg_Layer_Comp_Client[i] + Avg_Layer_Comp_Server[i] for i in range(len(Layer_Total_Comm_Cost))]

#Convert bytes to bits and calcualte communication cost in seconds
PBC_Total_Comm_Cost = [element * 8 /network_bandwidth_100 for element in Avg_PBC_Comm_total]
PBC_Query_Cost = [element * 8 /network_bandwidth_100 for element in Avg_PBC_Query_size]
PBC_Anwer_Cost = [element * 8 /network_bandwidth_100 for element in Avg_PBC_Anwer_size]
#Total commupuation costs
PBC_Total_Comp_Cost = [Avg_PBC_Comp_Client[i] + Avg_PBC_Comp_Server[i] for i in range(len(PBC_Total_Comm_Cost))]

#Convert bytes to bits and calcualte communication cost in seconds
Color_Total_Comm_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Color_Comm_total]
Color_Query_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Color_Query_size]
Color_Anwer_Cost = [element * 8 /network_bandwidth_100 for element in Avg_Color_Anwer_size]
#Total commupuation costs
Color_Total_Comp_Cost = [Avg_Color_Comp_Client[i] + Avg_Color_Comp_Server[i] for i in range(len(Color_Total_Comm_Cost))]

height = average(height2)
num_leave = [2 ** element for element in height]

#Total communication cost in seconds of the trivial solution (Download the whole Merkle tree)
Trival_Total_Comm_Cost = [(2 * 2 ** element - 2) * 256/network_bandwidth_100 for element in height]

#Number of leaves
x_label = ['$2^{10}$', '$2^{11}$', '$2^{12}$', '$2^{13}$', '$2^{14}$', '$2^{15}$', '$2^{16}$', '$2^{17}$', '$2^{18}$', '$2^{19}$', '$2^{20}$']

# create figure and axes
fig, ax = plt.subplots(2, 1, figsize=(16, 6))

##################################################### Average Communication and Computation costs (100 Mbps)
# Slice the data for positions 10 to 20
x_label_sliced = x_label[5:11]  # From 2^15 to 2^20

WholeTree_Total_Comm_Cost_sliced = WholeTree_Total_Comm_Cost[5:11]
WholeTree_Total_Comp_Cost_sliced = WholeTree_Total_Comp_Cost[5:11]
OneProof_Total_Comm_Cost_sliced = OneProof_Total_Comm_Cost[5:11]
OneProof_Total_Comp_Cost_sliced = OneProof_Total_Comp_Cost[5:11]
Layer_Total_Comm_Cost_sliced = Layer_Total_Comm_Cost[5:11]
Layer_Total_Comp_Cost_sliced = Layer_Total_Comp_Cost[5:11]
PBC_Total_Comm_Cost_sliced = PBC_Total_Comm_Cost[5:11]
PBC_Total_Comp_Cost_sliced = PBC_Total_Comp_Cost[5:11]
Color_Total_Comm_Cost_sliced = Color_Total_Comm_Cost[5:11]
Color_Total_Comp_Cost_sliced = Color_Total_Comp_Cost[5:11]
Trival_Total_Comm_Cost_sliced = Trival_Total_Comm_Cost[5:11]

bar_width = 0.15

bar_1_x = [i for i in range(len(x_label_sliced))]
bar_2_x = [i + bar_width for i in range(len(x_label_sliced))]
bar_3_x = [i + bar_width*2 for i in range(len(x_label_sliced))]
bar_4_x = [i + bar_width*3 for i in range(len(x_label_sliced))]
bar_5_x = [i + bar_width*4 for i in range(len(x_label_sliced))]
bar_6_x = [i + bar_width*5 for i in range(len(x_label_sliced))]

ax[0].bar(bar_1_x, WholeTree_Total_Comm_Cost_sliced, width=bar_width, fill = False, label='Communication costs (100 Mbps)', hatch = '...')
ax[0].bar(bar_1_x, WholeTree_Total_Comp_Cost_sliced, width=bar_width, bottom = WholeTree_Total_Comm_Cost_sliced, label='Computation costs', color = 'gray', hatch = '///')

ax[0].bar(bar_2_x, OneProof_Total_Comm_Cost_sliced, width=bar_width, fill = False, hatch = '...')
ax[0].bar(bar_2_x, OneProof_Total_Comp_Cost_sliced, width=bar_width, bottom = OneProof_Total_Comm_Cost_sliced, color = 'gray', hatch = '///')

ax[0].bar(bar_3_x, Layer_Total_Comm_Cost_sliced, width=bar_width, fill = False, hatch = '...')
ax[0].bar(bar_3_x, Layer_Total_Comp_Cost_sliced, width=bar_width, bottom = Layer_Total_Comm_Cost_sliced, color = 'gray', hatch = '///')

ax[0].bar(bar_4_x, PBC_Total_Comm_Cost_sliced, width=bar_width, fill = False, hatch = '...')
ax[0].bar(bar_4_x, PBC_Total_Comp_Cost_sliced, width=bar_width, bottom = PBC_Total_Comm_Cost_sliced, color = 'gray', hatch = '///')

ax[0].bar(bar_5_x, Color_Total_Comm_Cost_sliced, width=bar_width, fill = False, hatch = '...')
ax[0].bar(bar_5_x, Color_Total_Comp_Cost_sliced, width=bar_width, bottom = Color_Total_Comm_Cost_sliced, color = 'gray', hatch = '///')

ax[0].bar(bar_6_x, Trival_Total_Comm_Cost_sliced, width=bar_width, fill = False, hatch = '...')


for i in range(0, len(x_label_sliced), 2):
    value = WholeTree_Total_Comm_Cost_sliced[i] + WholeTree_Total_Comp_Cost_sliced[i] + 0.1
    ax[0].text(bar_1_x[i] - 0.05, value, '$h$-Repetition', color = 'black', rotation = 90)

    value = OneProof_Total_Comm_Cost_sliced[i] + OneProof_Total_Comp_Cost_sliced[i] + 0.1
    ax[0].text(bar_2_x[i] - 0.05, value, 'Proof-as-Element', color = 'black', rotation = 90)

    value = Layer_Total_Comm_Cost_sliced[i] + Layer_Total_Comp_Cost_sliced[i] + 0.1
    ax[0].text(bar_3_x[i] - 0.05, value, 'Layer-base', color = 'black', rotation = 90)

    value = PBC_Total_Comm_Cost_sliced[i] + PBC_Total_Comp_Cost_sliced[i] + 0.1
    ax[0].text(bar_4_x[i] - 0.05, value, 'PBC-SealPIR', color = 'black', rotation = 90)

    value = Color_Total_Comm_Cost_sliced[i] + Color_Total_Comp_Cost_sliced[i] + 0.1
    ax[0].text(bar_5_x[i] - 0.05, value, 'Coloring-based', color = 'black', rotation = 90, fontweight='bold')

    value = Trival_Total_Comm_Cost_sliced[i] + 0.1
    ax[0].text(bar_6_x[i] - 0.05, value, 'Trivial', color = 'black', rotation = 90)


# Chart customization
ax[0].set_xlabel('n', weight='bold', size = 14)
ax[0].set_ylabel('seconds', weight='bold', size = 14)
ax[0].set_title('Total Running Times', weight='bold', size = 16)
ax[0].set_xticks(bar_4_x, x_label_sliced)
# remove top and right spines
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)

ax[0].legend()

##################################################### Average Communication and Computation costs (1 Gbps)

WholeTree_Total_Comm_Cost_sliced_1G = [element / 10 for element in WholeTree_Total_Comm_Cost_sliced]
OneProof_Total_Comm_Cost_sliced_1G = [element / 10 for element in OneProof_Total_Comm_Cost_sliced]
Layer_Total_Comm_Cost_sliced_1G = [element / 10 for element in Layer_Total_Comm_Cost_sliced]
PBC_Total_Comm_Cost_sliced_1G = [element / 10 for element in PBC_Total_Comm_Cost_sliced]
Color_Total_Comm_Cost_sliced_1G = [element / 10 for element in Color_Total_Comm_Cost_sliced]
Trival_Total_Comm_Cost_sliced_1G = [element / 10 for element in Trival_Total_Comm_Cost_sliced]

ax[1].bar(bar_1_x, WholeTree_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, label='Communication costs (1 Gbps)', hatch = '...')
ax[1].bar(bar_1_x, WholeTree_Total_Comp_Cost_sliced, width=bar_width, bottom = WholeTree_Total_Comm_Cost_sliced_1G, label='Computation costs', color = 'gray', hatch = '///')

ax[1].bar(bar_2_x, OneProof_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, hatch = '...')
ax[1].bar(bar_2_x, OneProof_Total_Comp_Cost_sliced, width=bar_width, bottom = OneProof_Total_Comm_Cost_sliced_1G, color = 'gray', hatch = '///')

ax[1].bar(bar_3_x, Layer_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, hatch = '...')
ax[1].bar(bar_3_x, Layer_Total_Comp_Cost_sliced, width=bar_width, bottom = Layer_Total_Comm_Cost_sliced_1G, color = 'gray', hatch = '///')

ax[1].bar(bar_4_x, PBC_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, hatch = '...')
ax[1].bar(bar_4_x, PBC_Total_Comp_Cost_sliced, width=bar_width, bottom = PBC_Total_Comm_Cost_sliced_1G, color = 'gray', hatch = '///')

ax[1].bar(bar_5_x, Color_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, hatch = '...')
ax[1].bar(bar_5_x, Color_Total_Comp_Cost_sliced, width=bar_width, bottom = Color_Total_Comm_Cost_sliced_1G, color = 'gray', hatch = '///')

ax[1].bar(bar_6_x, Trival_Total_Comm_Cost_sliced_1G, width=bar_width, fill = False, hatch = '...')

for i in range(1, len(x_label_sliced) - 1, 2):
    value = WholeTree_Total_Comm_Cost_sliced_1G[i] + WholeTree_Total_Comp_Cost_sliced[i] + 0.1
    ax[1].text(bar_1_x[i] - 0.05, value, '$h$-Repetition', color = 'black', rotation = 90)

    value = OneProof_Total_Comm_Cost_sliced_1G[i] + OneProof_Total_Comp_Cost_sliced[i] + 0.1
    ax[1].text(bar_2_x[i] - 0.05, value, 'Proof-as-Element', color = 'black', rotation = 90)

    value = Layer_Total_Comm_Cost_sliced_1G[i] + Layer_Total_Comp_Cost_sliced[i] + 0.1
    ax[1].text(bar_3_x[i] - 0.05, value, 'Layer-base', color = 'black', rotation = 90)

    value = PBC_Total_Comm_Cost_sliced_1G[i] + PBC_Total_Comp_Cost_sliced[i] + 0.1
    ax[1].text(bar_4_x[i] - 0.05, value, 'PBC-SealPIR', color = 'black', rotation = 90)

    value = Color_Total_Comm_Cost_sliced_1G[i] + Color_Total_Comp_Cost_sliced[i] + 0.1
    ax[1].text(bar_5_x[i] - 0.05, value, 'Coloring-based', color = 'black', rotation = 90, fontweight='bold')

    value = Trival_Total_Comm_Cost_sliced_1G[i] + 0.1
    ax[1].text(bar_6_x[i] - 0.05, value, 'Trivial', color = 'black', rotation = 90)

value = WholeTree_Total_Comm_Cost_sliced_1G[len(x_label_sliced) - 1] + WholeTree_Total_Comp_Cost_sliced[len(x_label_sliced) - 1] + 0.1
ax[1].text(bar_1_x[len(x_label_sliced) - 1] - 0.05, value, '$h$-Repetition', color = 'black', rotation = 90)

value = Layer_Total_Comm_Cost_sliced_1G[len(x_label_sliced) - 1] + Layer_Total_Comp_Cost_sliced[len(x_label_sliced) - 1] + 0.1
ax[1].text(bar_3_x[len(x_label_sliced) - 1] - 0.05, value, 'Layer-base', color = 'black', rotation = 90)

value = PBC_Total_Comm_Cost_sliced_1G[len(x_label_sliced) - 1] + PBC_Total_Comp_Cost_sliced[len(x_label_sliced) - 1] + 0.1
ax[1].text(bar_4_x[len(x_label_sliced) - 1] - 0.05, value, 'PBC-SealPIR', color = 'black', rotation = 90)

value = Color_Total_Comm_Cost_sliced_1G[len(x_label_sliced) - 1] + Color_Total_Comp_Cost_sliced[len(x_label_sliced) - 1] + 0.1
ax[1].text(bar_5_x[len(x_label_sliced) - 1] - 0.05, value, 'Coloring-based', color = 'black', rotation = 90, fontweight='bold')

value = Trival_Total_Comm_Cost_sliced_1G[len(x_label_sliced) - 1] + 0.1
ax[1].text(bar_6_x[len(x_label_sliced) - 1] - 0.05, value, 'Trivial', color = 'black', rotation = 90)

# Chart customization
ax[1].set_xlabel('n', weight='bold', size = 14)
ax[1].set_ylabel('seconds', weight='bold', size = 14)
ax[1].set_xticks(bar_4_x, x_label_sliced)
# remove top and right spines
ax[1].spines['right'].set_visible(False)
ax[1].spines['top'].set_visible(False)

ax[1].legend()

plt.savefig('totalSealPIR.pdf', dpi=300, bbox_inches='tight')

#######################################################################################################
# create figure and axes
fig, a = plt.subplots(figsize=(7, 5))

# Plotting Server costs
a.plot(num_leave, Avg_WholeTree_Comp_Server, label='$h$-Repetition', marker='x', linestyle='-', color='black')
a.plot(num_leave, Avg_OneProof_Comp_Server, label='Proof-as-Element', marker='.', linestyle='-.', color='black')
a.plot(num_leave, Avg_Layer_Comp_Server, label='Layer-based', marker='.', linestyle=':', color='black')
a.plot(num_leave, Avg_PBC_Comp_Server, label='PBC-SealPIR', marker='x', linestyle='--', color='black')
a.plot(num_leave, Avg_Color_Comp_Server, label='Coloring-based', marker='.', linestyle='-', color='black')

# Chart customization
a.set_xlabel('n', weight='bold', size = 12)
a.set_ylabel('seconds', weight='bold', size = 12)
a.set_title('Server Eslapsed Time', weight='bold', size = 14)
# remove top and right spines
a.spines['right'].set_visible(False)
a.spines['top'].set_visible(False)

# Create the in axes
in_ax = plt.axes([0.58, 0.4, 0.3, 0.2])  # [left, bottom, width, height]

num_leave_zoom = num_leave[8:11]
Avg_Layer_Comp_Server_zoom = Avg_Layer_Comp_Server[8:11]
Avg_PBC_Comp_Server_zoom = Avg_PBC_Comp_Server[8:11]
Avg_Color_Comp_Server_zoom = Avg_Color_Comp_Server[8:11]

# Plotting Client costs
in_ax.plot(num_leave_zoom, Avg_Layer_Comp_Server_zoom, label='Layer-based', marker='.', linestyle=':', color='black')
in_ax.plot(num_leave_zoom, Avg_PBC_Comp_Server_zoom, label='PBC-SealPIR', marker='x', linestyle='--', color='black')
in_ax.plot(num_leave_zoom, Avg_Color_Comp_Server_zoom, label='Coloring-based', marker='.', linestyle='-', color='black')

# Chart customization
in_ax.set_xlabel('n', weight='bold', size = 8)
in_ax.set_ylabel('seconds', weight='bold', size = 8)
in_ax.set_title('Server Eslapsed Time', weight='bold', size = 8)

# remove top and right spines
#in_ax.spines['right'].set_visible(False)
#in_ax.spines['top'].set_visible(False)

# Calculate the width and height of the ellipse
ellipse_width = 1.2 * (max(num_leave_zoom) - min(num_leave_zoom))
ellipse_height = 4.5 * (max(Avg_PBC_Comp_Server_zoom) - min(Avg_PBC_Comp_Server_zoom))

# Calculate the center of the ellipse
ellipse_center_x = (max(num_leave_zoom) + min(num_leave_zoom)) / 2 + 40000
ellipse_center_y = (max(Avg_PBC_Comp_Server_zoom) + min(Avg_PBC_Comp_Server_zoom)) / 2

# Create the ellipse patch
ellipse = Ellipse((ellipse_center_x, ellipse_center_y), ellipse_width, ellipse_height,
                  edgecolor='gray', facecolor='none', linewidth=1)
a.add_patch(ellipse)

# Add a connection line between the circle and the smaller line chart
connection_line = ConnectionPatch((ellipse_center_x, ellipse_center_y + 0.3), (720000, 1.9),
                                  "data", "data", arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=10,
                                  lw = 1, color='gray')
a.add_artist(connection_line)

legend = a.legend()
legend.get_texts()[4].set_fontweight('bold')

# Display the chart
plt.savefig('serverSealPIR.pdf', dpi=300, bbox_inches='tight')
