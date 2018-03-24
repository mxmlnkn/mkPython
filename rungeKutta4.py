#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def rungeKutta4OneStep(f,dt,t0,v0):
    """
    One step of Runge-Kutta integration for solving the differential
    equation dv/dt = f e.g. interpretable as velocity change due to a force
    on an unchanging massive object
    """
    va = v0 + dt/2.0*  f(t0       ,v0)
    vb = v0 + dt/2.0*  f(t0+dt/2.0,va)
    vc = v0 + dt    *  f(t0+dt/2.0,vb)  # using va here actually reduces the error scaling to O(h^4)
    v1 = v0 + dt/6.0*( f(t0       ,v0)
               + 2.0*( f(t0+dt/2.0,va)
               +       f(t0+dt/2.0,vb) )
               +       f(t0+dt    ,vc) )
    return v1

def rungeKutta4(f,t,t0,v0,N=1000):
    dt = 1.*t/N
    v1 = v0
    t1 = t0
    for i in range(N):
        v1  = rungeKutta4OneStep(f,dt,t1,v1)
        t1 += dt
    return v1
