""" Filename: data_visualization.py
Outline
1. Initial demand and supply geographic map
2. Open and close facility map
3.

"""
import matplotlib.pyplot as plt
from matplotlib import collections as mc


# %% Plot customer and warehouse
def draw_initial_customer_demand(AllSt, facility, customer_df):
    # USA regions
    west = AllSt[AllSt['State_Code'].isin(['WA', 'OR', 'CA', 'ID', 'UT', 'MT', 'WY', 'CO', 'NV'])]
    southwest = AllSt[AllSt['State_Code'].isin(['AZ', 'NM', 'TX', 'OK'])]
    midwest = AllSt[AllSt['State_Code'].isin(['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'MI', 'IN', 'OH'])]
    southeast = AllSt[
        AllSt['State_Code'].isin(['AR', 'LA', 'MS', 'KY', 'TN', 'AL', 'WV', 'DC', 'VA', 'NC', 'SC', 'GA', 'FL'])]
    northeast = AllSt[AllSt['State_Code'].isin(['ME', 'VT', 'NH', 'MA', 'CT', 'RI', 'NY', 'PA', 'NJ', 'DE', 'MD'])]
    us_boundary_map = AllSt.boundary.plot(figsize=(18, 12), color='Black', linewidth=.5)

    west.plot(ax=us_boundary_map, color="MistyRose")
    southwest.plot(ax=us_boundary_map, color="PaleGoldenRod")
    southeast.plot(ax=us_boundary_map, color="Plum")
    midwest.plot(ax=us_boundary_map, color="PaleTurquoise")
    final_map = northeast.plot(ax=us_boundary_map, color="LightPink")

    # customer
    customer_df.plot(ax=us_boundary_map, marker='o', color='blue', markersize=50, alpha=0.1, label='Customer')

    # Plot potential facility locations as points
    facility.plot(ax=us_boundary_map, marker='p', color='red', markersize=500, alpha=1, label='Warehouse')

    for i in range(facility.shape[0]):
        plt.text(x=facility.longitude[i] - 1, y=facility.latitude[i] - 1,
                 s=facility.index[i] + 1,
                 fontdict=dict(color='black', size=15))
    plt.axis('off')

    # Add legend
    plt.legend(facecolor='white', title='Locations')
    # Add title
    # plt.title('Customer and warehouses locations')
    plt.show()


def draw_open_close_facility(AllSt, facility, customer_df):
    # Plot open and closed warehouse
    west = AllSt[AllSt['State_Code'].isin(['WA', 'OR', 'CA', 'ID', 'UT', 'MT', 'WY', 'CO', 'NV'])]
    southwest = AllSt[AllSt['State_Code'].isin(['AZ', 'NM', 'TX', 'OK'])]
    midwest = AllSt[AllSt['State_Code'].isin(['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'MI', 'IN', 'OH'])]
    southeast = AllSt[
        AllSt['State_Code'].isin(['AR', 'LA', 'MS', 'KY', 'TN', 'AL', 'WV', 'DC', 'VA', 'NC', 'SC', 'GA', 'FL'])]
    northeast = AllSt[AllSt['State_Code'].isin(['ME', 'VT', 'NH', 'MA', 'CT', 'RI', 'NY', 'PA', 'NJ', 'DE', 'MD'])]

    us_boundary_map = AllSt.boundary.plot(figsize=(18, 12), color='Black', linewidth=.5)

    west.plot(ax=us_boundary_map, color="MistyRose")
    southwest.plot(ax=us_boundary_map, color="PaleGoldenRod")
    southeast.plot(ax=us_boundary_map, color="Plum")
    midwest.plot(ax=us_boundary_map, color="PaleTurquoise")
    final_map = northeast.plot(ax=us_boundary_map, color="LightPink")

    # Plot customers as points
    customer_df.plot(ax=us_boundary_map, marker='*', color='blue', markersize=10, alpha=0.8, label='Customer')

    # Plot sites to establish
    facility.loc[facility.decisions == 'yes'].plot(ax=us_boundary_map, marker='p', color='red', markersize=120,
                                                   label='Keep')

    # Plot sites to discard
    facility.loc[facility.decisions == 'no']. \
        plot(ax=us_boundary_map, marker='p', color='yellow', markersize=120, label='Discard')

    # Add title
    plt.title('Optimized Warehouse Sites')
    # Add legend
    plt.legend(title='Warehouse Site', facecolor='white')
    # Remove ticks from axis
    plt.xticks([])
    plt.yticks([])
    # Show plot
    plt.show()


# %% Network Diagram
def draw_network_diagram(assignment, AllSt, facility0, customer_df0):
    # fig, ax = plt.subplots()
    us_boundary_map = AllSt.boundary.plot(figsize=(18, 12), color='Black', linewidth=.5)
    # customer
    customer_df0.plot(ax=us_boundary_map, marker='o', color='blue', markersize=50, alpha=0.1, label='Customer')
    # Plot potential facility locations as points
    facility0.plot(ax=us_boundary_map, marker='p', color='red', markersize=500, alpha=1, label='Warehouse')

    for i in range(facility0.shape[0]):
        plt.text(x=facility0.longitude[i] - 1, y=facility0.latitude[i] - 1,
                 s=facility0.index[i] + 1,
                 fontdict=dict(color='black', size=15))

    # plot the line segments, indicent points, and base station points of the final network
    unique_stations = assignment['facility no.'].unique()
    for ust in range(len(unique_stations)):
        d1 = assignment.loc[assignment['facility no.'] == unique_stations[ust]].reset_index()
        new_list = []
        for r in range(d1.shape[0]):
            new_list.append([(d1.c_longitude[r], d1.c_latitude[r]), (d1.f_longitude[r], d1.f_latitude[r])])
        lc = mc.LineCollection(new_list, colors=f'C{ust + 1}',
                               alpha=.2)  # alpha = (ust/len(unique_stations)), colors=ust,
        us_boundary_map.add_collection(lc)

    plt.axis('off')

    plt.show()
    plt.savefig('Outputs/network.png', transparent=True)
