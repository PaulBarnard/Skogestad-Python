'''
Created on Jan 27, 2012

@author: Carl Sandrock
'''

import numpy

#import control
#tf = control.TransferFunction

def circle(cx, cy, r):
    npoints = 100
    theta = numpy.linspace(0, 2*numpy.pi, npoints)
    y = cx + numpy.sin(theta)*r
    x = cx + numpy.cos(theta)*r
    return x, y

def distance_from_nominal(w, k, tau, theta, nom_response):
    r = k/(tau*w*i + 1)*numpy.exp(-theta*w*i)
    return numpy.abs(r - nom_response)

def arrayfun(f, A):
    """ recurses down to scalar elements in A, then applies f, returning lists containing the result"""
    if len(A.shape) == 0:
        return f(A)
    else:
        return [arrayfun(f, b) for b in A]

def listify(A):
    return [A]

def gaintf(K):
    r = tf(arrayfun(listify, K), arrayfun(listify, numpy.ones_like(K)))

def findst(G, K):
    """ Find S and T given a value for G and K """
    L = G*K
    I = numpy.eye(G.outputs, G.inputs)
    S = inv(I + L)
    T = S*L
    return S, T

def phase(G, deg=False):
    return numpy.unwrap(numpy.angle(G, deg=deg), discont=180 if deg else numpy.pi)


def Closed_loop(Kz, Kp, Gz, Gp):
    """Kz & Gz is the polynomial constants in the numerator
    Kp & Gp is the polynomial constants in the denominator"""

    # calculating the product of the two polynomials in the numerator and denominator of transfer function GK
    Z_GK = numpy.polymul(Kz, Gz)
    P_GK = numpy.polymul(Kp, Gp)

    #calculating the polynomial of closed loop sensitivity function s = 1/(1+GK)
    Zeros_poly = Z_GK
    Poles_poly = numpy.polyadd(Z_GK, P_GK)
    return Zeros_poly, Poles_poly

def RGA(Gin):
    """ Calculate the Relative Gain Array of a matrix """
    G = numpy.asarray(Gin)
    Ginv = numpy.linalg.pinv(G)
    return G*Ginv.T


def plot_direction(direction, name, color, figure_num):
    plt.figure(figure_num)
    if (direction.shape[0])>2:
        for i in range(direction.shape[0]):
            #label = '%s Input Dir %i' % (name, i+1)

            plt.subplot((direction.shape[0]), 1, i + 1)
            plt.title(name)
            plt.semilogx(w, direction[i, :], color)

    else:

        plt.subplot(211)
        plt.title(name)
        plt.semilogx(w, direction[0, :], color)

        plt.subplot(212)
        plt.title(name)
        plt.semilogx(w, direction[1, :], color)
