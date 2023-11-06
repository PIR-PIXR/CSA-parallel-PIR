import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch, Ellipse
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D

height = []

#1. Each Merkle proof as one element (Proof-As-Element)
OneProof_Querytime_Client = [] #us
OneProof_Querysize_Client = [] #bytes
OneProof_Extracttime_Client = [] #us
OneProof_Anstime_Server = [] #us
OneProof_Anssize_Server = [] #bytes
OneProof_Comm_total = [] #bytes

with open('proofAsElement_Client.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    # Iterate over each line
    for i in range(0, len(lines), 4):
        height.append(int(lines[i].strip()))
        OneProof_Querytime_Client.append(int(lines[i + 1].strip()))
        OneProof_Querysize_Client.append(int(lines[i + 2].strip()))
        OneProof_Extracttime_Client.append(int(lines[i + 3].strip()))

with open('proofAsElement_Servers.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    # Iterate over each line
    for i in range(0, len(lines), 3):
        OneProof_Anstime_Server.append(int(lines[i + 1].strip()))
        OneProof_Anssize_Server.append(int(lines[i + 2].strip()))


#2. Call SealPIR on the whole tree h times parallel (h-Repetition)
WholeTree_Querytime_Client = [] #us
WholeTree_Querysize_Client = [] #bytes
WholeTree_Extracttime_Client = [] #us
WholeTree_Anstime_Server = [] #us
WholeTree_Anssize_Server = [] #bytes
WholeTree_Comm_total = [] #bytes

with open('hRepetition_Client.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 3 + 1 for h in height]

    while i < len(lines):
        total_Querytime = 0
        total_Querysize = 0
        total_Extracttime = 0

        for j in range(0, step_values[k] - 1, 3):
            total_Querytime += int(lines[i + j + 1].strip())
            total_Querysize += int(lines[i + j + 2].strip())
            total_Extracttime += int(lines[i + j + 3].strip())

        WholeTree_Querytime_Client.append(total_Querytime)
        WholeTree_Querysize_Client.append(total_Querysize)
        WholeTree_Extracttime_Client.append(total_Extracttime)
        i += step_values[k]
        k += 1
    #print(WholeTree_Querytime_Client)

with open('hRepetition_Servers.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 2 + 1 for h in height]

    while i < len(lines):
        Anstime = []
        total_Anssize = 0

        for j in range(2):
            if j == 0:
                for l in range(0, height[k], 1):
                    Anstime.append(int(lines[i + l + 1].strip()))
            else:
                for l in range(height[k], step_values[k] - 1, 1):
                    total_Anssize += int(lines[i + l + 1].strip())

        WholeTree_Anstime_Server.append(max(Anstime))
        WholeTree_Anssize_Server.append(total_Anssize)
        i += step_values[k]
        k += 1
    #print(WholeTree_Anstime_Server)


#3. Call SealPIR on each layer and wait for the slowest (Layer-based)
Layer_Querytime_Client = [] #us
Layer_Querysize_Client = [] #bytes
Layer_Extracttime_Client = [] #us
Layer_Anstime_Server = [] #us
Layer_Anssize_Server = [] #bytes
Layer_Comm_total = [] #bytes

with open('layerBased_Client.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 3 + 1 for h in height]

    while i < len(lines):
        total_Querytime = 0
        total_Querysize = 0
        total_Extracttime = 0

        for j in range(0, step_values[k] - 1, 3):
            total_Querytime += int(lines[i + j + 1].strip())
            total_Querysize += int(lines[i + j + 2].strip())
            total_Extracttime += int(lines[i + j + 3].strip())

        Layer_Querytime_Client.append(total_Querytime)
        Layer_Querysize_Client.append(total_Querysize)
        Layer_Extracttime_Client.append(total_Extracttime)
        i += step_values[k]
        k += 1
    #print(Layer_Querytime_Client)

with open('layerBased_Servers.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 2 + 1 for h in height]

    while i < len(lines):
        Anstime = []
        total_Anssize = 0

        for j in range(2):
            if j == 0:
                for l in range(0, height[k], 1):
                    Anstime.append(int(lines[i + l + 1].strip()))
            else:
                for l in range(height[k], step_values[k] - 1, 1):
                    total_Anssize += int(lines[i + l + 1].strip())

        Layer_Anstime_Server.append(max(Anstime))
        Layer_Anssize_Server.append(total_Anssize)
        i += step_values[k]
        k += 1
    #print(Layer_Anstime_Server)

#5. Probabilistic Batch Code SealPIR (SealPIR + PBC)
PBC_Querytime_Client = [] #us
PBC_Querysize_Client = [] #bytes
PBC_Extracttime_Client = [] #us
PBC_Anstime_Server = [] #us
PBC_Anssize_Server = [] #bytes
PBC_Comm_total = [] #bytes

with open('pbc_Client.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [int (h * 3 * 1.5) + 1 for h in height]

    while i < len(lines):
        total_Querytime = 0
        total_Querysize = 0
        total_Extracttime = 0

        for j in range(0, step_values[k] - 1, 3):
            total_Querytime += int(lines[i + j + 1].strip())
            total_Querysize += int(lines[i + j + 2].strip())
            total_Extracttime += int(lines[i + j + 3].strip())

        PBC_Querytime_Client.append(total_Querytime)
        PBC_Querysize_Client.append(total_Querysize)
        PBC_Extracttime_Client.append(total_Extracttime)
        i += step_values[k]
        k += 1
    #print(PBC_Querytime_Client)

with open('pbc_Servers.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [int (h * 2 * 1.5) + 1 for h in height]

    while i < len(lines):
        Anstime = []
        total_Anssize = 0

        for j in range(2):
            if j == 0:
                for l in range(0, int (height[k] * 1.5) , 1):
                    Anstime.append(int(lines[i + l + 1].strip()))
            else:
                for l in range(int (height[k] * 1.5), step_values[k] - 1, 1):
                    total_Anssize += int(lines[i + l + 1].strip())

        PBC_Anstime_Server.append(max(Anstime))
        PBC_Anssize_Server.append(total_Anssize)
        i += step_values[k]
        k += 1
    #print(PBC_Anstime_Server)

#6. Balanced ancestral coloring (SealPIR + Coloring)
Color_Querytime_Client = [] #us
Color_Querysize_Client = [] #bytes
Color_Extracttime_Client = [] #us
Color_Anstime_Server = [] #us
Color_Anssize_Server = [] #bytes
Color_Comm_total = [] #bytes

with open('coloringBased_Client.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 3 + 1 for h in height]

    while i < len(lines):
        total_Querytime = 0
        total_Querysize = 0
        total_Extracttime = 0

        for j in range(0, step_values[k] - 1, 3):
            total_Querytime += int(lines[i + j + 1].strip())
            total_Querysize += int(lines[i + j + 2].strip())
            total_Extracttime += int(lines[i + j + 3].strip())

        Color_Querytime_Client.append(total_Querytime)
        Color_Querysize_Client.append(total_Querysize)
        Color_Extracttime_Client.append(total_Extracttime)
        i += step_values[k]
        k += 1
    #print(Color_Querytime_Client)

with open('coloringBased_Servers.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()

    i = 0
    k = 0
    step_values = [h * 2 + 1 for h in height]

    while i < len(lines):
        Anstime = []
        total_Anssize = 0

        for j in range(2):
            if j == 0:
                for l in range(0, height[k], 1):
                    Anstime.append(int(lines[i + l + 1].strip()))
            else:
                for l in range(height[k], step_values[k] - 1, 1):
                    total_Anssize += int(lines[i + l + 1].strip())

        Color_Anstime_Server.append(max(Anstime))
        Color_Anssize_Server.append(total_Anssize)
        i += step_values[k]
        k += 1
    #print(Color_Anstime_Server)

#7. DP-PIR
height2 = []
DPPIR_Offline = [] #ms
DPPIR_Online = [] #ms

with open('dpPIR.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    # Iterate over each line
    for i in range(0, len(lines), 3):
        height2.append(int(lines[i].strip()))
        DPPIR_Offline.append(int(lines[i + 1].strip()))
        DPPIR_Online.append(int(lines[i + 2].strip()))

#8. DP-PIR+Coloring
DPPIR_Coloring_Offline = [] #ms
DPPIR_Coloring_Online = [] #ms
with open('dpPIRcoloring.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    # Iterate over each line
    for i in range(0, len(lines), 3):
        DPPIR_Coloring_Offline.append(int(lines[i + 1].strip()))
        DPPIR_Coloring_Online.append(int(lines[i + 2].strip()))


###########################################################################################################################
#Number of leaves
x_label = ['$2^{10}$', '$2^{12}$', '$2^{14}$', '$2^{16}$', '$2^{18}$', '$2^{20}$']
x_label2 = ['$2^{10}$', '$2^{12}$', '$2^{14}$', '$2^{16}$']

#Convert from us to seconds
OneProof_Anstime_Server = [value/1000000 for value in OneProof_Anstime_Server]
WholeTree_Anstime_Server = [value/1000000 for value in WholeTree_Anstime_Server]
Layer_Anstime_Server = [value/1000000 for value in Layer_Anstime_Server]
PBC_Anstime_Server = [value/1000000 for value in PBC_Anstime_Server]
Color_Anstime_Server = [value/1000000 for value in Color_Anstime_Server]

#Convert from ms to seconds
DPPIR_Offline = [value/1000 for value in DPPIR_Offline]
DPPIR_Online = [value/1000 for value in DPPIR_Online]
DPPIR_Coloring_Offline = [value/1000 for value in DPPIR_Coloring_Offline]
DPPIR_Coloring_Online = [value/1000 for value in DPPIR_Coloring_Online]

##########################################Plotting Server costs (SealPIR)#############################################################
# create figure and axes
fig, a = plt.subplots(figsize=(8, 3))

# Plotting Server costs
a.plot(x_label, OneProof_Anstime_Server, label='Proof-as-Element', marker='.', linestyle='-.', color='black')
a.plot(x_label, WholeTree_Anstime_Server, label='$h$-Repetition', marker='x', linestyle='-', color='black')
a.plot(x_label, Layer_Anstime_Server, label='Layer-based', marker='.', linestyle=':', color='black')
a.plot(x_label, PBC_Anstime_Server, label='SealPIR+PBC', marker='x', linestyle='--', color='black')
a.plot(x_label, Color_Anstime_Server, label='SealPIR+Coloring', marker='.', linestyle='-', color='black')

# Chart customization
a.set_xlabel('n', weight='bold', size = 14)
a.set_ylabel('seconds', weight='bold', size = 14)
a.set_title('Server Eslapsed Time', weight='bold', size = 16)
# remove top and right spines
a.spines['right'].set_visible(False)
a.spines['top'].set_visible(False)

# Create the zoomin axes
in_ax = plt.axes([0.46, 0.5, 0.25, 0.38])  # [left, bottom, width, height]

num_leave_zoom = x_label[3:7]
Layer_Comp_Server_zoom = Layer_Anstime_Server[3:7]
PBC_Comp_Server_zoom = PBC_Anstime_Server[3:7]
Color_Comp_Server_zoom = Color_Anstime_Server[3:7]

# Plotting Server costs
in_ax.plot(num_leave_zoom, Layer_Comp_Server_zoom, label='Layer-based', marker='.', linestyle=':', color='black')
in_ax.plot(num_leave_zoom, PBC_Comp_Server_zoom, label='SealPIR+PBC', marker='x', linestyle='--', color='black')
in_ax.plot(num_leave_zoom, Color_Comp_Server_zoom, label='SealPIR+Coloring', marker='.', linestyle='-', color='black')

# Chart customization
in_ax.set_xlabel('n', weight='bold', size = 10)
in_ax.set_ylabel('seconds', weight='bold', size = 10)

# Calculate the width and height of the ellipse
ellipse_width = 2.3
ellipse_height = 1.6

# Calculate the center of the ellipse
ellipse_center_x = 4
ellipse_center_y = 0.4

# Create the ellipse patch
ellipse = Ellipse((ellipse_center_x, ellipse_center_y), ellipse_width, ellipse_height,
                  edgecolor='gray', facecolor='none', linewidth=1)

a.add_patch(ellipse)

# Add a connection line between the ellipse and the zoomin line chart
connection_line = ConnectionPatch((ellipse_center_x, ellipse_center_y + 0.5), (3.5, 4.8), "data", "data",
                                    arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=10, lw = 1, color='gray')
a.add_artist(connection_line)


legend = a.legend()
legend.get_texts()[4].set_fontweight('bold')
# Add a grid
a.grid(True, linestyle='--', alpha=0.6)

# Customize the fontsize of x-axis tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the chart
plt.savefig('serverSealPIRtime.pdf', dpi=600, bbox_inches='tight')

##########################################Plotting Client costs (SealPIR)#############################################################
OneProof_Comp_total = [(query_time + extract_time)/1000 for query_time, extract_time in zip(OneProof_Querytime_Client, OneProof_Extracttime_Client)]
WholeTree_Comp_total = [(query_time + extract_time)/1000 for query_time, extract_time in zip(WholeTree_Querytime_Client, WholeTree_Extracttime_Client)]
Layer_Comp_total = [(query_time + extract_time)/1000 for query_time, extract_time in zip(Layer_Querytime_Client, Layer_Extracttime_Client)]
PBC_Comp_total = [(query_time + extract_time)/1000 for query_time, extract_time in zip(PBC_Querytime_Client, PBC_Extracttime_Client)]
Color_Comp_total = [(query_time + extract_time)/1000 for query_time, extract_time in zip(Color_Querytime_Client, Color_Extracttime_Client)]

# create figure and axes
fig, a = plt.subplots(figsize=(8, 3))

# Plotting Server costs
a.plot(x_label, OneProof_Comp_total, label='Proof-as-Element', marker='.', linestyle='-.', color='black')
a.plot(x_label, WholeTree_Comp_total, label='$h$-Repetition', marker='x', linestyle='-', color='black')
a.plot(x_label, Layer_Comp_total, label='Layer-based', marker='.', linestyle=':', color='black')
a.plot(x_label, PBC_Comp_total, label='SealPIR+PBC', marker='x', linestyle='--', color='black')
a.plot(x_label, Color_Comp_total, label='SealPIR+Coloring', marker='.', linestyle='-', color='black')

# Chart customization
a.set_xlabel('n', weight='bold', size = 14)
a.set_ylabel('milliseconds', weight='bold', size = 14)
a.set_title('Total Client Computation Time', weight='bold', size = 16)
# remove top and right spines
a.spines['right'].set_visible(False)
a.spines['top'].set_visible(False)

legend = a.legend()
legend.get_texts()[4].set_fontweight('bold')
# Add a grid
a.grid(True, linestyle='--', alpha=0.6)

# Customize the fontsize of x-axis tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the chart
plt.savefig('clientSealPIRtime.pdf', dpi=600, bbox_inches='tight')

##########################################Plotting Communication costs (SealPIR)#############################################################
OneProof_Comm_total = [(query_size + ans_size)/1000000 for query_size, ans_size in zip(OneProof_Querysize_Client , OneProof_Anssize_Server)]
WholeTree_Comm_total = [(query_size + ans_size)/1000000 for query_size, ans_size in zip(WholeTree_Querysize_Client , WholeTree_Anssize_Server)]
Layer_Comm_total = [(query_size + ans_size)/1000000 for query_size, ans_size in zip(Layer_Querysize_Client , Layer_Anssize_Server)]
PBC_Comm_total = [(query_size + ans_size)/1000000 for query_size, ans_size in zip(PBC_Querysize_Client , PBC_Anssize_Server)]
Color_Comm_total = [(query_size + ans_size)/1000000 for query_size, ans_size in zip(Color_Querysize_Client , Color_Anssize_Server)]

# create figure and axes
fig, a = plt.subplots(figsize=(8, 3))

# Plotting Server costs
a.plot(x_label, OneProof_Comm_total, label='Proof-as-Element', marker='.', linestyle='-.', color='black')
a.plot(x_label, WholeTree_Comm_total, label='$h$-Repetition', marker='x', linestyle='-', color='black')
a.plot(x_label, Layer_Comm_total, label='Layer-based', marker='.', linestyle=':', color='black')
a.plot(x_label, PBC_Comm_total, label='SealPIR+PBC', marker='x', linestyle='--', color='black')
a.plot(x_label, Color_Comm_total, label='SealPIR+Coloring', marker='.', linestyle='-', color='black')

# Chart customization
a.set_xlabel('n', weight='bold', size = 14)
a.set_ylabel('MB', weight='bold', size = 14)
a.set_title('Total Communication Costs', weight='bold', size = 16)
# remove top and right spines
a.spines['right'].set_visible(False)
a.spines['top'].set_visible(False)

legend = a.legend()
legend.get_texts()[4].set_fontweight('bold')
# Add a grid
a.grid(True, linestyle='--', alpha=0.6)

# Customize the fontsize of x-axis tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the chart
plt.savefig('commSealPIRCosts.pdf', dpi=600, bbox_inches='tight')

##########################################Plotting Computation costs (DP-PIR)#############################################################
# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))  # 1 row, 2 columns

# Plotting Online/Offline costs
ax1.plot(x_label2, DPPIR_Offline, label='DP-PIR', marker='x', linestyle='--', color='black')
ax1.plot(x_label2, DPPIR_Coloring_Offline, label='DP-PIR+Coloring', marker='.', linestyle='-', color='black')
ax1.set_xlabel('n', weight='bold', size = 14)
ax1.set_ylabel('seconds', weight='bold', size = 14)
ax1.set_title('Offline Costs', weight='bold', size = 16)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.grid(True, linestyle='--', alpha=0.6)
legend = ax1.legend()
legend.get_texts()[1].set_fontweight('bold')
# Add numbers to the points in the first subplot
for i in range(1, len(x_label2)):
    xi, yi = x_label2[i], DPPIR_Coloring_Offline[i]
    ax1.text(xi, yi, f'{yi}', ha='center', va='bottom', fontsize=10, color='gray')

ax2.plot(x_label2, DPPIR_Online, label='DP-PIR', marker='x', linestyle='--', color='black')
ax2.plot(x_label2, DPPIR_Coloring_Online, label='DP-PIR+Coloring', marker='.', linestyle='-', color='black')
ax2.set_xlabel('n', weight='bold', size = 14)
ax2.set_ylabel('seconds', weight='bold', size = 14)
ax2.set_title('Online Costs', weight='bold', size = 16)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.grid(True, linestyle='--', alpha=0.6)
legend = ax2.legend()
legend.get_texts()[1].set_fontweight('bold')
# Add numbers to the points in the second subplot
for i in range(1, len(x_label2)):
    xi, yi = x_label2[i], DPPIR_Coloring_Online[i]
    ax2.text(xi, yi, f'{yi}', ha='center', va='bottom', fontsize=10, color='gray')

# Customize the fontsize of x-axis tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the chart
plt.savefig('compOnOffCosts.pdf', dpi=600, bbox_inches='tight')
