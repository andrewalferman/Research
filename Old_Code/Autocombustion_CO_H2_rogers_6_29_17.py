#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:54:13 2017

@author: andrewalferman
"""

import matplotlib
matplotlib.use('Agg')
import os as os
import numpy as np
import pyjacob as pyjacob
import pylab as pyl
# import scipy as sci
import datetime
import time as timer

# from scipy.integrate import odeint
from scipy.integrate import ode

pyl.ioff()


def firstderiv(time, state, press):
    """Force the integrator to use the right arguments."""
    # Need to make sure that N2 is at the end of the state array
    dy = np.zeros_like(state)
    pyjacob.py_dydt(time, press, state, dy)
    return dy


def jacobval(time, state, press):
    """Force the integrator to use the right arguments."""
    # Need to get rid of N2 because PyJac doesn't compute it.
    # new = state[:-1]
    # print('Jacobian function called.')
    a = len(state)
    jacobian = np.zeros(a**2)
    # Obtain the jacobian from pyJac
    pyjacob.py_eval_jacobian(time, press, state, jacobian)
    jacobian = np.reshape(jacobian, (a, a))
    # Re-add the zeros back in
    # jacobian = np.insert(jacobian, a, np.zeros(a), axis=1)
    # jacobian = np.vstack((jacobian, np.zeros(a+1)))
    return jacobian


def jacvdp(x, y, eta):
    """Find the local Jacobian matrix of the Van der Pol equation."""
    return np.array([[0., 1.], [-1. - 2*y[0]*y[1]*eta, eta-eta*y[0]**2]])


def dydx(x, y, eta):
    """Find the local vector of the first derivative of the Van der Pol eqn."""
    # Unpack the y vector
    y1 = y[0]
    y2 = y[1]

    # Create dydx vector (y1', y2')
    f = np.array([y2, eta*y2 - y1 - eta*y2*y1**2.])
    # print(f)
    return f


def d2ydx2(x, y, eta):
    """Find the local vector of the 2nd derivative of the Van der Pol eqn."""
    # Unpack the y vector
    y1 = y[0]
    y2 = y[1]

    # Create vector of the second derivative
    y2prime = eta*y2 - y1 - eta*y2*y1**2.
    f = np.array([y2prime, eta*y2prime - y2 - 2*eta*y1*y2 - eta*y2prime*y1**2])
    return f


def derivcd4(vals, dx):
    """Take the derivative of a series using 4th order central differencing.

    Given a list of values at equally spaced points, returns the first
    derivative using the fourth order central difference formula, or forward/
    backward differencing at the boundaries.
    """
    deriv = []
    for i in range(2):
        deriv.append((-3 * vals[i] + 4 * vals[i + 1] - vals[i + 2]) / (2 * dx))
    for i in range(2, len(vals) - 2):
        deriv.append(((-1 * vals[i + 2]) + (8 * vals[i + 1]) -
                     (8 * vals[i - 1]) + vals[i - 2]) /
                     (12 * dx)
                     )
    for i in range((len(vals) - 2), len(vals)):
        deriv.append((3 * vals[i] - 4 * vals[i - 1] + vals[i - 2]) / 2 * dx)
    return deriv


def weightednorm(matrix, weights):
    """Weighted average norm function as defined in 1985 Shampine.

    Takes a matrix and 2 weights and returns the maximum value (divided by
    wi) of the sum of each value in each row multiplied by wj.  Needs to be
    passed either a matrix of m x n dimensions where m,n > 1, or a column
    vector.
    """
    # Unpack the parameters
    wi, wj = weights

    # Initialize a list that will be called later to obtain the maximum value
    colsums = np.zeros(len(matrix))

    # Try loop used because numpy didn't seem to like 1D arrays for the
    # weighted norm
    try:
        for i in range(len(matrix)):
            colsums += wj * np.abs(matrix[i])
        return np.max(colsums) / wi
    except TypeError:
        matrixcol = wj * np.abs(matrix)
        return np.sum(matrixcol) / wi


def stiffnessindex(xlist, solution, dfun, jfun, *args, **kwargs):
    """Determine the stiffness index across a solution vector.

    Function that uses stiffness parameters, the local Jacobian matrix,
    and a vector of the local function values to determine the local stiffness
    index as defined in 1985 Shampine.

    Future optimizations:
        1.  Use a different integrator that saves the values of the derivative
        as it goes so that we don't need to calculate each derivative twice.
        Same goes with the Jacobian, it would be much faster to evaluate
        it on the fly.
        2.  Implement this index in the integrator itself so that it makes all
        of the values as the integration goes.  This would eliminate the need
        to save the dydx list beyond a few variables that would be needed to
        compute the higher level derivatives.
    """
    SIparams = {'method': 2,
                'gamma': 1,
                'xi': 1,
                'order': 1,
                'tolerance': 1,
                'wi': 1,
                'wj': 1
                }

    for key, value in kwargs.items():
        SIparams[key] = value

    funcparams = []
    for arg in args:
        funcparams.append(arg)

    # Method 2 uses the weighted norm of the Jacobian, Method 1 uses the
    # spectral radius of the Jacobian.
    method = SIparams['method']
    # Stiffness index parameter values
    gamma = SIparams['gamma']
    xi = SIparams['xi']
    order = SIparams['order']
    tolerance = SIparams['tolerance']
    # Weighted norm parameters
    wi = SIparams['wi']
    wj = SIparams['wj']

    normweights = wi, wj

    # Obtain the derivative values for the derivative of order p
    dx = xlist[1] - xlist[0]
    dydxlist = []
    for i in range(len(solution)):
        dydxlist.append(dfun(xlist[i], solution[i, :], funcparams[0]))
    # Raise the derivative to the order we need it
    for i in range(order):
        dydxlist = derivcd4(dydxlist, dx)
    dydxlist = np.array(dydxlist)

    # Create a list to return for all the index values in a function
    indexlist = []

    # Figure out some of the values that will be multiplied many times, so that
    # each computation only needs to happen once.
    exponent = 1. / (order + 1)
    xiterm = ((np.abs(xi)**(-1 * exponent)) / np.abs(gamma))
    toleranceterm = tolerance**exponent

    # Actual computation of the stiffness index for the method specified.
    for i in range(len(solution)):
        jacobian = jfun(xlist[i], solution[i, :], funcparams[0])
        if method == 1:
            eigenvalues = np.linalg.eigvals(jacobian)
            index = toleranceterm *\
                np.max(np.abs(eigenvalues)) *\
                weightednorm(dydxlist[i, :], normweights)**(-1 * exponent) *\
                xiterm
        else:
            index = toleranceterm *\
                weightednorm(jacobian, normweights) *\
                weightednorm(dydxlist[i, :], normweights)**(-1 * exponent) *\
                xiterm
        indexlist.append(index)
    indexlist = np.array(indexlist)
    print('Last Jacobian:')
    for i in jacobian:
        print(i)
    return indexlist  # , dydxlist


def stiffnessindicator(xlist, solution, jfun, *args):
    """
    Find the stiffness indicator across a solution.

    Given the set of values of the solution, find the stiffness indicator as
    defined by Soderlind 2013.
    """
    funcparams = []
    for arg in args:
        funcparams.append(arg)

    indicatorvals = []
    for i in range(len(solution)):
        jacobian = jfun(xlist[i], solution[i], funcparams[0])
        Hermitian = 0.5 * (jacobian + np.transpose(jacobian))
        eigvals = np.linalg.eigvals(Hermitian)
        indicatorvals.append(0.5 * (min(eigvals) + max(eigvals)))
    return indicatorvals


def reftimescale(indicatorvals, Tlen):
    """
    Find the reference timescale for the stiffness indicator.

    Given the stiffness indicator values as defined by Soderlind 2013, finds
    the reference time scale.
    """
    timescales = []
    for i in range(len(indicatorvals)):
        if indicatorvals[i] >= 0:
            timescales.append(Tlen)
        else:
            timescales.append(min(Tlen, -1/indicatorvals[i]))
    timescales = np.array(timescales)
    return timescales


def loadpasrdata():
    """Load the initial conditions from the PaSR files."""
    pasrarrays = []
    print('Loading data...')
    for i in range(9):
        filepath = os.path.join(os.getcwd(),
                                'pasr_out_h2-co_' +
                                str(i) +
                                '.npy')
        filearray = np.load(filepath)
        pasrarrays.append(filearray)
    return np.concatenate(pasrarrays, 1)


def rearrangepasr(Y):
    "Rearrange the PaSR data so it works with pyJac"
    press_pos = 2
    temp_pos = 1
    arraylen = len(Y)

    Y_press = Y[press_pos]
    Y_temp = Y[temp_pos]
    Y_species = Y[3:arraylen]
    Ys = np.hstack((Y_temp, Y_species))

    # Put N2 to the last value of the mass species
    N2_pos = 9
    newarlen = len(Ys)
    Y_N2 = Ys[N2_pos]
    # Y_x = Ys[newarlen - 1]
    for i in range(N2_pos, newarlen - 1):
        Ys[i] = Ys[i + 1]
    Ys[newarlen - 1] = Y_N2
    if useN2:
        initcond = Ys
    else:
        initcond = Ys[:-1]
    return initcond, Y_press


# Finding the current time to time how long the simulation takes
starttime = datetime.datetime.now()
print('Start time: {}'.format(starttime))

"""
-------------------------------------------------------------------------------
All of the values that need to be adjusted should be in this section.
"""
# Specify how you want to save the figures/data
savedata = 0
savefigures = 1
figformat = 'png'

# Possible options will be 'VDP', 'Autoignition', or 'Oregonator'
equation = 'Autoignition'

# Possible options will be 'Stiffness_Index', 'Stiffness_Indicator'
method = 'Stiffness_Indicator'

# Make this true if you want to obtain the reference timescale of the stiffness
# indicator.
findtimescale = False

# Make this true if you want to test all of the values across the PaSR.
# Otherwise, this will run a single autoignition at particle 92, timestep 4.
PaSR = False

# Define the range of the computation
dt = 1.e-2
tstart = 0.
tstop = 400.
tlist = np.arange(tstart, tstop + 0.5 * dt, dt)

# ODE Solver parameters
abserr = 1.0e-17
relerr = 1.0e-15

# Keep this at false, something isn't working with using the jacobian yet.
usejac = False

# Decide if you want to give pyJac N2 or not
useN2 = False

# Used if you want to check that the PaSR data is being properly conditioned
displayconditions = False

# Display the solution shape for plotting/debugging
displaysolshapes = False

# To be implemented later.
makesecondderivplots = False
makerainbowplot = False
"""
-------------------------------------------------------------------------------
"""

if equation == 'VDP':
    # Makes no sense to have PaSR for this, so it won't be allowed.
    PaSR = False
    RHSfunction = dydx
    EQjac = jacvdp
    EQ2deriv = d2ydx2
elif equation == 'Autoignition':
    RHSfunction = firstderiv
    EQjac = jacobval

if equation == 'Autoignition':
    # Load the initial conditions from the PaSR files
    pasr = loadpasrdata()

    numparticles = len(pasr[0, :, 0])
    numtsteps = len(pasr[:, 0, 0])
elif equation == 'VDP':
    initcond = [2, 0]
    RHSparam = 200.

# Cheated a little here and entered the number of variables to code faster
numparams = 15
# pasrstiffnesses = np.zeros((numtsteps, numparticles))
# pasrstiffnesses2 = np.zeros((numtsteps, numparticles, numparams))

# Create vectors for that time how long it takes to compute stiffness index and
# the solution itself
solutiontimes, stiffcomptimes, stiffvals = [], [], []

# expeigs = np.zeros((numtsteps, numparticles))

# Loop through the PaSR file for initial conditions
if PaSR:
    print('Code progress:')
    particlelist = range(numparticles)
    timelist = range(numtsteps)
else:
    particlelist = [92]
    timelist = [4]

for particle in particlelist:
    if PaSR:
        print(particle)
    for tstep in timelist:
        if equation == 'Autoignition':
            # Set up the initial conditions for autoignition
            Y = pasr[tstep, particle, :].copy()
            initcond, RHSparam = rearrangepasr(Y)
            if displayconditions:
                print('Initial Condition:')
                for i in Y:
                    print(i)
                print('Modified condition:')
                for i in initcond:
                    print(i)

        print('Integrating...')
        solution = []
        # Specify the integrator
        if usejac:
            intj = EQjac
        else:
            intj = None

        solver = ode(RHSfunction,
                     jac=intj
                     ).set_integrator('vode',
                                      method='bdf',
                                      nsteps=99999999,
                                      atol=abserr,
                                      rtol=relerr,
                                      with_jacobian=usejac,
                                      # first_step=dt,
                                      # min_step=dt,
                                      # max_step=dt
                                      )

        # Set initial conditions
        solver.set_initial_value(initcond, tstart)
        solver.set_f_params(RHSparam)
        solver.set_jac_params(RHSparam)

        # Integrate the ODE across all steps
        while solver.successful() and solver.t <= tstop:
            time0 = timer.time()
            solver.integrate(solver.t + dt)
            time1 = timer.time()
            # print('-----')
            # print('Condition at t = {}'.format(solver.t))
            # for i in solver.y:
            #     print(i)
            solution.append(solver.y)
            solutiontimes.append(time1 - time0)

        if displayconditions:
            print('Final time:')
            print(solver.t)
            print('Last solution value:')
            for i in solver.y:
                print(i)

            lastjac = jacobval(0.2, solver.y, RHSparam)

            print('Last Jacobian value:')
            for i in lastjac:
                print(i)

        # Convert the solution to an array for ease of use.  Maybe just using
        # numpy function to begin with would be faster?
        solution = np.array(solution)
        primaryvals = np.array(solution[:, 0])
        # Find the stiffness index across the range of the solution and time it

        # indexvalues, derivatives = stiffnessindex(stiffnessparams,
        #                                           normweights,
        # print(np.shape(tlist2))
        # print(dt*100.)
        # print(np.shape(solution))
        if method == 'Stiffness_Indicator':
            print('Finding Stiffness Indicator...')
            time2 = timer.time()
            stiffvalues = stiffnessindicator(tlist,
                                             solution,
                                             EQjac,
                                             RHSparam
                                             )
            time3 = timer.time()
            if findtimescale:
                print('Finding reference timescales...')
                timescales = reftimescale(stiffvalues, tstop - tstart)
            stiffcomptimes.append(time3 - time2)
        elif method == 'Stiffness_Index':
            print('Finding Stiffness Index...')
            time2 = timer.time()
            stiffvalues = stiffnessindex(tlist,
                                         solution,
                                         RHSfunction,
                                         EQjac,
                                         RHSparam
                                         )
            time3 = timer.time()
            stiffcomptimes.append(time3 - time2)

# CODE GRAVEYARD!!!
# "Where old code goes to die..."
# This statement intended to cut back on the amount of data processed
# derivatives = derivatives[2]

# stiffvals.append(indexvalues[2])

# Commented old code for the maximum eigenvalue or CEMA analysis
# expeigs[tstep,particle] = np.log10(maxeig)
# Commented old code for just figuring out the PaSR stiffness values
# pasrstiffnesses[tstep, particle] = np.log10(indexvalues[2])
# pasrstiffnesses[tstep,particle,:] = np.hstack((solution[2],
#                                               indexvalues[2]))
# This variable includes the values of the derivatives
# pasrstiffnesses2[tstep, particle, :] = np.hstack(
#    (derivatives, indexvalues[2]))

speciesnames = ['H', 'H$_2$', 'O', 'OH', 'H$_2$O', 'O$_2$', 'HO$_2$',
                'H$_2$O$_2$', 'Ar', 'He', 'CO', 'CO$_2$', 'N$_2$']

# Plot the results

# Clear all previous figures and close them all
for i in range(15):
    pyl.figure(i)
    pyl.clf()
pyl.close('all')

# Something is causing a bug in the tlist and this is intended to fix it
if len(tlist) == len(primaryvals) + 1:
    tlist = tlist[1:]

if displaysolshapes:
    print('Solution[:, 0] shape:')
    print(np.shape(solution[:, 0]))
    print('tlist shape:')
    print(np.shape(tlist))
    print('primaryvals shape:')
    print(np.shape(primaryvals))
    print('solutiontimes shape:')
    print(np.shape(solutiontimes))
    print('stiffvalues shape:')
    print(np.shape(stiffvalues))

plotnum = 0
if PaSR:
    # Ratios of the stiffness computation times to integration times
    ratios = []
    for i in range(len(solutiontimes)):
        ratios.append(stiffcomptimes[i] / solutiontimes[i])

    # Average stiffness computation and solution times
    datanum = len(solutiontimes)
    solavg = 0.0
    stiffavg = 0.0
    for i in range(len(solutiontimes)):
        solavg += solutiontimes[i]
        stiffavg += stiffcomptimes[i]
    solavg = 1000. * (solavg / datanum)
    stiffavg = 1000. * (stiffavg / datanum)
    print("Average integration time (ms): {:.7f}".format(solavg))
    print("Average SI computation time (ms): {:.7f}".format(stiffavg))
    print("Maximum integration time (ms): {:.7f}".format(
        max(solutiontimes) * 1000.))
    print("Maximum SI computation time (ms): {:.7f}".format(max(stiffcomptimes)
                                                            * 1000.))

    # Plot of integration times vs. computation number
    pyl.figure(0)
    pyl.xlim(0, datanum)
    pyl.ylim(0, max(solutiontimes))
    pyl.xlabel('Computation Number')
    pyl.ylabel('Integration Time')
    pyl.scatter(range(datanum), solutiontimes, 0.1)
    if savefigures == 1:
        pyl.savefig('Integration_Times_6_24.' + figformat)
    plotnum += 1

    # Plot of stiffness computation times vs. computation number
    pyl.figure(plotnum)
    pyl.xlim(0, datanum)
    pyl.ylim(0, max(stiffcomptimes))
    pyl.xlabel('Computation Number')
    pyl.ylabel('Stiffness Index Computation Time')
    pyl.scatter(range(datanum), stiffcomptimes, 0.1)
    if savefigures == 1:
        pyl.savefig('Stiff_Comp_Times_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # Plot of ratio of stiffness computation times vs. integration times
    pyl.figure(plotnum)
    pyl.xlim(0, datanum)
    pyl.ylim(0, max(ratios))
    pyl.xlabel('Particle Number')
    pyl.ylabel('Ratio')
    pyl.scatter(range(datanum), ratios, 0.1)
    if savefigures == 1:
        pyl.savefig('Stiff_Comp_Ratios_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # Plot of stiffness computation times vs. stiffness index
    pyl.figure(plotnum)
    pyl.ylabel('Stiffness Index ')
    pyl.xlabel('Stiffness Index Computation Time')
    pyl.ylim(min(stiffvals), max(stiffvals))
    pyl.xlim(0., max(stiffcomptimes))
    pyl.yscale('log')
    pyl.scatter(stiffcomptimes, stiffvals, 0.1)
    if savefigures == 1:
        pyl.savefig('Stiffcomp_Stiffvals_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # Plot of stiffness computation times vs. stiffness index
    pyl.figure(plotnum)
    pyl.ylabel('Stiffness Index ')
    pyl.xlabel('Integration Time')
    pyl.xlim(0., max(solutiontimes))
    pyl.ylim(min(stiffvals), max(stiffvals))
    pyl.yscale('log')
    pyl.scatter(solutiontimes, stiffvals, 0.1)
    if savefigures == 1:
        pyl.savefig('Int_Stiffvals_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # if makerainbowplot:
    #     # Plot the stiffness at every point in the PaSR simulation
    #     # Create a mesh to plot on
    #     xcoords = np.arange(numparticles)
    #     ycoords = np.arange(numtsteps)
    #     xmesh, ymesh = np.meshgrid(xcoords, ycoords)
    #
    #     pyl.figure(plotnum)
    #     # pyl.xlim(0,numparticles)
    #     # pyl.ylim(0,numtsteps)
    #     pyl.xlabel('Particle Number')
    #     pyl.ylabel('PaSR Timestep')
    #     plot = pyl.contourf(xmesh, ymesh, pasrstiffnesses, 50)
    #     pyl.grid(b=True, which='both')
    #     cb = pyl.colorbar(plot)
    #     label = cb.set_label('log$_{10}$ (Stiffness Index)')
    #     if savefigures == 1:
    #         pyl.savefig('PaSR_Range_Stiffness_Index.' + figformat)

else:
    # Create a list of normalized dt values
    normtlist = []
    for i in tlist:
        normtlist.append(i / (tstop - tstart))

    # Plot the solution of the temperature
    pyl.figure(plotnum)
    if equation == 'VDP':
        ylab = 'Y_Value'
        pyl.ylabel(ylab)
    elif equation == 'Autoignition':
        ylab = 'Temperature'
        pyl.ylabel(ylab + ' (K)')
    pyl.xlabel('Time (sec)')
    # pyl.xlim(tstart, tstop)
    pyl.xlim(0, 1)
    pyl.plot(normtlist, primaryvals)
    pyl.grid(b=True, which='both')
    if savefigures == 1:
        pyl.savefig(equation + '_' +
                    ylab +
                    str(dt) +
                    '_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # Plot the time per integration
    pyl.figure(plotnum)
    pyl.xlabel('Time (sec)')
    pyl.ylabel('Integration time (sec)')
    # pyl.xlim(tstart, tstop)
    # pyl.ylim(0, 0.005)
    pyl.xlim(0, 1)
    pyl.plot(normtlist, solutiontimes)
    pyl.grid(b=True, which='both')
    if savefigures == 1:
        pyl.savefig(equation + '_Integration_Times_' +
                    str(dt) +
                    '_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    # Plot the stiffness indicator vs. time
    pyl.figure(plotnum)
    pyl.xlabel('Time (sec)')
    pyl.ylabel('Stiffness Indicator')
    # pyl.xlim(tstart, tstop)
    pyl.xlim(0, 1)
    pyl.plot(normtlist, stiffvalues)
    pyl.grid(b=True, which='both')
    if savefigures == 1:
        pyl.savefig(equation + '_' +
                    method + '_' +
                    str(dt) +
                    '_' + timer.strftime("%m_%d") +
                    '.' + figformat)
    plotnum += 1

    if findtimescale:
        # Plot the reference timescales vs. time
        pyl.figure(plotnum)
        pyl.xlabel('Time (sec)')
        pyl.ylabel('Reference Timescale')
        pyl.xlim(tstart, tstop)
        pyl.plot(tlist, timescales)
        pyl.grid(b=True, which='both')
        if savefigures == 1:
            pyl.savefig(equation + '_Ref_Timescale_' +
                        str(dt) +
                        '_' + timer.strftime("%m_%d") +
                        '.' + figformat)
        plotnum += 1

"""
# Plot all of the 2nd derivatives vs stiffness index
for i in range(14):
    for j in range(len(pasrstiffnesses2[0, :, 0])):
        pyl.figure(i)
        # Label all of the x axes
        if i == 0:
            pyl.xlabel('Temperature, 2nd derivative')
            pyl.ylabel('Stiffness Index')
        else:
            pyl.ylabel('Stiffness Index', fontsize=12)
            pyl.xlabel(speciesnames[i - 1] + ' Mass Fraction, 2nd derivative',
                       fontsize=12)

        # Some of the derivatives may come out to zero, so we need to mask it
        for k in range(len(pasrstiffnesses2[:, j, i])):
            if pasrstiffnesses2[k, j, i] == 0:
                # Set values to None so that the plotter skips over them
                pasrstiffnesses2[k, j, i] = None
                pasrstiffnesses2[k, j, 14] = None

        # Hexbin plot used for sake of ease and making the files smaller
        plot = pyl.hexbin(abs(pasrstiffnesses2[:, j, i]),
                          pasrstiffnesses2[:, j, 14],
                          yscale='log',
                          xscale='log',
                          bins='log',
                          cmap='Blues',
                          gridsize=50,
                          mincnt=1
                          )
    cb = pyl.colorbar(plot)
    label = cb.set_label('log$_{10}$ |count + 1|', fontsize=12)

if savefigures == 1:
    for i in range(14):
        pyl.figure(i)
        pyl.savefig('COH2_PaSR_SI_p' + str(i) + figformat)

"""

finishtime = datetime.datetime.now()
print('Finish time: {}'.format(finishtime))

# pyl.close('all')
# pyl.show()
