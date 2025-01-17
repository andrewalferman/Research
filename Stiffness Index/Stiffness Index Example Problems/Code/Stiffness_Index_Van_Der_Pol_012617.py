#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 12:53:14 2017

@author: alfermaa
"""

import numpy as np
import scipy as sci
import pylab as pyl


def dydx(y, x, eta):
    '''Finds the local vector of the first derivative of the Van der Pol
    equation.'''
    # Unpack the y vector
    y1, y2 = y

    # Create dydx vector (y1', y2')
    f = [y2, eta*y2 - y1 - eta*y2*y1**2.]
    return f


def d2ydx2(y, x, eta):
    '''Finds the local vector of the second derivative of the Van der Pol
    equation.'''
    # Unpack the y vector
    y1, y2 = y

    # Create vector of the second derivative
    y2prime = eta*y2 - y1 - eta*y2*y1**2.
    f = [y2prime, eta*y2prime - y2 - 2*eta*y1*y2 - eta*y2prime*y1**2]
    return f


def jacobian(y, eta):
    '''Find the local Jacobian matrix of the Van der Pol equation.'''
    return [[0., 1.], [-1. - 2*y[0]*y[1]*eta, eta-eta*y[0]**2]]


def weightednorm(matrix, weights):
    """Weighted average norm function as defined in 1985 Shampine.  Takes a
    matrix and 2 weights and returns the maximum value (divided by wi) of the
    sum of each value in each row multiplied by wj."""
    # Unpack the parameters
    wi, wj = weights

    # Initialize a list that will be called later to obtain the maximum value
    ivalues = []

    matrix = np.array(matrix)

    # A few try statements are used to figure out the shape of the matrix
    # Try statements are used because the code would otherwise return an
    # exception if the matrix is one dimensional.  The shape of the matrix is
    # needed to iterate across the rows and columns later.
    try:
        num_rows, num_columns = matrix.shape
        dimensions = 2
    except ValueError:
        dimensions = 1
        try:
            num_rows = 1
            num_columns = matrix.shape[0]
        except IndexError:
            num_rows = matrix.shape[1]
            num_columns = 1
    # Sums up the values across each of the columns and applies the weights,
    # then finds the maximum value (the weighted matrix norm) after the weights
    # have been applied.
    for i in range(num_columns):
        columnsum = 0.
        for j in range(num_rows):
            if dimensions == 2:
                columnsum += np.abs(matrix[j][i]) * wj
            else:
                columnsum += np.abs(matrix[i]) * wj
        ivalues.append(columnsum / wi)
    return np.max(ivalues)


def stiffnessindex(sp, jacobian, derivativevals, normweights):
    '''Function that uses stiffness parameters (sp), the local Jacobian matrix,
    and a vector of the local function values to determine the local stiffness
    index as defined in 1985 Shampine'''
    # Method 1 uses the weighted norm of the Jacobian, Method 2 uses the
    # spectral radius of the Jacobian.
    method = 2

    # Unpack the parameters
    tolerance, order, xi, gamma = sp

    # The second derivative normally will come in one row for this program,
    # however we want to be taking the weighted norm of the second derivative
    # values in one column instead.  The derivative values must then be
    # transposed.  Should try to make this smarter by checking the number of
    # rows/columns before transposing.
    np.asarray(derivativevals).T.tolist()

    if method == 1:
        exponent = 1./(order + 1)
        index = tolerance**exponent *\
            weightednorm(jacobian, normweights) *\
             weightednorm(derivativevals, normweights)**exponent *\
             ((np.abs(xi)**exponent) / np.abs(gamma))
    else:
        exponent = 1./(order + 1)
        index = tolerance**exponent *\
            np.max(np.abs(np.linalg.eigvals(jacobian))) *\
             weightednorm(derivativevals, normweights)**exponent *\
             ((np.abs(xi)**exponent) / np.abs(gamma))
    return index

# Define the range of the computation
xstart = 0
xstop = 810.
xswitch = 807.01
xswitch2 = 807.5
dx1 = 1.0e-1
dx2 = 1.0e-8

# Equation parameters
eta = 1.0e3

# Initial conditions
y1zero = 2
y2zero = 0

# ODE Solver parameters
abserr = 1.0e-10
relerr = 1.0e-8

# Stiffness index parameter values to be sent to the stiffness index function
gamma = 1.
xi = 1.
order = 1
tolerance = 1.
stiffnessparams = tolerance, order, xi, gamma

# Weighted norm parameters to be sent to the weighted norm function
wi = 1.
wj = 1.
normweights = wi, wj

# Create the range of points along x to integrate
xlist1 = np.arange(xstart, xswitch, dx1)
xlist2 = np.arange(xswitch, xswitch2, dx2)
xlist3 = np.arange(xswitch2, xstop+dx1*.5, dx1)
x_listcombo = np.concatenate((xlist1, xlist2, xlist3))

# Pack up the parameters to send to the integrator
y = [y1zero, y2zero]

# Call the integrator
solutioncombo = sci.integrate.odeint(dydx, y, x_listcombo, args=(eta,),
                                atol=abserr, rtol=relerr)

# Find the stiffness index across the range of the solution by using the above
# functions to get the Jacobian matrix and second derivative
indexvaluescombo = []
for i in solutioncombo:
    localjac = jacobian(i, eta)
    secondderiv = d2ydx2(i, 0, eta)
    localstiffness = stiffnessindex(stiffnessparams, localjac,
                                    secondderiv, normweights)
    indexvaluescombo.append(localstiffness)

# Plot the solution.  This loop just sets up some of the parameters that we
# want to modify in all of the plots.
for p in range(1, 3):
    pyl.figure(p, figsize=(6, 4.5), dpi=400)
    pyl.xlabel('x Value')
    pyl.grid(True)
    pyl.hold(True)
#    pyl.xlim(0.005,0.006)

#Set the linewidth to make plotting look nicer
lw = 1

# Set all of the parameters that we want to apply to each plot specifically.
pyl.figure(1)
pyl.ylabel('y1 Value')
pyl.plot(x_listcombo, solutioncombo[:,0], 'b', linewidth=lw)
pyl.title('Solution Component')

pyl.figure(2)
pyl.ylabel('Index Value')
pyl.plot(x_listcombo, indexvaluescombo, 'b', linewidth=lw)
pyl.title('IA-Stiffness Index, Order = {}'.format(order))
pyl.yscale('log')

pyl.show()
