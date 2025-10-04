import ee
import geemap
import datetime
import json

from utils.utils import BANDS, RENAME_MAP, sample_point, calculate_ndvi, calculate_gndvi, calculate_bloom_dates

def fetch_data_year(lat, lon, year):
    # Define area of interest (example coordinates)
    # TODO: allow polygon input for field data
    aoi = ee.Geometry.Point([lon, lat])  # or use a polygon for a field

    # TODO: adjust end date limit based on most recent data
    date_start = f"{year}-01-01"
    date_end = f"{year}-12-31"
    date_start = '2017-03-28' if date_start < '2017-03-28' else date_start
    date_end = '2025-10-04' if date_end > '2025-10-04' else date_end

    # Filter Sentinel-2 harmonized dataset
    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .select(BANDS)
    )

    # Map the function over the ImageCollection and convert to a FeatureCollection.
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(BANDS))

    df = geemap.ee_to_df(samples_fc)

    # TODO: perform these additions in the dataframe directly, for efficiency and for data analytics purposes
    df = df.rename(columns=RENAME_MAP)
    dict_data = df.to_dict(orient='list')
    dict_data['ndvi'] = [calculate_ndvi(r, n) for r, n in zip(dict_data['red'], dict_data['nir'])]
    dict_data['gndvi'] = [calculate_gndvi(g, n) for g, n in zip(dict_data['green'], dict_data['nir'])]
    dict_data['bloom_dates'] = calculate_bloom_dates()

    return json.dumps(dict_data)

def fetch_data_full(lat, lon):
    aoi = ee.Geometry.Point([lon, lat])

    # TODO: adjust end date limit based on most recent data
    date_start = '2017-03-28'
    date_end = '2025-10-04'

    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select(BANDS)
    )
    
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(BANDS))
    df = geemap.ee_to_df(samples_fc)

    # TODO: perform these additions in the dataframe directly, for efficiency and for data analytics purposes
    df = df.rename(columns=RENAME_MAP)
    dict_data = df.to_dict(orient='list')
    dict_data['ndvi'] = [calculate_ndvi(r, n) for r, n in zip(dict_data['red'], dict_data['nir'])]
    dict_data['gndvi'] = [calculate_gndvi(g, n) for g, n in zip(dict_data['green'], dict_data['nir'])]
    dict_data['bloom_dates'] = calculate_bloom_dates()

    return json.dumps(dict_data)
