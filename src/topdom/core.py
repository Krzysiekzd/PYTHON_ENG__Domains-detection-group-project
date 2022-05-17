import math
import warnings

import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

import topdom.import_matrix as import_matrix

warnings.filterwarnings("ignore")


def l2d_to_1d(list2d):
    # Flattens 2D list to 1D (for wilcoxon function)
    return [j for i in list2d for j in i]


def generate_binsignal(matrix, k):
    # Calculate mean value of the interactions for k-neighborhood of each bin. If unable to, assign 0 instead.
    binsignal = [matrix[0,0] if not math.isnan(matrix[0,0]) and not math.isinf(matrix[0,0]) else 0]
    for i in range(1,len(matrix)):
        sig = matrix[0 if i-k<0 else i-k : i, i:i + k].mean()
        binsignal.append(0 if math.isinf(sig) else sig)
    return binsignal


def flatten_binsignal(binsignal, sensitivity, bins):
    # Algorithm explanation - link below:
    # https://drive.google.com/file/d/13iEmGw6RxeWfnzsDbzO1WL9vHXpSi_Uf/view?usp=sharing

    # Step 1. Replace binsignal with local extremes
    extremes_positions = [0]
    extremes_values = [binsignal[0]]
    for i in range(1, len(binsignal) - 1):
        if binsignal[i - 1] > binsignal[i] < binsignal[i + 1]:
            extremes_positions.append(bins[i])
            extremes_values.append(binsignal[i])
        elif binsignal[i - 1] < binsignal[i] > binsignal[i + 1]:
            extremes_positions.append(bins[i])
            extremes_values.append(binsignal[i])
    extremes_positions.append(len(binsignal)-1)
    extremes_values.append(binsignal[-1])
    # Step 2. Calculate maximum and minimum value and multiply their difference by sensitivity parameter
    min_bin = min(binsignal)
    max_bin = max(binsignal)
    diff = (max_bin - min_bin) * sensitivity

    # Step 3. Filter out noise in the data, by replacing regions with fluctuations below calculated number
    # with flat lines

    # Find regions that will be replaced with flat lines
    # note: these regions will be represented in flat_areas list as tuples - (a,b), where a,b are indexes
    # of extremes_positions list - different from bins' indexes
    flat_areas = []
    flat_area_beginning = 0
    for i in range(1, len(extremes_positions)-1):
        if abs(extremes_values[i] - extremes_values[i - 1]) > diff:
            if extremes_positions[i - 1] - extremes_positions[flat_area_beginning] > 1:
                flat_areas.append((flat_area_beginning, i - 1))
            flat_area_beginning = i
    if flat_area_beginning!=i-1:
        flat_areas.append((flat_area_beginning, i-1))

    # Replace found regions in binsignal with 2 points (start and end coordinates)
    new_binsignal_positions = [0]
    new_binsignal_values = [binsignal[0]]
    last = 0
    for i in flat_areas:
        # To new binsignal, add regions that are in between flat areas
        new_binsignal_positions += extremes_positions[last + 1:i[0]]
        new_binsignal_values += extremes_values[last + 1:i[0]]

        new_binsignal_positions.append(extremes_positions[i[0]])
        new_binsignal_positions.append(extremes_positions[i[1]])
        value = (extremes_values[i[0]] + extremes_values[i[1]]) / 2
        new_binsignal_values.append(value)
        new_binsignal_values.append(value)
        last = i[1]
    new_binsignal_positions.append(extremes_positions[-1])
    new_binsignal_values.append(extremes_values[-1])

    return new_binsignal_positions, new_binsignal_values


def find_minimums(posits, vals):
    # This function is used to return informations about minimums in flattened binsignal.
    # Note: It will return first and last elements as minimums.
    min_positions = [posits[0]]
    min_values = [vals[0]]
    last_min_index = 0
    is_descending = False

    for i in range(1, len(vals)):
        if vals[i] < vals[i-1]:
            last_min_index = i
            is_descending = True
        elif vals[i] > vals[i-1]:
            if is_descending:
                min_positions.append(posits[last_min_index])
                min_values.append(vals[last_min_index])
            is_descending = False
    min_positions.append(posits[-1])
    min_values.append(vals[-1])

    return min_positions, min_values


def statistical_filtering(matrix, min_coords, wsize, msize):
    # For each minimum, we examine the hypothesis (using the wilcoxon test)
    # that it comes (with window size accuracy) from the same distribution as its neighborhood
    p_values = []
    for i in min_coords:
        lower = max(1, i - wsize)
        up_mtx = matrix[lower:i, lower:i]
        upper = min(i + wsize, msize)
        down_mtx = matrix[i:upper, i:upper]
        middle_up = matrix[i:upper, lower:i]
        middle_down = matrix[lower:i, i:upper]
        middle_lst = l2d_to_1d(middle_up) + l2d_to_1d(middle_down)
        corner_lst = l2d_to_1d(down_mtx) + l2d_to_1d(up_mtx)
        if len(middle_lst) == len(corner_lst):
            p_values.append(wilcoxon(middle_lst, corner_lst).pvalue)
        else:
            p_values.append(0)
    return p_values


def filter_coords(coords, p_values, p_limit):
    # Deletes coordinates with a p-value less than the set limit 
    delete = []
    for i in range(len(coords)):
        if max(p_values[i], p_values[i + 1]) > p_limit:
            delete.append(i)
    delete.reverse()
    for i in delete:
        coords.pop(i)

def topdom(np_matrix, window_size, sensitivity, pval_limit):
    #Step 1 - generate binsignal from matrix
    binsignal = generate_binsignal(np_matrix, window_size)
    bins = list(range(len(np_matrix)))
    #Step 2 - Flatten binsignal and find minima
    flattened_binsignal_positions, flatenned_binsignal_values = flatten_binsignal(binsignal, sensitivity, bins)
    minima_positions, minima_values = find_minimums(flattened_binsignal_positions, flatenned_binsignal_values)
    tad_coords = [(minima_positions[i], minima_positions[i + 1]) for i in range(len(minima_positions) - 1) ]
    #Step 3 - Filter results
    p_values = statistical_filtering(np_matrix, minima_positions, window_size, len(np_matrix) - window_size)
    filter_coords(tad_coords, p_values, pval_limit)
    return tad_coords


def run(matrix_filepath, R, alpha=None, window_size=5, sensitivity=0.04, pval_limit=0.05):
    if alpha is not None:
        mtx = import_matrix.import_normalized_matrix(matrix_filepath, R, alpha)
    else:
        mtx = import_matrix.import_matrix(matrix_filepath, R)
    topdom_coords = topdom(np_matrix=mtx, window_size=window_size, sensitivity=sensitivity, pval_limit=pval_limit)
    return mtx, topdom_coords


if __name__ == "__main__":
    # Mainly to debug
    a = import_matrix.import_matrix('insert_path_here', 25000)
    win = 5
    sns = 0.04
    pval = 0.05
    print("Window size: " + str(win) + ", sensitivity: " + str(sns))
    topdom(a, win, sns, pval)
