import argparse
import random
import sys
import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# This script creates toy matrix with given parameters, that can be used for testing purposes.

def create_square(matrix, size, left_up_corner, min_value, max_value):
    for i in range(size):
        for j in range(size):
            matrix[left_up_corner + i][left_up_corner + j] = max(matrix[left_up_corner + i][left_up_corner + j], random.randint(min_value, max_value))
    print('Positions from: {} to: {}, values from: {} to {}'.format(left_up_corner, left_up_corner + size,
                                                                min_value, max_value))


def extract_args():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("-s", "--size", required=False, help="size of square")
    ap.add_argument("-hs", "--hics", required=False, help="number of hics")
    args = vars(ap.parse_args(sys.argv[1:]))
    return int(args.get('size') or 300), int(args.get('hics') or 10)


def new_initialized_matrix(low, high, size_of_matrix):
    output = np.random.randint(low=low, high=high, size=(size_of_matrix, size_of_matrix), dtype=np.int8)
    output[299][0] = 100
    output[299][1] = 0
    return output


def symmetrize_matrix(matrix):
    size_of_matrix = matrix.shape[0]
    for i in range(size_of_matrix):
        for j in range(size_of_matrix - i):
            matrix[i][j] = matrix[j][i]
    return matrix


def display_matrix(matrix, should_save=False, filename="hic.png"):
    plot = sns.heatmap(matrix, cmap='YlOrRd')
    if should_save:
        figure = plot.get_figure()
        figure.savefig(filename, dpi=600)
    plt.show()


def propose_hic_tree(depth, lower_bound, upper_bound, init_run=False):
    print(lower_bound, upper_bound)
    output = Proposition()
    if depth >= 1 and lower_bound != upper_bound:
        rand1, rand2 = random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound)
        start = min(rand1, rand2)
        if bool(random.getrandbits(1)):
            start = lower_bound
        end = max(rand1, rand2)
        if bool(random.getrandbits(1)):
            end = upper_bound
        intervals = [(start, end)]

        if bool(random.getrandbits(1)) or init_run:
            if start - lower_bound > 15:
                rand1, rand2 = random.randint(lower_bound, start), random.randint(lower_bound, start)
                sibling_start = min(rand1, rand2)
                sibling_end = max(rand1, rand2)
                intervals.append((sibling_start, sibling_end))
            elif upper_bound - end > 15:
                rand1, rand2 = random.randint(end, upper_bound), random.randint(end, upper_bound)
                sibling_start = min(rand1, rand2)
                sibling_end = max(rand1, rand2)
                intervals.append((sibling_start, sibling_end))

        output.intervals = intervals
        output.children = [propose_hic_tree(depth - 1, interval_start, interval_end) for (interval_start, interval_end) in intervals]
    return output


class Proposition:
    intervals = []
    children = []

    def __init__(self):
        self.intervals = []
        self.children = []

    def __str__(self):
        if len(self.intervals) == 0:
            return ""
        else:
            return str(self.intervals) + "".join([str(proposition) for proposition in self.children])


def random_interval_range(current_depth, depth, min_value, max_value):
    dimension_size = math.floor(max_value / depth)
    start_val = max(current_depth * dimension_size, min_value)
    end_val = min((current_depth + 1) * dimension_size, max_value)
    return start_val, end_val


def inject_propositions_to_matrix(matrix, proposition, depth, current_depth=0):
    for (interval_start, interval_end) in proposition.intervals:
        density_low, density_up = random_interval_range(current_depth, depth, 0, 100)
        create_square(matrix, interval_end - interval_start, interval_start, density_low, density_up)
    for child in proposition.children:
        inject_propositions_to_matrix(matrix, child, depth, current_depth + 1)


def list_to_intervals(list, min_value, max_value):
    previous = min_value
    output = []
    for el in list:
        output.append((previous, el))
        previous = el
    output.append((el, max_value))
    return output


if __name__ == '__main__':
    size, hics_amount = extract_args()
    HIC_MAX_DEPTH = 4
    matrix = new_initialized_matrix(10, 30, size)
    matrix = symmetrize_matrix(matrix)
    random_split_points = sorted(random.sample(range(0, size), hics_amount))
    initial_split = list_to_intervals(random_split_points, 0, size)
    random_split_points_for_soft = sorted(random.sample(range(0, size), hics_amount))
    initial_split_for_soft = list_to_intervals(random_split_points_for_soft, 0, size)
    propositions = [propose_hic_tree(HIC_MAX_DEPTH, min, max, True) for (min, max) in initial_split]
    for (min_val, max_val) in initial_split:
        create_square(matrix, max_val - min_val, min_val, 30, 85)
    for (min_val, max_val) in initial_split_for_soft:
        create_square(matrix, max_val - min_val, min_val, 15, 45)
    for proposition in propositions:
        inject_propositions_to_matrix(matrix, proposition, HIC_MAX_DEPTH)
    display_matrix(matrix)


