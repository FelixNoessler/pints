#
# Markov jump model.
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import numpy as np
from scipy.interpolate import interp1d
import pints
import random

from .. import ToyModel


class MarkovJumpModel(pints.ForwardModel, ToyModel):
    r"""
    A general purpose Markov Jump model used for any systems of reactions
    that proceed through jumps. We simulate a population of N different species
    reacting through M different reaction equations.

    Simulations are performed using Gillespie's algorithm [1]_, [2]_:

    1. Sample values :math:`r_0`, :math:`r_1`, from a uniform distribution

    .. math::
        r_0, r_1 \sim U(0,1)

    2. Calculate the time :math:`\tau` until the next single reaction as

    .. math::
        \tau = \frac{-\ln(r)}{a_0}

    where a_0 is the sum of the propensities at the current time.

    3. Decide which reaction, i, takes place using r_1 * a_0 and iterating

    through propensities. Since r_1 is a a value between 0 and 1 and a_0 is

    the sum of all propensities, we can find k for which

    s_k / a_0 <= r_2 < s_(k+1) / a_0 where s_j is the sum of the first j

    propensities at time t. We then choose i as the reaction corresponding

    to propensity k.

    4. Update the state :math:`x` at time :math:`t + \tau` as:

    .. math::
        x(t + \tau) = x(t) + V[i]

    4. Return to step (1) until no reaction can take place or the process

    has gone past the maximum time.

    Extends :class:`pints.ForwardModel`, :class:`pints.toy.ToyModel`.

    Parameters
    ----------
    x_0
        An N-vector specifying the initial population of each
        of the N species.
    V
        An NxM matrix consisting of stochiometric vectors v_i specifying
        the changes to the state, x,  from reaction i taking place.
    propensities
        A function from the current state, x, and reaction rates, k,
        to a vector of the rates of each reaction taking place.

    References
    ----------
    .. [1] A Practical Guide to Stochastic Simulations of Reaction Diffusion
           Processes. Erban, Chapman, Maini (2007).
           arXiv:0704.1908v2 [q-bio.SC]
           https://arxiv.org/abs/0704.1908
    .. [2] A general method for numerically simulating the stochastic time
           evolution of coupled chemical reactions. Gillespie (1976).
           Journal of Computational Physics
           https://doi.org/10.1016/0021-9991(76)90041-3
    """
    def __init__(self, x0, V, propensities):
        super(MarkovJumpModel, self).__init__()
        self._x0 = np.asarray(x0)
        self._V = V
        self._propensities = propensities
        if any(self._x0 < 0):
            raise ValueError('Initial molecule count cannot be negative.')

    def n_parameters(self):
        """ See :meth:`pints.ForwardModel.n_parameters()`. """
        return len(self._V)

    def simulate_raw(self, rates, max_time):
        """
        Returns raw times, mol counts when reactions occur
        """
        if len(rates) != self.n_parameters():
            raise ValueError('This model should have only ',
                             str(self.n_parameters()),
                             ' parameter(s).')
        # Setting the current propensities and summing them up
        current_propensities = self._propensities(self._x0, rates)
        prop_sum = sum(current_propensities)

        # Initial time and count
        t = 0
        x = np.array(self._x0)

        # Run Gillespie SSA, calculating time until next
        # reaction, deciding which reaction, and applying it
        mol_count = [np.array(x)]
        time = [t]
        while prop_sum > 0 and t <= max_time:
            r_1, r_2 = random.random(), random.random()
            t += -np.log(r_1) / (prop_sum)
            s = 0
            r = 0
            while s <= r_2 * prop_sum:
                s += current_propensities[r]
                r += 1
            r -= 1
            x = np.add(x, self._V[r])

            current_propensities = self._propensities(x, rates)
            prop_sum = sum(current_propensities)

            time.append(t)
            mol_count.append(np.array(x))
        return time, mol_count

    def interpolate_mol_counts(self, time, mol_count, output_times):
        """
        Takes raw times and inputs and mol counts and outputs interpolated
        values at output_times
        """
        # Interpolate as step function, decreasing mol_count by 1 at each
        # reaction time point
        interp_func = interp1d(time, mol_count, kind='previous', axis=0,
                               fill_value="extrapolate", bounds_error=False)

        # Compute molecule count values at given time points using f1
        # at any time beyond the last reaction, molecule count = 0
        values = interp_func(output_times)
        return values

    def simulate(self, parameters, times):
        """ See :meth:`pints.ForwardModel.simulate()`. """
        times = np.asarray(times)
        if np.any(times < 0):
            raise ValueError('Negative times are not allowed.')
        # Run Gillespie
        time, mol_count = self.simulate_raw(parameters, max(times))
        # Interpolate
        if len(time) < 2:
            time = np.append(time, time[0])
            mol_count = np.append(mol_count, mol_count[0])
        values = self.interpolate_mol_counts(np.asarray(time),
                                             np.asarray(mol_count), times)
        return values