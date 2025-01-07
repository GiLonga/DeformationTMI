import numpy as np
from sklearn.neighbors import KDTree, NearestNeighbors
import scipy
import scipy.spatial
import pickle
from tqdm.auto import tqdm


def load_ints(path, from_matlab=False):
    vals = np.loadtxt(path,dtype=int)
    if from_matlab:
        vals -= 1
    return vals


def save_ints(path, vals, to_matlab=False):
    if to_matlab:
        vals += 1

    np.savetxt(path, vals, fmt='%d')


def save_pickle(path, vals):
    pickle.dump(vals, open(path,"wb"))


def load_pickle(path):
    return pickle.load(open(path,"rb"))


def knn_query(X, Y, k=1, return_distance=False, use_scipy=False, dual_tree=False, n_jobs=1):

    if use_scipy:
        tree = scipy.spatial.KDTree(X)
        dists, matches = tree.query(Y, k=k, workers=n_jobs)
        if k == 1:
            dists = dists.squeeze()
            matches = matches.squeeze()
    else:
        # if n_jobs == 1:
        #     tree = KDTree(X, leaf_size=40)
        #     dists, matches = tree.query(Y, k=k, return_distance=True)
        # else:
        tree = NearestNeighbors(n_neighbors=k, leaf_size=40, algorithm="kd_tree", n_jobs=n_jobs)
        tree.fit(X)
        dists, matches = tree.kneighbors(Y)
        if k == 1:
            dists = dists.squeeze()
            matches = matches.squeeze()

    if return_distance:
        return dists, matches
    return matches


def knn_query_normals(X, Y, normals1, normals2, k_base=30, return_distance=False, n_jobs=1, verbose=False):
    """
    Compute a NN query ensuring normal consistency.
    k_base determines the number of neighbors first computed for faster computation.
    """
    final_matches = np.zeros(Y.shape[0], dtype=int)
    final_dists = np.zeros(Y.shape[0])

    # FIRST DO KNN SEARCH HOPING TO OBTAIN FAST
    # tree = KDTree(X)  # Tree on (n1,)
    # dists, matches = tree.query(Y, k=k_base, return_distance=True)  # (n2,k), (n2,k)

    dists, matches = knn_query(X, Y, k=k_base, return_distance=True, n_jobs=n_jobs)

    # Check for which vertices the solution is already computed
    isvalid = np.einsum('nkp,np->nk', normals1[matches], normals2) > 0  # (n2, k)
    valid_row = isvalid.sum(1) > 0

    valid_inds = valid_row.nonzero()[0]  # (n',)
    invalid_inds = (~valid_row).nonzero()[0]  # (n2-n')

    if verbose:
        print(f'{valid_inds.size} direct matches and {invalid_inds.size} specific indices')

    # Fill the known values
    final_matches[valid_inds] = matches[(valid_inds, isvalid[valid_inds].argmax(axis=1))]
    if return_distance:
        final_dists[valid_inds] = dists[(valid_inds, isvalid[valid_inds].argmax(axis=1))]

    # Individually check other indices
    n_other = invalid_inds.size
    myit = range(n_other)
    for inv_ind in myit:
        vert_ind = invalid_inds[inv_ind]
        possible_inds = np.nonzero(normals1 @ normals2[vert_ind] > 0)[0]

        if len(possible_inds) == 0:
            final_matches[vert_ind] = matches[vert_ind,0]
            final_dists[vert_ind] = dists[vert_ind,0]
            continue

        tree = KDTree(X[possible_inds])
        temp_dist, temp_match_red = tree.query(Y[None, vert_ind], k=1, return_distance=True)

        final_matches[vert_ind] = possible_inds[temp_match_red.item()]
        final_dists[vert_ind] = temp_dist.item()

    if return_distance:
        return final_dists, final_matches
    return final_matches


def rotation(theta, axis):
    rot = np.zeros((3,3))

    rot[axis, axis] = 1

    inds = [i for i in range(3) if i != axis]
    rot[np.ix_(inds, inds)] = np.array([[np.cos(theta), -np.sin(theta)],
                                        [np.sin(theta), np.cos(theta)]])

    return rot


def rotx(theta):
    return rotation(theta, 0)


def roty(theta):
    return rotation(theta, 1)


def rotz(theta):
    return rotation(theta, 2)


def rigid_alignment(X1, X2, p2p_12=None, weights=None, return_params=False, return_deformed=True):
    """
    Solve optimal R and t so that
    || X1@R.T + t - X2 || is minimized

    X1 : (n1,3)
    X2 : (n2,3)
    p2p_12 : (n1,) point to point from X1 to X2
    weights : (n1,)

    Returns deformed X1
    """
    if not (return_params or return_deformed):
        raise ValueError("Choose something to return")

    X = X1  # (n1,3)
    Y = X2[p2p_12] if p2p_12 is not None else X2  # (n1,3)

    if weights is None:
        X_cent = X.mean(axis=0)
        Y_cent = Y.mean(axis=0)
    else:
        weights /= weights.sum()
        X_cent = (weights[:, None]*X).sum(axis=0)
        Y_cent = (weights[:, None]*Y).sum(axis=0)

    X_bar = X - X_cent
    Y_bar = Y - Y_cent

    if weights is None:
        H = X_bar.T @ Y_bar  # (3,3)
    else:
        H = X_bar.T @ (weights[:, None]*Y_bar)  # (3,3)

    U, _, VT = scipy.linalg.svd(H)
    theta = VT.T @ U.T

    if np.isclose(scipy.linalg.det(theta), -1):
        U[:, -1] *= -1
        theta = VT.T @ U.T

    t = Y_cent - X_cent@theta.T

    if not return_deformed:
        return theta, t

    X_new = X@theta.T + t

    if not return_params:
        return X_new

    else:
        return X_new, theta, t


def icp_align(X1, X2, p2p_12=None, weights=None, return_params=False, n_iter=50, epsilon=1e-8, n_jobs=1, verbose=False):
    """
    Solve optimal R and t so that
    || X1@R.T + t - X2 || is minimized
    using ICP

    X1 : (n1,3)
    X2 : (n2,3)
    p2p : (n1,) point to point from X1 to X2

    Returns deformed X1
    """
    tree = NearestNeighbors(n_neighbors=1, leaf_size=40, algorithm="kd_tree", n_jobs=n_jobs)
    tree.fit(X2)

    if p2p_12 is None:
        _, p2p_12 = tree.kneighbors(X1)
        p2p_12 = p2p_12.squeeze()

    X_curr = X1.copy()
    theta_curr = np.eye(3)
    t_curr = np.zeros(3)
    criteria = np.inf
    iteration = 0

    iterable = tqdm(range(n_iter)) if verbose else range(n_iter)
    for iteration in iterable:
        res_icp = rigid_alignment(X_curr, X2, p2p_12=p2p_12, weights=weights, return_params=return_params)

        if return_params:
            X_new, theta, t = res_icp
            theta_curr = theta @ theta_curr
            t_curr = theta @ t_curr + t
        else:
            X_new = res_icp

        _, p2p_12 = tree.kneighbors(X_new)
        p2p_12 = p2p_12.squeeze()

        criteria = np.linalg.norm(X_new - X_curr)
        X_curr = X_new.copy()

        if criteria < epsilon:
            break

    if verbose:
        print(f'Aligned using ICP in {iteration} iterations')

    if return_params:
        return X_new, theta_curr, t_curr

    return X_new