import csv

attributes_weights = [
    0.140,
    0.434,
    0.084,
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

# Function that calculates total weights for each attribute
def weights_of_attributes(matrix):
    n = len(matrix)
    sums = [0] * n
    for j in range(n):
        sums[j] = sum(matrix[j])
    for j in range(n):
        sums[j] = round(sums[j] / n, 2)
    return sums

# Function mapping our range of values from (min_val, max_val) to (1, 9)
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
def calculate_weights(mapped_all):
    weights = []
    for mapped in mapped_all:
        comp_matrix = make_comparison_matrix(mapped)
        normalize_rows_in_matrix_EVN(comp_matrix)
        weights.append(weights_of_attributes(comp_matrix))
    return weights

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

# Main driver function
def calculate_ranking(country_names_list):
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

    # Calculate all ranking values
    weights = calculate_weights(mapped_all)
    pre_ranking = multiply_by_attr_weights(weights, attributes_weights)

    # Attach country names to values and sort by value
    ranking = [[x, round(pre_ranking[i], 3)] for i, x in enumerate(countries_dict.keys())]
    ranking.sort(key=lambda x:x[1], reverse=True)

    # Make output list for GUI
    final = []
    for i, row in enumerate(ranking):
        # final.append([i+1, row[0]])
        final.append(str(i+1) + ". " + row[0])
    return final
