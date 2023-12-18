from itertools import combinations_with_replacement
from collections import Counter
import os
from copy import deepcopy

def find_combos(points, voltorbs, free_cells):
    all_combinations = combinations_with_replacement([1, 2, 3], free_cells)
    combos = [comb for comb in all_combinations if sum(comb) == points]
    combos = [list(combo) for combo in combos]
    for i in range(len(combos)):
        combos[i] = list(combos[i])
        combos[i].extend([0] * voltorbs)
    
    return combos

def combine_combos(row_combos, col_combos):
    row_vals = set()
    for combo in row_combos:
        for k in combo:
            row_vals.add(k)
    
    col_vals = set()
    for combo in col_combos:
        for k in combo:
            col_vals.add(k)

    filtered_vals = set()
    for val in row_vals:
        if val in col_vals:
            filtered_vals.add(val)

    if col_vals != row_vals:
        filtered_col_combos = []
        filtered_row_combos = []

        for combo in row_combos:
            contains = False
            for v in filtered_vals:
                if v in combo:
                    contains = True
                    break
            
            if contains:
                filtered_row_combos.append(combo)
        
        for combo in col_combos:
            contains = False
            for v in filtered_vals:
                if v in combo:
                    contains = True
                    break
            
            if contains :
                filtered_col_combos.append(combo)
        
        return [filtered_row_combos, filtered_col_combos], filtered_vals
    
    else:
        return [row_combos, col_combos], filtered_vals
    
def updated_combos(val, combos):
    final_combos = []
    for combo in combos:
        if val in combo:
            combo.remove(val)
            final_combos.append(combo)

    return final_combos

def get_probs(pvals, row_combos, col_combos):
    row_probs = {i:0 for i in range(4)}
    col_probs = {i:0 for i in range(4)}
    probs = {i:0 for i in range(4)}

    for combo in row_combos:
        counts = dict(Counter(combo))
        for p in counts:
            row_probs[p] += (counts[p] / len(combo)) / len(row_combos)
    
    for combo in col_combos:
        counts = dict(Counter(combo))
        for p in counts:
            col_probs[p] += (counts[p] / len(combo)) / len(col_combos)
    
    s = 0
    for p in probs:
        probs[p] = col_probs[p] * row_probs[p]
        s += probs[p]
    for p in probs:
        probs[p] = round(probs[p] / s, 3)
    
    return probs

points = 6  # Total sum
voltorbs = 1
free_cells = 2
row_combos = find_combos(points, voltorbs, free_cells)

points = 7  # Total sum
voltorbs = 2
free_cells = 3
col_combos = find_combos(points, voltorbs, free_cells)

final_combos, pvals = combine_combos(row_combos, col_combos)
probs = get_probs(pvals, row_combos, col_combos)

print("OG ROW:", row_combos)
print("OG COL:", col_combos)
print("MERGED COMBOS:", final_combos)
print("Possible Vals:", pvals)
print("Probs:", probs)

choice = 2
final_combos[0] = updated_combos(choice, final_combos[0])
final_combos[1] = updated_combos(choice, final_combos[1])

print("CHOICE:", choice)
print("FINAL COMBOS:", final_combos)

'''
STEPS:
1. update (x, y) with choice
2. update row x, col y with updated_combos
3. for each col on row x, update cells/col with  combine_combos
4. for each row on col x, update cells/rows with combine_combos


'''

def get_most_recently_added_file(directory):
    # Get list of .png files in the directory with their full path
    png_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith('.png')]

    if not png_files:
        return None  # No .png files found in the directory

    # Find the most recently added .png file (based on creation time)
    newest_png_file = max(png_files, key=os.path.getctime)
    return newest_png_file

# # Example usage
# directory_path = '/Users/raffukhondaker/Desktop'  # Replace with your directory path
# most_recent_file = get_most_recently_added_file(directory_path)
# print(f"The most recently added file is: {most_recent_file}")