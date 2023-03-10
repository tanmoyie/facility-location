""" Filename: data_preparation.py

Outline:



"""

#%% section name
df2 = df[['NAME', 'ST', 'POPULATION', 'longitude', 'latitude']]
df2.head()

#remove two states: AK and HI
twos = df2[df2['ST'].isin(['AK', 'HI'])].index
df2.drop(twos, inplace=True)

df2.reset_index(inplace=True)

df2.drop("index", axis=1, inplace=True)

#%% Section name


