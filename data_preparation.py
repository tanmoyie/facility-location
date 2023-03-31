""" Filename: data_preparation.py

Outline:
Create dataset of customer and facility points (to be used by model)

Date: March 2023

"""

import geopandas
import pandas as pd


def data_prep(data_demand):
    """
    :param data_demand:
    :return: demand and customer points
    """
    # remove two states: AK and HI
    non_mainland = data_demand[data_demand['ST'].isin(['AK', 'HI'])].index
    data_demand.drop(non_mainland, inplace=True)
    data_demand.reset_index(inplace=True)
    data_demand.drop("index", axis=1, inplace=True)

    # %% Section name
    # choose 5 cities from 5 region
    facility_raw = data_demand[data_demand['NAME'].isin(['Atlanta', 'Chicago', 'Dallas', 'New York', 'San Francisco'])]
    # filter by taking population ??
    facility = facility_raw[facility_raw['POPULATION'].isin([2781116, 871042, 464043, 8691599, 1323651])]

    facility.reset_index(inplace=True)
    facility.drop("index", axis=1, inplace=True)
    facility['ST'].nunique()

    # %%
    # All cities are customer
    customer_df = data_demand.copy()
    customer_df.head()

    # Customers IDs list
    customer_df['customer_id'] = range(1, 1 + customer_df.shape[0])

    def add_geocoordinates(data_demand, lat='longitude', lng='latitude'):
        assert pd.Series([lat, lng]).isin(data_demand.columns).all(), \
            f'Cannot find columns "{lat}" and/or "{lng}" in the input dataframe.'
        return geopandas.GeoDataFrame(
            data_demand, geometry=geopandas.points_from_xy(data_demand.longitude, data_demand.latitude))

    customer_df = add_geocoordinates(customer_df)
    facility = add_geocoordinates(facility)

    # Facility
    facility['facility_coord'] = facility['latitude'].astype(str) + ',' + facility['longitude'].astype(str)
    facility['warehouse_id'] = ['Warehouse ' + str(i) for i in range(1, 1 + facility.shape[0])]
    # Customer
    customer_df['customer_coord'] = customer_df['latitude'].astype(str) + ',' + customer_df['longitude'].astype(str)
    customer_df['customer_id'] = range(1, 1 + customer_df.shape[0])
    return facility, customer_df
