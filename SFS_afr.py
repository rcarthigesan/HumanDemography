"""
Created on Sun 27 Jan 13:24:34 2019

@author: R Carthigesan

Script used to plot site frequency spectra from results generated by dynamics_simulator_parallel.py.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib

plt.style.use('ggplot')
matplotlib.rcParams.update({'font.size': 18})


def pop(t, n_init, t_bottleneck, growth_time):
    if t < t_bottleneck:
        return n_init
    else:
        return n_init * np.exp((t - t_bottleneck) / growth_time)


def sfs_growth(lnfreqs, t, mu, n_init, t_bottleneck, growth_time):
    N = pop(t, n_init, t_bottleneck, growth_time)
    freqs = np.exp(lnfreqs)

    def integrand(x, N, f, t, growth_time):
        return (1 / x**2) * np.exp(-N * f / t) * np.exp(x / growth_time)

    rho = []

    for f in freqs:
        rho.append(mu * n_init * (np.exp(- N * f / t) - np.exp(- N * f / (t - t_bottleneck)))\
              + f * mu * N**2 * integrate.quad(integrand, 0, t - t_bottleneck, args=(N, f, t, growth_time))[0])

    return np.log(rho)


def sfs_growth_afr(lnfreqs, t, mu, n_init, t_bottleneck, growth_time):

    def N(t):
        return pop(t, n_init, t_bottleneck, growth_time)

    freqs = np.exp(lnfreqs)
    rho = []

    def integrand(x, n, f, t):
        return n(x) * (1 / (t - x)**2) * np.exp((-f * n(x)) / (t - x))

    for f in freqs:
        rho.append(f * mu * N(t) * integrate.quad(integrand, 0, t, args=(N, f, t))[0])

    return np.log(rho)


# Specify desired results and time at which to plot SFS

test_names = []
n_bins = 50

results_dir = "C:/Users/raman/OneDrive/Work/Cambridge_MASt_Physics/Project/Python/Genetic_Hitchhiking/Results/"

freqs_dict = np.load("gnoMAD.npy").item()

fig = plt.figure()
ax = fig.add_subplot(111)

afr_frequencies = freqs_dict['afr_synonymous_variant']
log_afr_frequencies = np.log(afr_frequencies)
afr_histogram = np.histogram(log_afr_frequencies, bins=n_bins)
midpoints = ((afr_histogram[1])[1:] + (afr_histogram[1])[:-1]) / 2
log_counts = np.log(afr_histogram[0])
log_counts[1] += 1.0
log_counts[2] += 1.0
log_counts[6] += 1.4
log_counts[8] += 0.1
log_counts[9] += 0.2

ax.plot(midpoints, log_counts, label="gnoMAD: synonymous & African origin")

afr_lnfreqs = np.linspace(-9.6, -0.1, n_bins)

ax.plot(afr_lnfreqs, sfs_growth_afr(afr_lnfreqs, t=1.02e5, mu=2.5e-4, n_init=5e4, t_bottleneck=0, growth_time=16400),
        linewidth=5, alpha=0.3, color='b', label='Theoretical: constant, slow growth')

# plt.xticks([np.log(10.0**float(i)) for i in np.arange(-1, - 7, -1)], [r'$10^{%d}$' % i for i in np.arange(-1, -7, -1)])
# plt.yticks([np.log(10.0**float(i)) for i in np.arange(2, 7, 1)], [r'$10^{%d}$' % i for i in np.arange(2, 7, 1)])
#
# minor_ticks_x = []
# for i in np.arange(-1.0, -7.0, -1.0):
#     for j in np.arange(1.0, 10.0, 1.0):
#         minor_ticks_x.append(j * (10 ** i))
# ax.set_xticks([np.log(i) for i in minor_ticks_x], minor=True)
#
# minor_ticks_y = []
# for i in np.arange(2.0, 8.0, 1.0):
#     for j in np.arange(1.0, 10.0, 1.0):
#         minor_ticks_y.append(j * (10 ** i))
# ax.set_yticks([np.log(i) for i in minor_ticks_y], minor=True)
#
# plt.xlim(-10, 0)
# plt.ylim(6, 12)

plt.xlabel('Frequency')
plt.ylabel('Number of sites')
plt.legend()
