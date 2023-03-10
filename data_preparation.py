""" Filename: data_preparation.py

Outline:



"""


def data_preparation(df):
    # %% section name
    df2 = df[['NAME', 'ST', 'POPULATION', 'longitude', 'latitude']]
    df2.head()

    # remove two states: AK and HI
    twos = df2[df2['ST'].isin(['AK', 'HI'])].index
    df2.drop(twos, inplace=True)

    df2.reset_index(inplace=True)

    df2.drop("index", axis=1, inplace=True)

    # %% Section name
    # choose 5 cities from 5 region
    facility2 = df2[df2['NAME'].isin(['Atlanta','Chicago','Dallas','New York', 'San Francisco'])]
    facility2
    # filter by taking population
    facility2 = facility2[facility2['POPULATION'].isin([2781116, 871042, 464043, 8691599, 1323651])]

    facility2.reset_index(inplace=True)
    facility2.drop("index", axis=1, inplace=True)
    facility2['ST'].nunique()

    #%%
    # All cities are customer
    customer_df = df2.copy()
    customer_df.head()

    # Customers IDs list
    customer_df['customer_id'] = range(1, 1 + customer_df.shape[0])

    def add_geocoordinates(df2, lat='longitude', lng='latitude'):
        '''
        Add column "geometry" with <shapely.geometry.point.Point> objects
            built from latitude and longitude values in the input dataframe

        Args:
            - df: input dataframe
            - lat: name of the column containing the latitude (default: lat)
            - lng: name of the column containing the longitude (default: lng)
        Out:
            - df: same dataframe enriched with a geo-coordinate column
        '''
        assert pd.Series([lat, lng]).isin(df2.columns).all(), \
            f'Cannot find columns "{lat}" and/or "{lng}" in the input dataframe.'
        return geopandas.GeoDataFrame(
            df2, geometry=geopandas.points_from_xy(df2.longitude, df2.latitude))

    customer_df = add_geocoordinates(customer_df)
    facility2 = add_geocoordinates(facility2)

    facility2.head()

    #%% Draw location graph
    # Load geometric file for map
    AllSt = geopandas.read_file("Data/States_shapefile.shp")
    # remove 2 states from map
    indexNames = AllSt[AllSt['State_Code'].isin(['AK', 'HI'])].index
    AllSt.drop(indexNames, inplace=True)

    #%% Plot customer and warehouse

    # Plot customer and warehouse
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

    customer_df. \
        plot(ax=us_boundary_map, marker='*', color='blue', markersize=10, alpha=0.8, label='Customer')

    # Plot potential facility locations as points
    facility2. \
        plot(ax=us_boundary_map, marker='p', color='red', markersize=120, alpha=0.9, label='Warehouse')

    # Add legend
    plt.legend(facecolor='white', title='Locations')

    # Add title
    plt.title('Customer and warehouses locations')



