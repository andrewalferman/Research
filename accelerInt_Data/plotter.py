#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:34 2017

@author: andrewalferman
"""

import numpy as np
import csv as csv
import matplotlib.pyplot as plt


def readsolver(solver):
    """Take the input file and return the QoI."""
    ratios, indicators, CEMAvals, inttimes = [], [], [], []
    with open('speciesdata-' + solver + '.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ratios.append(float(row[1]))
            indicators.append(float(row[2]))
            CEMAvals.append(float(row[3]))
            inttimes.append(float(row[4]))
    ratios = np.array(ratios)
    indicators = np.array(indicators)
    CEMAvals = np.array(CEMAvals)
    inttimes = np.array(inttimes)
    return [ratios, indicators, CEMAvals, inttimes]


solvers = ['cvodes', 'radau2a', 'exprb43', 'radau2a']
data = {}
for key in solvers:
    data[key] = readsolver(key)

# Clear all previous figures and close them all
for i in range(15):
    plt.figure(i)
    plt.clf()
plt.close('all')

print('Plotting...')

ymax = 0
xmax = np.array([0, 0, 0])
xmin = np.array([0, 0, 0])
for key in solvers:
    ymax = max(ymax, max(data[key][3]))
    for i in range(3):
        plt.figure(i)
        plt.ylabel('Integration Times')
        plt.grid(b=True, which='both')
        plt.scatter(data[key][i], data[key][3], 1.0, lw=0, label=key)
        xmax[i] = max(xmax[i], max(data[key][i]))
        xmin[i] = min(xmin[i], min(data[key][i]))

ymax = 0.00005

plt.figure(0)
plt.title('Ratios vs. Int Times')
plt.xlabel('Ratio Values')
plt.xscale('log')
plt.xlim(0, xmax[0])
plt.ylim(0, ymax)

plt.figure(1)
plt.title('Indicators vs. Int Times')
plt.xlabel('Indicator Values')
plt.xlim(xmin[1], xmax[1])
plt.ylim(0, ymax)

plt.figure(2)
plt.title('CEM vs. Int Times')
plt.xlabel('CEM Values')
plt.xlim(max(1e-6, xmin[2]), xmax[2])
plt.ylim(0, ymax)

for i in range(3):
    plt.figure(i)
    plt.legend(fontsize='small', markerscale=5)
    plt.tight_layout()

plt.show()
