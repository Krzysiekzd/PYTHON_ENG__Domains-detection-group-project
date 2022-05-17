from scipy import sparse
import utils.HiCtoolbox as HiCtoolbox
from arrowhead.connected_components import largest_value_within_components
from arrowhead.corner_score import *
from plots.plots import *


R = 100000


def import_matrix(file):
    A = np.loadtxt(file)
    A = np.int_(A)
    A = np.concatenate((A, np.transpose(np.array([A[:, 1], A[:, 0], A[:, 2]]))), axis=0)  # build array at pb resolution
    A = sparse.coo_matrix((A[:, 2], (A[:, 0], A[:, 1])))
    binned_map = HiCtoolbox.bin2d(A, R, R)  # !become csr sparse array
    del A
    return binned_map.toarray().astype(np.float64)


def load_test_matrix():
    return np.loadtxt('data/hic_matrix.csv', delimiter=',', dtype=np.float64)


def compute_algorithm(A):
    normalize(A)
    arrowhead_matrix = generate_arrowhead_matrix(A)
    S_corner, S_var, U_mean_sgn, L_mean_sgn = compute_score_matrix(arrowhead_matrix)
    S = compute_filtered_score_matrix(S_corner, S_var, U_mean_sgn, L_mean_sgn)
    results = largest_value_within_components(S)
    return results


def run(matrix_file_path):
    mtx = import_matrix(matrix_file_path)
    results = compute_algorithm(mtx)
    return mtx, results