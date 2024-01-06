
# extracting data from json file 

import pandas as pd
import json

with open('Student Handout/Input data/level0.json', 'r') as f:
  data = json.load(f)


import json

def tsp_nearest_neighbor_with_cost(matrix):
    num_nodes = len(matrix)
    unvisited_nodes = set(range(1, num_nodes))
    current_node = 0  # Start from node 0
    tour = [current_node]

    total_cost = 0

    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda node: matrix[current_node][node])
        total_cost += matrix[current_node][nearest_node]
        tour.append(nearest_node)
        unvisited_nodes.remove(nearest_node)
        current_node = nearest_node

    # Return to the starting node to complete the tour
    tour.append(tour[0])
    return tour,total_cost


n_neighbourhoods=(data['n_neighbourhoods'])
n_restaurants=(data['n_restaurants'])
quantity=[0 for i in range(n_neighbourhoods)]
distanceMat=[[0]*(n_neighbourhoods+n_restaurants+1) for i in range(n_neighbourhoods+n_restaurants)]



for i in range(n_restaurants):
    distanceMat[i]=data['restaurants']['r'+str(i)]["restaurant_distance"]+data['restaurants']['r'+str(i)]["neighbourhood_distance"]
for i in range(n_neighbourhoods):
    quantity[i]=data['neighbourhoods']['n'+str(i)]['order_quantity']
    distanceMat[i+n_restaurants]=[distanceMat[0][i+n_restaurants]]+data['neighbourhoods']['n'+str(i)]['distances']


tour, tour_cost = tsp_nearest_neighbor_with_cost(distanceMat)
print("Tour:", tour)
print("Tour Cost:", tour_cost)



final=[]
for i in tour:
    if(i<n_restaurants):
        final.append('r'+str(i))
    else:
        final.append('n'+str(i-1))


def convert_to_json(node_list):
    if not node_list:
        return None

    start_node = node_list[0]
    end_node = node_list[-1]

    json_data = {
        f"v0": {
            "path": node_list
        }
    }

    with open("level0_output.json", "w") as json_file:
        json.dump(json_data, json_file, indent=2)

convert_to_json(final)

