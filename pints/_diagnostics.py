#
# Functions to calculate various MCMC diagnostics
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import numpy as np


def autocorrelation(x):
    """
    Calculate autocorrelation for a vector x using a spectrum density
    calculation.
    """
    x = (x - np.mean(x)) / (np.std(x) * np.sqrt(len(x)))
    result = np.correlate(x, x, mode='full')
    return result[int(result.size / 2):]


def autocorrelate_negative(autocorrelation):
    """
    Finds last positive autocorrelation, T.
    """
    T = 1
    for a in autocorrelation:
        if a < 0:
            return T - 1
        T += 1
    return T


def ess_single_param(x):
    """
    Calculates ESS for a single parameter.
    """
    rho = autocorrelation(x)
    T = autocorrelate_negative(rho)
    n = len(x)
    ess = n / (1 + 2 * np.sum(rho[0:T]))
    return ess


def effective_sample_size(samples):
    """
    Calculates ESS for a matrix of samples.
    """
    try:
        n_samples, n_params = samples.shape
    except (ValueError, IndexError):
        raise ValueError('Samples must be given as a 2d array.')
    if n_samples < 2:
        raise ValueError('At least two samples must be given.')

    return [ess_single_param(samples[:, i]) for i in range(0, n_params)]


def within(samples):
    """
    Calculates within-chain variance.
    """
    mu = list(map(lambda x: np.var(x, ddof=1), samples))
    W = np.mean(mu)
    return W


def between(samples):
    """
    Calculates between-chain variance.
    """
    mu = list(map(lambda x: np.mean(x), samples))
    mu_overall = np.mean(mu)
    m = len(samples)
    t = len(samples[0])
    return (t / (m - 1.0)) * np.sum((mu - mu_overall) ** 2)


def reorder(param_number, chains):
    """
    Reorders chains for a given parameter into a more useful format for
    calculating rhat.
    """
    # split chains in two
    a_len = int(chains.shape[1] / 2)
    chains_first = [chain[:a_len, :] for chain in chains]
    chains_second = [chain[a_len:, :] for chain in chains]
    chains = chains_first + chains_second
    num_chains = len(chains)
    samples = [chains[i][:, param_number] for i in range(0, num_chains)]
    return samples


def reorder_all_params(chains):
    """
    Reorders chains for all parameters into a more useful format for
    calculating rhat.
    """
    num_params = chains[0].shape[1]
    samples_all = [reorder(i, chains) for i in range(0, num_params)]
    return samples_all


def rhat(samples):
    r"""
    Calculates :math:`\hat{R} = sqrt(((n - 1)/n * W + (1/n) * B)/W)`` as per
    [1]_ for a single parameter. It does this after splitting each chain into
    two.
    """
    W = within(samples)
    B = between(samples)
    t = len(samples[0])
    return np.sqrt((W + (1.0 / t) * (B - W)) / W)


def rhat_all_params(chains):
    r"""
    Calculates :math:`\hat{R} = sqrt(((n - 1)/n * W + (1/n) * B)/W)`` as per
    [1]_ for all parameters. It does this after splitting each chain into two.

    References
    ----------
    ..  [1] "Bayesian data analysis", 3rd edition, Gelman et al., 2014.
    """
    samples_all = reorder_all_params(chains)
    rhat_all = list(map(lambda x: rhat(x), samples_all))
    return rhat_all
