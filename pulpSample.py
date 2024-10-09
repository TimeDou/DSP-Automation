# import pulp
#
# def minimize_manhattan_distance(source_target_dict, k):
#     # Create the linear programming problem to minimize
#     prob = pulp.LpProblem("ManhattanDistanceMinimization", pulp.LpMinimize)
#
#     # Create variables for the coordinates of the source and target points
#     point_vars = {}
#     for point in set(sum(source_target_dict.values(), [])):  # source points
#         point_vars[point] = (pulp.LpVariable(f"{point}_x", 0, k-1),
#                              pulp.LpVariable(f"{point}_y", 0, 1))
#     for point in source_target_dict.keys():  # target points
#         point_vars[point] = (pulp.LpVariable(f"{point}_x", 0, k-1),
#                              pulp.LpVariable(f"{point}_y", -2, 3))
#
#     # Create the objective function
#     total_distance = []
#     for target, sources in source_target_dict.items():
#         for source in sources:
#             total_distance.append(
#                 pulp.lpSum([abs(point_vars[target][i] - point_vars[source][i]) for i in range(2)])
#             )
#     prob += pulp.lpSum(total_distance), "Total Manhattan Distance"
#
#     # Solve the problem
#     prob.solve()
#
#     # Return the coordinates of the points
#     return {point: (pulp.value(var[0]), pulp.value(var[1])) for point, var in point_vars.items()}
"""
A set partitioning model of a wedding seating problem
Adaptation where an initial solution is given to solvers: CPLEX_CMD, GUROBI_CMD, PULP_CBC_CMD

Authors: Stuart Mitchell 2009, Franco Peschiera 2019
"""

import pulp

max_tables = 5
max_table_size = 4
guests = "A B C D E F G I J K L M N O P Q R".split()


def happiness(table):
    """
    Find the happiness of the table
    - by calculating the maximum distance between the letters
    """
    return abs(ord(table[0]) - ord(table[-1]))


# create list of all possible tables
possible_tables = [tuple(c) for c in pulp.allcombinations(guests, max_table_size)]

# create a binary variable to state that a table setting is used
x = pulp.LpVariable.dicts(
    "table", possible_tables, lowBound=0, upBound=1, cat=pulp.LpInteger
)

seating_model = pulp.LpProblem("Wedding Seating Model", pulp.LpMinimize)

seating_model += pulp.lpSum([happiness(table) * x[table] for table in possible_tables])

# specify the maximum number of tables
seating_model += (
    pulp.lpSum([x[table] for table in possible_tables]) <= max_tables,
    "Maximum_number_of_tables",
)

# A guest must seated at one and only one table
for guest in guests:
    seating_model += (
        pulp.lpSum([x[table] for table in possible_tables if guest in table]) == 1,
        f"Must_seat_{guest}",
    )

# I've taken the optimal solution from a previous solving. x is the variable dictionary.
solution = {
    ("M", "N"): 1.0,
    ("E", "F", "G"): 1.0,
    ("A", "B", "C", "D"): 1.0,
    ("I", "J", "K", "L"): 1.0,
    ("O", "P", "Q", "R"): 1.0,
}
for k, v in solution.items():
    x[k].setInitialValue(v)

solver = pulp.PULP_CBC_CMD(msg=True, warmStart=True)
# solver = pulp.CPLEX_CMD(msg=True, warmStart=True)
# solver = pulp.GUROBI_CMD(msg=True, warmStart=True)
# solver = pulp.CPLEX_PY(msg=True, warmStart=True)
# solver = pulp.GUROBI(msg=True, warmStart=True)
seating_model.solve(solver)


print(f"The chosen tables are out of a total of {len(possible_tables)}:")
for table in possible_tables:
    if x[table].value() == 1.0:
        print(table)
