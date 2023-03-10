""" FileName: model.py
Outline:

Developer:
Date: March 2023
"""
from gurobipy import Model, GRB, quicksum


def solve(I, J, p, d_ij, N):
    """
    :param I:
    :param J:
    :param p:
    :param d_ij:
    :param N:
    :return:
    """

    # Model
    mdl = Model('location')

    # Decision Variables
    z = mdl.addVars(I, vtype=GRB.BINARY, name='z')
    x = mdl.addVars(J, vtype=GRB.BINARY, name='x')

    obj = quicksum(p[i] * (z[i]) for i in I)
    mdl.setObjective(obj, sense=GRB.MAXIMIZE)
    # add constraints
    # Constraint1 what it is doing?
    C_capacity = mdl.addConstrs((quicksum((d_ij[i, j] * x[j]) for j in J) >= z[i] for i in I), name='capacity')

    C_max_facility = mdl.addConstr(quicksum((x[j]) for j in J) == N, name='max_facility')

    lpfile = mdl.write(mdl.lp)
    mdl.optimize()
    logfile = mdl.write(mdl.log)
    attrfile = mdl.write(mdl.attr)

    return lpfile, logfile, attrfile
