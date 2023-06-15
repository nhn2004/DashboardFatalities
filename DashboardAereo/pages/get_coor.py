'''import pandas as pd
from geopy.geocoders import OpenCage

geocoder = OpenCage('9f60422213fc4cb5a210e1f916c11c0f')

locs_gb = pd.read_csv('locs_gb.csv')

locs_gb['Latitude'] = None
locs_gb['Longitude'] = None

for index, row in locs_gb.iterrows():
    location = row['location']
    try:
        result = geocoder.geocode(location)
        if result and 'geometry' in result.raw:
            latitude = result.raw['geometry']['lat']
            longitude = result.raw['geometry']['lng']
            locs_gb.loc[index, 'Latitude'] = latitude
            locs_gb.loc[index, 'Longitude'] = longitude
    except:
        pass
 
locs_gb.to_csv('coordinates.csv', index=True)'''
