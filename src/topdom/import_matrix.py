import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse

import utils.HiCtoolbox as HiCtoolbox

HiCfilename = './chr21_25kb.RAWobserved.txt'
R = 100000
alpha = 0.227


def import_normalized_matrix(file, compression, alpha):
    A = np.loadtxt(file)
    A = np.int_(A)
    A = np.concatenate((A, np.transpose(np.array([A[:, 1], A[:, 0], A[:, 2]]))), axis=0)  # build array at pb resolution
    A = sparse.coo_matrix((A[:, 2], (A[:, 0], A[:, 1])))
    binned_map = HiCtoolbox.bin2d(A, compression, compression)  # !become csr sparse array
    del A
    contact_map = HiCtoolbox.SCN(binned_map)
    contact_map = np.asarray(contact_map) ** alpha  # now we are not sparse at all
    dist_matrix = HiCtoolbox.fastFloyd(1 / contact_map)  # shortest path on the matrix
    dist_matrix = dist_matrix - np.diag(np.diag(dist_matrix))  # remove the diagonal
    dist_matrix = (dist_matrix + np.transpose(
        dist_matrix)) / 2;  # just to be sure that the matrix is symetric, not really usefull in theory
    return dist_matrix


def import_matrix(file, compression):
    A = np.loadtxt(file)
    A = np.int_(A)
    A = np.concatenate((A, np.transpose(np.array([A[:, 1], A[:, 0], A[:, 2]]))), axis=0)  # build array at pb resolution
    A = sparse.coo_matrix((A[:, 2], (A[:, 0], A[:, 1])))
    binned_map = HiCtoolbox.bin2d(A, compression, compression)  # !become csr sparse array
    del A
    return binned_map.toarray()


if __name__ == "__main__":
    plt.imshow(import_matrix(HiCfilename, R), cmap='Wistia')
    plt.show()
