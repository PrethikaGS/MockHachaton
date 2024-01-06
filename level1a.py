import pandas as pd
import json

with open('Student Handout/Input data/level1a.json', 'r') as f:
  data = json.load(f)

# bin packing
from ortools.linear_solver import pywraplp


n_neighbourhoods=(data['n_neighbourhoods'])
n_restaurants=(data['n_restaurants'])
quantity=[0 for i in range(n_neighbourhoods)]
distanceMat=[[0]*(n_neighbourhoods+n_restaurants+1) for i in range(n_neighbourhoods+n_restaurants)]
vehicles=1
vehiclecap=data['vehicles']['v0']["capacity"]


for i in range(n_restaurants):
    distanceMat[i]=data['restaurants']['r'+str(i)]["restaurant_distance"]+data['restaurants']['r'+str(i)]["neighbourhood_distance"]
for i in range(n_neighbourhoods):
    quantity[i]=data['neighbourhoods']['n'+str(i)]['order_quantity']
    distanceMat[i+n_restaurants]=[distanceMat[0][i+n_restaurants]]+data['neighbourhoods']['n'+str(i)]['distances']


def firstFit(weight, n, c):
    final=[]
    res = 0
    bin_rem = [0]*n

    for i in range(n):
        j = 0
        while( j < res):
            if (bin_rem[j] >= weight[i]):
                bin_rem[j] = bin_rem[j] - weight[i]
                final[j].append(i)
                break
            j+=1
        if (j == res):
            bin_rem[res] = c - weight[i]
            final.append([i])
            res= res+1
    return final
     
nodes_to_traverse=firstFit(quantity,20,600)
print(nodes_to_traverse)















































































"""

from ortools.linear_solver import pywraplp


def create_data_model():
    #Create the data for the example.
    data = {}
    weights = quantity
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = 600
    return data



def main():
    data = create_data_model()

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data["items"]:
        for j in data["bins"]:
            x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" % (i, j))

    # y[j] = 1 if bin j is used.
    y = {}
    for j in data["bins"]:
        y[j] = solver.IntVar(0, 1, "y[%i]" % j)

    # Constraints
    # Each item must be in exactly one bin.
    for i in data["items"]:
        solver.Add(sum(x[i, j] for j in data["bins"]) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in data["bins"]:
        solver.Add(
            sum(x[(i, j)] * data["weights"][i] for i in data["items"])
            <= y[j] * data["bin_capacity"]
        )

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum([y[j] for j in data["bins"]]))

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    nodes_tovisit=[]
    if status == pywraplp.Solver.OPTIMAL:
        num_bins = 0
        for j in data["bins"]:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data["items"]:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(i)
                        bin_weight += data["weights"][i]
                if bin_items:
                    num_bins += 1
                    nodes_tovisit.append(bin_items)

        print("Number of bins used:", nodes_tovisit)

    else:
        print("The problem does not have an optimal solution.")
    




if __name__ == "__main__":
    main()

"""