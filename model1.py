""" FileName: model.py
Outline: Write a computer model to implement the Integer Programming
Two decision variables and two constraints

Developer: M. Alam & T. Das
Date: March 2023
"""
from gurobipy import Model, GRB, quicksum
import pandas as pd


def solve(I, J, p, d_ij, N, facility, customer_df):
    """
    :param I:
    :param J:
    :param p:
    :param d_ij:
    :param N:
    :param facility:
    :param customer_df:
    :return:
    """

    # Model
    mdl = Model('location allocation IP')
    # Decision Variables
    z = mdl.addVars(I, J, vtype=GRB.BINARY, name='z')  # customer
    x = mdl.addVars(J, vtype=GRB.BINARY, name='x')  # facility

    # Add constraints
    # Constraint1 what it is doing?
    # C_capacity = mdl.addConstrs((quicksum((d_ij[i, j] * x[j]) for j in J)
    #               >= z[i, j] for i in I for j in J), name='capacity')
    c1 = mdl.addConstrs((z[i, j] <= x[j] for i in I for j in J), name='c1')
    C_max_facility = mdl.addConstr(quicksum((x[j]) for j in J) == N, name='max_facility')
    C_facility_per_customer = mdl.addConstrs((z.sum(i, '*') <= 1 for i in I), name='facility_per_customer')

    # Objective
    obj = quicksum((p[i] - d_ij[i, j]) * z[i, j] for i in I for j in J)
    mdl.setObjective(obj, sense=GRB.MAXIMIZE)

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

    #%% Extract sol
    # Extract assignment variables
    z_series = pd.Series(mdl.getAttr('X', z))
    z_1s = z_series[z_series > 0.5]
    x_series = pd.Series(mdl.getAttr('X', x))
    x_1s = x_series[x_series > 0.5]

    sol_z = pd.Series(mdl.getAttr('X', z))
    sol_z.name = 'Assignments'
    sol_z.index.names = ['customer no.', 'facility no.']
    assignment0 = sol_z[sol_z > 0.5].to_frame()
    assignment_name = assignment0.reset_index()

    # organize data
    customer_df2 = pd.DataFrame(customer_df[['longitude', 'latitude']]).reset_index()
    customer_df2.columns = ['customer no.', 'c_longitude', 'c_latitude']
    facility_df = pd.DataFrame(facility[['longitude', 'latitude']]).reset_index()
    facility_df.columns = ['facility no.', 'f_longitude', 'f_latitude']
    assignment2 = pd.merge(assignment_name[['customer no.', 'facility no.']],
                           facility_df[['facility no.', 'f_longitude', 'f_latitude']], on='facility no.')
    assignment = pd.merge(assignment2, customer_df2[['customer no.', 'c_longitude', 'c_latitude']])

    return z_1s, x_1s, customer_df2, facility_df, assignment, attrfile, decision_df, assignment_name
