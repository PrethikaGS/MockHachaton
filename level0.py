
# extracting data from json file 

import pandas as pd
import json


with open('Student Handout/Input data/level0.json', 'r') as f:
  data = json.load(f)


n_neighbourhoods=(data['n_neighbourhoods'])
n_restaurants=(data['n_restaurants'])
quantity=[0 for i in range(n_neighbourhoods)]
distanceMat=[[0]*n_neighbourhoods for i in range(n_neighbourhoods)]
restaurantMat=[[0]*(n_neighbourhoods+n_restaurants) for i in range(n_restaurants)]


for i in range(n_neighbourhoods):
    quantity[i]=data['neighbourhoods']['n'+str(i)]['order_quantity']
    distanceMat[i]=data['neighbourhoods']['n'+str(i)]['distances']
for i in range(n_restaurants):
    restaurantMat[i]=data['restaurants']['r'+str(i)]["restaurant_distance"]+data['restaurants']['r'+str(i)]["neighbourhood_distance"]


