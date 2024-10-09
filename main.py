import dspAutomation
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value, PULP_CBC_CMD


recipes = dspAutomation.getRecipes('recipes.json')
inSet = set()
outSet = set()
for key, value in recipes.items():
    outSet.add(key)
    for item in value:
        inSet.add(item)
ELEMENTS_A = [i for i in inSet]
ELEMENTS_B = [i for i in outSet]

relationTable = {}
for key, values in recipes.items():
    for value in values:
        if value in relationTable:
            relationTable[value][key] = 1
        else:
            relationTable[value] = {key: 1}

# Constants
ROWS = 4
COLS = 36

# Initialize the problem
model = LpProblem("Minimize_Manhattan_Distances", LpMinimize)

# Decision variables
x = LpVariable.dicts("Position", (range(ROWS), range(COLS), ELEMENTS_A + ELEMENTS_B), cat='Binary')

# Auxiliary variables
z = LpVariable.dicts("Pair", (range(ROWS), range(COLS), range(ROWS), range(COLS), ELEMENTS_A, ELEMENTS_B), cat='Binary')

# Objective function
model += lpSum(z[i][j][k][l][a][b] * (abs(i - k) + abs(j - l))
               for i in range(ROWS) for j in range(COLS)
               for k in range(ROWS) for l in range(COLS)
               for a in ELEMENTS_A for b in ELEMENTS_B if b in relationTable[a])

# Constraints
# Each input element must be placed exactly once
for element in ELEMENTS_A:
    model += lpSum(x[i][j][element] for i in range(ROWS) for j in range(COLS)) >= 1
# Each output element must be placed exactly once
for element in ELEMENTS_B:
    model += lpSum(x[i][j][element] for i in range(ROWS) for j in range(COLS)) == 1

# Each grid cell must contain exactly one element
for i in range(ROWS):
    for j in range(COLS):
        model += lpSum(x[i][j][element] for element in ELEMENTS_A + ELEMENTS_B) == 1

# An elements only in rows 1 and 2, B elements in rows 0 and 3
for j in range(COLS):
    for a in ELEMENTS_A:
        model += x[0][j][a] == 0
        model += x[3][j][a] == 0
    for b in ELEMENTS_B:
        model += x[1][j][b] == 0
        model += x[2][j][b] == 0

# Auxiliary variable constraints
for i in range(ROWS):
    for j in range(COLS):
        for k in range(ROWS):
            for l in range(COLS):
                for a in ELEMENTS_A:
                    for b in ELEMENTS_B:
                        model += z[i][j][k][l][a][b] <= x[i][j][a]
                        model += z[i][j][k][l][a][b] <= x[k][l][b]
                        model += z[i][j][k][l][a][b] >= x[i][j][a] + x[k][l][b] - 1

solver = PULP_CBC_CMD(threads=4)
# Solve the problem
model.solve()

# Check the status and print the result
print("Status:", LpStatus[model.status])

# Print the positions of each element (optional, to verify)
for element in ELEMENTS_A + ELEMENTS_B:
    for i in range(ROWS):
        for j in range(COLS):
            if value(x[i][j][element]) == 1:
                print(f"{element} is placed at ({i}, {j})")
