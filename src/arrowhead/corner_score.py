import numpy as np

MIN_TAD_HEIGHT = 3
thresholds = [0.2, 0.5, 0.4]

def generate_arrowhead_matrix(M):
    column_size, row_size = M.shape
    A = np.zeros(M.shape)
    for i in range(column_size):
        for d in range(1, row_size - i):
            a = M[i, i + d]
            b = M[i, i - d] if i - d >= 0 else 0
            A[i, i + d] = (a - b) * (a + b)
            #A[i + d, i] = (a - b) * (a + b)  
            # if you want to visualize full arrowhead matrix, uncomment line above

    return A


# computes aggregate sum of values in both U and L triangles for each corner
# depending on type it returns sum of values, sum of signs or sum of squares
def compute_sum(A, type):
    N = A.shape[0]
    U = np.zeros(A.shape)
    L = np.zeros(A.shape)
    L_col = np.zeros(N)
    U_col = np.zeros(N)
    Row = np.zeros(N)
    if type == 'value':
        aggregate = np.sum
        value = lambda x: x
    elif type == 'sign':
        aggregate = lambda x: np.sum(np.sign(x))
        value = np.sign
    else:
        aggregate = lambda x: np.dot(x, x)
        value = lambda x: x * x

    for a in range(N):
        for b in range(a + 1, N):
            mid = (a + b + 1) // 2
            if a == 0:
                U_col[b] = aggregate(A[0:mid, b])
                L_col[b] = aggregate(A[mid:b, b])
                Row[b] = aggregate(A[b, (b + 1):(2 * b + 1)])
            else:
                U_col[b] -= value(A[a - 1, b])
                if (a + b) % 2 == 1:
                    mid_val = value(A[mid - 1, b])
                    U_col[b] += mid_val
                    L_col[b] -= mid_val
                last_row_index = 2 * b + 1 - a
                if last_row_index < N:
                    Row[b] -= value(A[b, last_row_index])
            U[a, b] = U[a, b - 1] + U_col[b]
            L[a, b] = L[a, b - 1] - L_col[b - 1] + Row[b]

    return [U, L]


# computes variance of N elements with sum S_1 and sum of squares S_2
def var(S_1, S_2, N):
    return (S_2 / N - (S_1 / N) ** 2) * (N / (N - 1)) if N > 1 else 0


# computes variance for each corner and mean sgn sum of U and L for each corner
def compute_variance_and_mean_sgn(A, U_sign, L_sign, U_sum, L_sum):
    U_sum_sq, L_sum_sq = compute_sum(A, 'square')
    # The matrices above will be reused to contain the mean sgn 
    # in U and L triangles for each corner (in order to save memory)
    U_mean_sgn = U_sum_sq
    L_mean_sgn = L_sum_sq

    N = A.shape[0]
    S_var = np.zeros(A.shape)
    for a in range(N):
        N_U = 0  # number of elements in U triangle
        N_L = 0  # number of elements in L triangle
        for b in range(a + 1, N):
            n = b - a
            N_U += (n + 1) // 2
            N_L += - (n - 1 - n // 2) + min(n, max(0, N - b - 1))
            if n >= MIN_TAD_HEIGHT:
                S_var[a, b] = var(U_sum[a, b], U_sum_sq[a, b], N_U) + var(L_sum[a, b], L_sum_sq[a, b], N_L)
                U_mean_sgn[a, b] = U_sign[a, b] / N_U
                L_mean_sgn[a, b] = L_sign[a, b] / N_L

    return [S_var, U_mean_sgn, L_mean_sgn]


def normalize(M):
    M /= np.max(M)


def compute_score_matrix(A):
    U_sign, L_sign = compute_sum(A, 'sign')
    U_sum, L_sum = compute_sum(A, 'value')
    S_var, U_mean_sgn, L_mean_sgn = compute_variance_and_mean_sgn(A, U_sign, L_sign, U_sum, L_sum)

    S_sum = L_sum
    S_sum -= U_sum
    normalize(S_sum)
    S_corner = S_sum  # reusing matrices to save memory

    S_sign = L_sign
    S_sign -= U_sign
    normalize(S_sign)
    S_corner += S_sign

    normalize(S_var)
    S_corner += S_var

    return [S_corner, S_var, U_mean_sgn, L_mean_sgn]


def compute_filtered_score_matrix(S_corner, S_var, U_mean_sgn, L_mean_sgn):
    N = S_corner.shape[0]
    t1, t2, t3 = thresholds
    S_filtered = S_corner.copy()

    # first pass
    for a in range(N):
        for b in range(a + 1, N):
            if b - a < MIN_TAD_HEIGHT or S_var[a, b] >= t1 or U_mean_sgn[a, b] >= -t2 or L_mean_sgn[a, b] <= t2:
                S_corner[a, b] = 0

    # second pass
    non_zero = np.zeros(N, dtype=int)
    for b in range(1, N):
        for a in range(b - MIN_TAD_HEIGHT, non_zero[b - 1] - 1, -1):
            if S_corner[a, b] != 0:
                non_zero[b] = a
                break
        if (non_zero[b] == 0):
            non_zero[b] = non_zero[b - 1]

    for a in range(N):
        for b in range(a + 1, N):
            if b - a < MIN_TAD_HEIGHT or non_zero[b] >= a or U_mean_sgn[a, b] >= -t3 or L_mean_sgn[a, b] <= t3:
                S_filtered[a, b] = 0

    S_filtered += S_corner
    return S_filtered
