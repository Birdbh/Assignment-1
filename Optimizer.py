import cvxpy as cp

def Optimizer(Pmax, n_c, n_d, Cmax, C_0, C_n, p):

    # Define the length of your horizon
    n = len(p)
    
    # Define your optimization variables
    p_c = cp.Variable(n)
    p_d = cp.Variable(n)
    X   = cp.Variable(n)
    
    # Define your cost function
    profit = cp.sum(p_d@p - p_c@p)
    
    # Define your constraints
    constraints = [p_c >= 0, 
               p_d >= 0, 
               p_c <= Pmax, 
               p_d <= Pmax]
    constraints += [X >= 0.1*Cmax, X <= Cmax]
    constraints += [X[0]==C_0 + p_c[0]*n_c - p_d[0]/n_d]

    for j in range(1,n):
        constraints += [X[j]==X[j-1] + p_c[j]*n_c - p_d[j]/n_d]

    constraints += [X[n-1]>=C_n]
    
    # Solve the problem
    problem = cp.Problem(cp.Maximize(profit), constraints)
    problem.solve(solver=cp.ECOS)
    
    return profit.value, p_c.value, p_d.value, X.value
