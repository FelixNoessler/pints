#!/usr/bin/env python3
#
# Change point tests for HamiltonianMCMC
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import pints
import pints.cptests as cpt


def two_dim_gaussian(n_iterations=1000, n_warmup=200):
    """
    Tests :class:`pints.HamiltonianMCMC`
    on a two-dimensional Gaussian distribution with true solution
    ``[0, 0]`` and returns a dictionary with entries ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.cptests.RunMcmcMethodOnTwoDimGaussian`.
    """
    problem = cpt.RunMcmcMethodOnTwoDimGaussian(
        method=_method,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=n_warmup,
        method_hyper_parameters=[20, 1]
    )
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def high_dim_gaussian(n_iterations=4000, n_warmup=1000):
    """
     Tests :class:`pints.HamiltonianMCMC`
    on a 20-dimensional Gaussian distribution centered at the origin, and
    returns a dictionary with entries ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.cptests.RunMcmcMethodOnHighDimensionalGaussian`.
    """
    problem = cpt.RunMcmcMethodOnHighDimensionalGaussian(
        method=_method,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=n_warmup,
        method_hyper_parameters=[20, 1]
    )
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def annulus(n_iterations=10000, n_warmup=1000):
    """
    Tests :class:`pints.HamiltonianMCMC`
    on a two-dimensional annulus distribution with radius 10, and returns a
    dictionary with entries ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.cptests.RunMcmcMethodOnAnnulus`.
    """
    problem = cpt.RunMcmcMethodOnAnnulus(
        method=_method,
        n_chains=10,
        n_iterations=n_iterations,
        n_warmup=n_warmup)
    return {
        'kld': problem.estimate_distance(),
        'mean-ess': problem.estimate_mean_ess()
    }


_method = pints.HamiltonianMCMC
_change_point_tests = [
    two_dim_gaussian,
    high_dim_gaussian,
    annulus,
]
