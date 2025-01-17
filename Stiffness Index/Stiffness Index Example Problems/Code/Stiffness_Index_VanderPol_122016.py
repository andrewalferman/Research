#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:54:30 2016

@author: andrewalferman
"""

import numpy as np
import matplotlib.pyplot as plt


def backwardeuler(yold, ynew, eta, dx, tolerance):
    '''A backward (implicit) Euler scheme for the van der Pol equation.'''
    ynext = np.zeros(2)
#    jacobianterm = dx * np.array(jacobiantwo(ynew, eta))
#    ynext = np.dot(np.linalg.inv(np.eye(2) - jacobianterm), yold)
    ynext[1] = (yold[1] - dx*ynew[0]) / (1 + dx*eta*(-1 + ynew[0]**2))
    ynext[0] = yold[0] + dx * ynext[1]
    return ynext


#def newtons_method(yvals, tolerance, eta, x):
#    deviation = 999999.
#    y1new = y1old = yvals[0]
#    y2new = y2old = yvals[1]
#    while deviation > tolerance:
#        y1new = y1new - (y1old + dx*y2new)/ ((y2old - dx*y1new) /\
#                   (1 + dx*eta*(-1 + y1new**2)))
#        print(y1new)
#        y2new = (y2old - dx*y1new) / (1 + dx*eta*(-1 + y1new**2))
#        deviation = abs(y1new - y1old)
#    ynext = [y1new, y2new]
#    print(ynext)
#    return ynext

def newtons_method(yvals, tolerance, eta, dx):
    '''Simple function that uses Newton's method to find the next value in the
    implicit scheme.  Configured for the van der Pol equation specifically.'''
    deviation = 99999.
    yold = yvals[:]
    ynew = yvals[:]
    iterations = 0
    while deviation > tolerance:
        ynext = backwardeuler(yvals, ynew, eta, dx, tolerance)
        print('YNEXT:')
        print(ynext)
        print('YNEW1:')
        print(ynew)
        jacobian = np.array(jacobiantwo(ynext, eta))
#        print('JACOBIAN:')
#        print(jacobian)
#        yprime = np.dot(jacobian, ynext)
#        print('SLOPES:')
#        print(yprime)
#        print(np.linalg.inv(yprime))
#        print((ynext[0] - yvals[0])/dx)
#        ynew[0] = ynew[0] - ynext[0] / ((ynext[0] - yvals[0]) / dx)
#        ynew[1] = (yvals[1] - dx*ynew[0]) / (1 + eta*dx*(-1 + ynew[0]**2))
#        print('JACOBIAN INVERSE')
#        print(np.linalg.inv(jacobian))
        ynew = ynew - np.dot(ynew, np.linalg.inv(jacobian))
        print('YNEW2:')
        print(ynew)
#        print('YOLD:')
#        print(yold)
#        print(ynew[0])
        deviation = np.abs(ynew[0] - yold[0])
        print('DEVIATION:')
        print(deviation)
        yold = ynew
        iterations += 1
    print('ITERATIONS:')
    print(iterations)
    return ynew


#def functiontwo(x, eta):
#    '''Function to evaluate the semi-analytical solution to the Van der Pol
#    equation.   Equation 6.3 of 1985 Shampine.'''
#    y, y1p = np.zeros(2), np.zeros(2)
#    y[0] = x*y[1] + 2
#    y[1] = x*y[1]/eta - x*y[0] - x*(y[0]**2)*y[1]/eta
##    y1p[0] = y[1]
##    y1p[1] = y[1]*eta**-1 - y[0] - y[0]*y[1]*eta**-1
#    return y, y1p


def jacobiantwo(y, eta):
    '''Find the local Jacobian matrix of the Van der Pol equation.'''
    return [[0, 1], [-1 - y[0]*y[1]*eta, eta]]


def factorial(number):
    '''Simple function that returns the factorial of a given integer.  Prints
    an error message and returns None if the value given is not a positive
    integer.'''
    if isinstance(number, int) and number > 0:
        result = 1
        for i in range(number):
            result *= number
            number -= 1
        return result
    elif isinstance(number, int) and number == 0:
        return 1
    else:
        raise ValueError('Number must be a positive integer.')
        return None


def weightednorm(matrix, weights):
    """Weighted average norm function as defined in 1985 Shampine.  Takes a
    matrix and 2 weights and returns the maximum value (divided by wi) of the
    sum of each value in each row multiplied by wj."""
    wi, wj = weights
    ivalues = []
    matrix = np.array(matrix)
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
    tolerance, order, xi, gamma = sp
    if method == 1:
        index = tolerance**(1./(order + 1.)) *\
            weightednorm(jacobian, normweights) *\
             weightednorm(derivativevals, normweights)**\
                 (-1. / (order + 1.)) *\
             ((np.abs(xi)**(-1./(order + 1.))) / np.abs(gamma))
    else:
        index = tolerance**(1./(order + 1.)) *\
            np.max(np.abs(np.linalg.eigvals(jacobian))) *\
             weightednorm(derivativevals, normweights)**\
                 (-1. / (order + 1.)) *\
             ((np.abs(xi)**(-1./(order + 1.))) / np.abs(gamma))
    return index

# Stepsize and other important variables that affect accuracy
dx = 1.
newtontolerance = 1.e-6

# Stiffness index parameter values (stiffnessparams)
#gamma = 1.
#xi = 1.
#order = 1
#tolerance = 1.
#stiffnessparams = tolerance, order, xi, gamma

# Weighted norm parameters (normweights)
#wi = 1.
#wj = 1.
#normweights = wi, wj

# List of all the eta values to plot for the second function
eta_list = [1.e3]
x_list = np.arange(0, 30 + .5*dx, dx)

# Iterate across the range of 0<x<3000 for each of the eta values for the
# second function
#indexvalues = []
funcvals = []
for eta in eta_list:
#    indexvalrow = []
    y = [2., 0.]
    for x in x_list:
        funcvals.append(y[0])
        yprev = y
        print(y)
        y = newtons_method(y, newtontolerance, eta, dx)
#        derivativevals, localvals = functiontwo(x, eta, order)
#        jacobian = jacobiantwo(x, eta, order)
#        indexvalrow.append(stiffnessindex(stiffnessparams, jacobian,
#                                          derivativevals, normweights))
#    indexvalues.append(indexvalrow)

# Plot all of the values calculated
plt.figure(0)
plt.scatter(x_list, funcvals, label='Eta value: {}'.format(eta_list[0]))
#    plt.figure(1)
#    plt.plot(x2_list, indexvalues[i], label='Eta value: {}'.format(eta_list[i]))
for i in range(1):
    plt.figure(i)
    plt.legend(bbox_to_anchor=(1, 1), loc=2)
    plt.xlabel('X range')
    plt.grid(b=True, which='both')
plt.figure(0)
plt.title('Numerical Solution')
plt.ylabel('Y1 value')
#plt.figure(1)
#plt.title('IA-Stiffness Index')
#plt.ylabel('Stiffness Index Value')
#plt.yscale('log')
plt.show()
