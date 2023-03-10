import cvxpy as cp

def ProsumerOptimizer(Pmax, n_c, n_d, Cmax, C_0, C_n, l_b, l_s, p_PV, p_L):

    # Define the length of your horizon
    n = len(l_b)
    
    # Define your optimization variables
    p_c = cp.Variable(n)
    p_d = cp.Variable(n)
    p_s = cp.Variable(n)
    p_b = cp.Variable(n)
    X   = cp.Variable(n)
    
    #Bought from the grid minus sold from the grid
    cost = cp.sum(p_b@l_b - p_s@l_s)
    
    # Define your constraints
    constraints = [p_c >= 0, 
                   p_d >= 0, 
                   p_c <= Pmax, 
                   p_d <= Pmax,
                   0 <= p_b,
                   0 <= p_s]
    constraints += [p_PV+p_b+p_d == p_L+p_s+p_c]
    constraints += [X >= Cmax*0.1, X <= Cmax]
    constraints += [X[0]==C_0 + p_c[0]*n_c - p_d[0]/n_d]

    for j in range(1,n):
        constraints += [X[j]==X[j-1] + p_c[j]*n_c - p_d[j]/n_d]

    constraints += [X[n-1]>=C_n]
    
    # Solver the problem
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve(solver=cp.ECOS)
    
    return cost.value, p_c.value, p_d.value, p_b.value, p_s.value, X.value
