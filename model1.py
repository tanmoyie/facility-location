""" FileName: model.py
Outline: Write a computer model to implement the Integer Programming
Two decision variables and two constraints

Developer: M. Alam & T. Das
Date: March 2023
"""
from gurobipy import Model, GRB, quicksum
import pandas as pd


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
    mdl = Model('location allocation IP')
    # Decision Variables
    z = mdl.addVars(I, vtype=GRB.BINARY, name='z')
    x = mdl.addVars(J, vtype=GRB.BINARY, name='x')

    # Add constraints
    # Constraint1 what it is doing?
    C_capacity = mdl.addConstrs((quicksum((d_ij[i, j] * x[j]) for j in J) >= z[i] for i in I), name='capacity')
    C_max_facility = mdl.addConstr(quicksum((x[j]) for j in J) == N, name='max_facility')

    # Objective
    obj = quicksum(p[i] * (z[i]) for i in I)
    mdl.setObjective(obj, sense=GRB.MAXIMIZE)
    lpfile = 0  # mdl.write(mdl.lp)
    mdl.write('Outputs/model1.lp')
    # Run the model
    mdl.optimize()
    mdl.Params.LogFile = f"Outputs/model1.log"  # write the log file
    attrfile = mdl.write("Outputs/model1.attr")

    # %% Decision to open or close warehouse
    decision = []
    for var in mdl.getVars():
        if "x" in var.varName:
            if var.xn > 0:
                decision.append("yes")
            else:
                decision.append("no")

    decision_df = pd.DataFrame(decision, columns=["decisions"])

    return lpfile, attrfile, decision_df
