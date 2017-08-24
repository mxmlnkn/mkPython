
def eulerOneStep(t0,h,v0,f):
    """
    One step of euler integration for solving the differential
    equation dv/dt = f e.g. interpretable as velocity change due to a force
    on an unchanging massive object
    """
    return v0 + f2(t0,v0)*h

def euler(f,t,t0,v0,N=1000):
    dt = 1.*t/N
    v1 = v0
    t1 = t0
    for i in range(N):
        v1  = eulerOneStep(f,dt,t1,v1)
        t1 += dt
    return v1
