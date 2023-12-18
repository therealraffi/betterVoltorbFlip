from itertools import combinations_with_replacement
from collections import Counter
import os

def find_combinations(n, k):
    combinations = combinations_with_replacement([1, 2, 3], k)
    valid_combinations = [comb for comb in combinations if sum(comb) == n]
    return valid_combinations

def find_pvals(points, voltorbs, free_cells):
    pvals = {i:0 for i in range(4)}
    combos = find_combinations(points, free_cells)

    for combo in combos:
        counts = dict(Counter(combo))
        for p in counts:
            pvals[p] += counts[p] / (free_cells + voltorbs)

    try:
        for p in pvals:
            pvals[p] = round(pvals[p]/len(combos), 3)
    
    except(ZeroDivisionError):
        raise(ValueError("Impossible value!"))
    
    # print()
    # print(free_cells)
    # print(combos)
    # print(pvals)
    try:
        pvals[0] = round( voltorbs / (voltorbs + free_cells), 3)
    except(ZeroDivisionError):
        return pvals, combos

    # s = sum([pvals[i] for i in pvals])
    # ev = round(sum([i * pvals[i] for i in pvals]), 3)
    # print("Sum:", s, "EV:", ev)

    return pvals, combos
    
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


# points = 6  # Total sum
# voltorbs = 2
# free_cells = 3
# pvals = find_pvals(points, voltorbs, free_cells)
# print(pvals)
