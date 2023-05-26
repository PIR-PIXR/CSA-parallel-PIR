import matplotlib.pyplot as plt

REP = 100
jump = REP + 1

Height = []
Micro = []
Micro_Avage = []

#Read data from text file
with open('outputCSA.txt', 'r') as f:
    # Read the lines of the file
    lines = f.readlines()
    # Iterate over each line
    for i in range(0, len(lines), jump):
        # Read height
        Height.append(int(lines[i].strip()))

        for j in range(1, jump, 1):
            Micro.append(int(lines[i + j].strip()))

#Average REP times
def average(array):
    result = []
    n = len(array)
    for i in range(0, n, REP):
        chunk = array[i:i+REP]
        avg = sum(chunk) / len(chunk)
        result.append(avg)
    return result

Micro_Avage = average(Micro)
Mili_Avage = [element/1000 for element in Micro_Avage]

num_leave = [2 ** element for element in Height]

# Plotting
plt.plot(num_leave, Mili_Avage, marker='o', linestyle='-', color='black')

# Chart customization
plt.xlabel('n', weight='bold', size = 12)
plt.ylabel('milliseconds', weight='bold', size = 12)
plt.title('CSA Running Time', weight='bold', size = 14)
# Access the axes object
ax = plt.gca()

# Hide right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.legend()

# Save the chart as a PDF file
plt.savefig('CSAline.pdf', bbox_inches='tight', dpi=300)
