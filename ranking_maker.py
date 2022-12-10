import csv

#           pop	    avg	    pkb	    happ	sums
# pop	    1	    4	    4	    3	    12
# avg	    0,25	1	    6	    5	    12,25
# pkb	    0,25	0,16	1	    2	    3,416
# happ	    0,33	0,2	    0,5	    1	    2,03

# 	    pop	        avg	        pkb	        happ        
# pop	0,083333333	0,333333333	0,333333333	0,25
# avg	0,020408163	0,081632653	0,489795918	0,408163265
# pkb	0,073185012	0,046838407	0,292740047	0,585480094
# happ	0,162561576	0,098522167	0,246305419	0,492610837

# sum of each column gives us values for attribute_weights table
def remap_from_1_9_17_to_1over9_1_9(value):
    value = int(value)
    if value == 9:
        return 1
    if value > 9:
        return value - 8
    if value < 9:
        return 1 / (10 - value)


def make_importance_matrix(tab):
    size = 4
    cnt = 0
    matrix = [[None for _ in range(size)] for _ in range(size)]
    for i in range(0, size):
        matrix[i][i] = 1
        for j in range(i+1, size):
            matrix[i][j] = remap_from_1_9_17_to_1over9_1_9(tab[cnt])
            matrix[j][i] = 1/matrix[i][j]
            cnt += 1
    for row in matrix:
        print(row)
    return matrix

def calculate_importance(matrix):
    n = len(matrix)
    # matrix = [[i/j for i in tab] for j in tab]
    for i, x in enumerate(matrix):
        s = 0
        for y in x:
            s += y
        for j in range(n):
            matrix[i][j] /= s*n
    # print(matrix)
    prio_sums = [0] * 4
    for i in range(n):
        for j in range(n):
            prio_sums[i] += matrix[j][i]
    
    return prio_sums
# Importance of attributes calculated from matrix
attributes_weights = [
    0.140,
    0.434,
    0.086,
    0.340
    ]

# Function that takes mapped attributes and creates comparison matrix
def make_comparison_matrix(tab):
    n = len(tab)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i, x in enumerate(tab):
        for j, y in enumerate(tab):
            matrix[i][j] = x / y
    return matrix

# Function that takes matrix and normalizes it (sum(matrix[row]) == 1)
def normalize_rows_in_matrix_EVN(matrix):
    n = len(matrix)
    sums = [0] * n
    for j in range(n):
        for i in range(n):
            sums[i] += matrix[j][i]

    for j in range(n):
        for i in range(n):
            matrix[j][i] /= sums[i]

# Function that divides all values by size of matrix
def weights_of_attributes(matrix):
    n = len(matrix)
    sums = [0] * n
    for j in range(n):
        sums[j] = sum(matrix[j])
    for j in range(n):
        sums[j] = round(sums[j] / n, 2)
    return sums

# Function mapping our range of values from (0, max_val) to (1, 9)
def map_values_to_1_9_scale(tab, vmax, proportional = True):
    n = len(tab)
    # # scale down to 0...
    # vmin = min(tab)
    # for i in range(n):
    #     tab[i] = tab[i] / vmin - 1

    # scale up to 1...9
    for i in range(n):
        tab[i] = tab[i] * 8 / vmax + 1

    # invert if not proportional
    if not proportional:
        for i in range(n):
            tab[i] = 10 - tab[i]
    return tab

# Function that takes all mapped attributes for all countries and drives all other calculations for it
def calc_weights_EVM(mapped_all):
    weights = []
    for mapped in mapped_all: # for life happiness population and pkb EVM
        comp_matrix = make_comparison_matrix(mapped) # make matrixes for each attr
        normalize_rows_in_matrix_EVN(comp_matrix) # scale rows to make sum of each equal 1
        weights.append(weights_of_attributes(comp_matrix)) # divide all values by number of rows to make whole matrix sum equal 1
    return weights # return all weights ( 2D )

# Function that multiplies our result weights with our set importance of each attribute. Returning single ranking value for each country
def multiply_by_attr_weights(weights, attr_weights):
    nattr = len(attr_weights)
    nweig = len(weights[0])
    for i in range(nattr):
        for j in range(nweig):
            weights[i][j] *= attr_weights[i]

    pre_ranking = [0] * nweig
    for i in range(nattr):
        for j in range(nweig):
            pre_ranking[j] += weights[i][j]
    return pre_ranking

def swap_em(xd):
    xd[0], xd[1], xd[2], xd[3]= xd[1], xd[3], xd[0], xd[2]
    return xd

# Main driver function
def calculate_ranking(prio, country_names_list):
    # Read all countries from .csv
    with open("countries.csv") as file:
        csvreader = csv.reader(file)

        # Pick only choosen countries from list
        rows = []
        countries_dict = {}
        for row in csvreader:
            rows.append(row)
            if row[0] in country_names_list:
                countries_dict[row[0]] = row[1:]

    # Make values lists of each attribute
    avg_life =      [float(x[0]) for x in countries_dict.values()]
    happiness =     [float(x[1]) for x in countries_dict.values()]
    population =    [float(x[2]) for x in countries_dict.values()]
    pbk =           [float(x[3]) for x in countries_dict.values()]

    # Map all the lists to 1-9 scale
    mapped_avg_life =   map_values_to_1_9_scale(avg_life, 100)
    mapped_happiness =  map_values_to_1_9_scale(happiness, 10)
    mapped_population = map_values_to_1_9_scale(population, 300, False) # because smaller is better here
    mapped_pbk =        map_values_to_1_9_scale(pbk, 100000)

    mapped_all = [
        mapped_avg_life,
        mapped_happiness,
        mapped_population,
        mapped_pbk
    ]
    # Calc importance matrix
    imp_mtx = make_importance_matrix(prio)
    attributes_weights = calculate_importance(imp_mtx)
    attributes_weights = swap_em(attributes_weights)
    print(attributes_weights[0], "Population")
    print(attributes_weights[1], "Average lifetime")
    print(attributes_weights[2], "PKB")
    print(attributes_weights[3], "Happiness")
    print(attributes_weights)



    # Calculate all ranking values
    weights = calc_weights_EVM(mapped_all) 
    pre_ranking = multiply_by_attr_weights(weights, attributes_weights) # multiply all weights by their importance

    # Attach country names to values and sort by value
    ranking = [[x, round(pre_ranking[i], 3)] for i, x in enumerate(countries_dict.keys())] 
    # Sort ranking table
    ranking.sort(key=lambda x:x[1], reverse=True) 

    # Make output list for GUI
    final = []
    for i, row in enumerate(ranking):
        # final.append([i+1, row[0]])
        final.append(str(i+1) + ". " + row[0]) # format recieved by gui
    return final

# prio = [1,1,17,1,17,17]
# prio = [12, 12, 11, 14, 13, 10]
# imp_mtx = make_importance_matrix(prio)
# attributes_weights = calculate_importance(imp_mtx)
# attributes_weights = swap_em(attributes_weights)
# print(attributes_weights, sum(attributes_weights))