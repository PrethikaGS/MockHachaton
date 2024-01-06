import pandas as pd
import json

with open('Student Handout/Input data/level2a.json', 'r') as f:
  data = json.load(f)


n_neighbourhoods=(data['n_neighbourhoods'])
n_restaurants=(data['n_restaurants'])
n_vehicles=0
vehiclecap=[]
for i in data["vehicles"]:
    n_vehicles+=1
    vehiclecap.append(data["vehicles"][i]["capacity"])
#print(vehiclecap)
quantity=[0 for i in range(n_neighbourhoods)]
distanceMat=[[0]*(n_neighbourhoods+n_restaurants+1) for i in range(n_neighbourhoods+n_restaurants)]



for i in range(n_restaurants):
    distanceMat[i]=data['restaurants']['r'+str(i)]["restaurant_distance"]+data['restaurants']['r'+str(i)]["neighbourhood_distance"]
for i in range(n_neighbourhoods):
    quantity[i]=data['neighbourhoods']['n'+str(i)]['order_quantity']
    distanceMat[i+n_restaurants]=[distanceMat[0][i+n_restaurants]]+data['neighbourhoods']['n'+str(i)]['distances']


def tsp(graph):
    num_nodes = len(graph)

    # memoization table to store computed subproblems
    memo = {}

    def tsp_helper(mask, pos):
        # base case: all nodes visited
        if mask == (1 << num_nodes) - 1:
            return graph[pos][0], [pos, 0]

        # check if the subproblem is already solved
        if (mask, pos) in memo:
            return memo[(mask, pos)]

        min_cost = float('inf')
        min_path = []

        # try visiting each unvisited node
        for next_pos in range(num_nodes):
            if (mask >> next_pos) & 1 == 0:
                new_mask = mask | (1 << next_pos)
                cost, path = tsp_helper(new_mask, next_pos)
                cost += graph[pos][next_pos]

                if cost < min_cost:
                    min_cost = cost
                    min_path = [pos] + path

        memo[(mask, pos)] = min_cost, min_path
        return min_cost, min_path

    # start from node 0
    mask = 1  # 1 << 0
    start_pos = 0

    min_cost, min_path = tsp_helper(mask, start_pos)
    return min_cost, min_path



def firstFit(weight, n, c):
    final=[]
    res = 0
    bin_rem = [0]*n

    for i in range(n):
        j = 0
        while( j < res):
            if (bin_rem[j] >= weight[i]):
                bin_rem[j] = bin_rem[j] - weight[i]
                final[j].append(i+1)
                break
            j+=1
        if (j == res):
            bin_rem[res] = c - weight[i]
            final.append([i+1])
            res= res+1
    for i in range(res):
        final[i].insert(0,0)
    return final


vehicleqty=[[] for i in range(n_vehicles)]
curr=0
for i in range(n_neighbourhoods):
    curr=curr%n_vehicles
    vehicleqty[curr].append(quantity[i])
    curr+=1
nodes_to_traverse=[]
#print(vehicleqty)
for i in range(n_vehicles):
    nodes_to_traverse.append(firstFit(vehicleqty[i],len(vehicleqty[i]),vehiclecap[i]))
print(nodes_to_traverse)

#print(nodes_to_traverse)
#-------------------------------------------------------------------------------------------------
paths=[]
for k in range(len(nodes_to_traverse)):
    for l in range(len(nodes_to_traverse[k])):
        # Use list comprehensions to extract the submatrix
        result_matrix = [[distanceMat[i][j] for j in nodes_to_traverse[k][l]] for i in nodes_to_traverse[k][l]]
        #print(result_matrix)
        total_cost,tour=tsp(result_matrix)
        #print(tour)
        final=[]
        for i in tour:
            if(i<n_restaurants):
                final.append('r'+str(i))
            else:
                final.append('n'+str(nodes_to_traverse[k][l][i]-1))
        paths.append(final)
    #print(paths)



    result_json = {}

    for i, path in enumerate(paths, start=1):
        key = f"path{i}"
        result_json[key] = path

    result_dict = {"v"+str(k): result_json}
    result_json_string = json.dumps(result_dict, indent=2)

file_name = "level2a_output.json"
with open(file_name, "w") as json_file:
    json_file.write(result_json_string)
