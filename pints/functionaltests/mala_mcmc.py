#!/usr/bin/env python3
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#

from __future__ import division

import pints

from ._problems import (RunMcmcMethodOnTwoDimGaussian,
                        RunMcmcMethodOnBanana,
                        RunMcmcMethodOnHighDimensionalGaussian,
                        RunMcmcMethodOnCorrelatedGaussian,
                        RunMcmcMethodOnAnnulus,
                        RunMcmcMethodOnMultimodalGaussian,
                        RunMcmcMethodOnCone)


def test_mala_mcmc_on_two_dim_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 1000
    problem = RunMcmcMethodOnTwoDimGaussian(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=200,
        method_hyper_parameters=[[1.0, 1.0]]
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_banana(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnBanana(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[0.8] * 2]
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_high_dim_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnHighDimensionalGaussian(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[1.2] * 20]
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_correlated_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnCorrelatedGaussian(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[1.0] * 6]
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_annulus(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnAnnulus(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[1.2] * 2]
    )

    return {
        'distance': problem.estimate_distance(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_multimodal_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnMultimodalGaussian(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[2.0] * 2]
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_mala_mcmc_on_cone(n_iterations=None):
    if n_iterations is None:
        n_iterations = 2000
    problem = RunMcmcMethodOnCone(
        method=pints.MALAMCMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=500,
        method_hyper_parameters=[[1.0, 1.0]]
    )

    return {
        'distance': problem.estimate_distance(),
        'mean-ess': problem.estimate_mean_ess()
    }
