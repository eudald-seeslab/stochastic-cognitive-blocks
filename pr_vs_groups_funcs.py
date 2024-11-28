import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import stats
import seaborn as sb


n_iterations = 20


def compute_cors(dataframe, group, memberships, random_links=False, block_random_links=False, verbose=False):
    correlations = dict()
    for classroom_id in dataframe.classroom.unique():
        # Get classroom
        one_class = dataframe.loc[dataframe.classroom == classroom_id, ["period", "gender", "student", "value"]].rename(
            columns={"student": "source", "value": "target"})

        if random_links:
            one_class["source"] = np.random.permutation(one_class["source"])
        if block_random_links:
            indices = one_class["source"].unique()
            one_class = one_class.replace({"source": dict(zip(indices, np.random.permutation(indices)))})

        # Get period
        period = one_class.period.values[0]
        one_class = one_class.drop(["period"], axis=1).dropna()

        gn = nx.from_pandas_edgelist(one_class, create_using=nx.DiGraph)
        pr = nx.pagerank_numpy(gn)
        values = np.array(list(pr.values()))
        prs = pd.DataFrame({"index": [str(int(a)) for a in list(gn.nodes)], "pr": values})
        aa = memberships.merge(prs, how="right").dropna()

        # Add correlation to cors dict with appropriate course
        try:
            correlations.setdefault(period, []).append(stats.spearmanr(aa[group], aa.pr))
        except ValueError:
            if verbose:
                print(aa)

    return correlations


def compute_correlation_means(correlations, output=False, plots=False):
    correlations = dict(sorted(correlations.items()))
    correlation_means = dict()
    for per, vals in correlations.items():

        vals = np.array([a[0] for a in vals])
        vals = vals[np.isfinite(vals)]
        m = np.mean(vals)
        sd = np.std(vals)
        correlation_means.setdefault(per, []).append((m, sd, len(vals), vals))

        if output:
            print(f"Period {per}")

            print(f"Mean correlation = {m}")
            print(f"Standard deviation = {sd}")

            print(stats.ttest_1samp(vals, 0))

        if plots:

            plt.figure(per)
            sb.histplot(vals)

    return correlation_means


def compute_iteration_means(results, course):
    m = np.mean([a[course][0][0] for a in results.values()])
    s = np.mean([a[course][0][1] for a in results.values()])
    n = np.mean([a[course][0][2] for a in results.values()])
    v = [[a[course][0][3] for a in results.values()]]

    return [(m, s, n, v)]


def structure_cor_means(cc, coef):
    # pandas is astounding
    temp = pd.DataFrame.from_dict(cc).transpose()
    correlation_means = pd.DataFrame(temp[0].tolist(), index=temp.index)
    correlation_means.columns = ["m", "sd", "n", "vals"]
    correlation_means = correlation_means.assign(ci=lambda x: coef * x.sd / np.sqrt(x.n))

    return correlation_means.index, correlation_means.m, correlation_means.ci, correlation_means.vals


def computations_with_baselines(df, group, theta, memberships=True, links=False, block_links=False):
    # real values
    cors = compute_cors(df, group, theta)
    comp_cors = compute_correlation_means(cors)

    ret_dict = {"Observed": comp_cors}

    if memberships:
        # permutation of membership values
        it_results = dict()
        for i in range(n_iterations):
            theta_random = theta.copy(deep=True)
            theta_random["index"] = np.random.permutation(theta_random["index"].values)
            rand_memberships = compute_cors(df, group, theta_random)
            it_results[i] = compute_correlation_means(rand_memberships)
        final_dict = dict()
        for course in range(5, 15):
            final_dict[course] = compute_iteration_means(it_results, course)
        ret_dict["Null model"] = final_dict

    if links:
        # permutation of links
        it_results = dict()
        for i in range(n_iterations):
            rand_memberships = compute_cors(df, group, theta, random_links=True)
            it_results[i] = compute_correlation_means(rand_memberships)
        final_dict = dict()
        for course in range(5, 15):
            final_dict[course] = compute_iteration_means(it_results, course)

        ret_dict["Link Permutation Baseline"] = final_dict

    if block_links:
        # permutation of links in block
        it_results = dict()
        for i in range(n_iterations):
            rand_memberships = compute_cors(df, group, theta, block_random_links=True)
            it_results[i] = compute_correlation_means(rand_memberships)
        final_dict = dict()
        for course in range(5, 15):
            final_dict[course] = compute_iteration_means(it_results, course)

        ret_dict["Link Block Permutation Baseline"] = final_dict

    return ret_dict
