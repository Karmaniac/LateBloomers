import ee
import geemap
from datetime import datetime

from utils.utils import BANDS, CLIMATE_BANDS, RENAME_MAP, sample_point, calculate_ndvi, calculate_gndvi, calculate_bloom_dates, mask_clouds

last_polled_timestamp_s2 = '0000-00-00'
last_polled_timestamp_era5 = '0000-00-00'

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
        .map(lambda img: ee.Image(mask_clouds(img)))
        .select(BANDS)
    )

    # Map the function over the ImageCollection and convert to a FeatureCollection.
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(BANDS))

    df = geemap.ee_to_df(samples_fc)

    # TODO: perform these additions in the dataframe directly, for efficiency and for data analytics purposes
    df = df.rename(columns=RENAME_MAP)
    dict_data = df.to_dict(orient='list')
    if dict_data:
        dict_data['ndvi'] = [calculate_ndvi(r, n) for r, n in zip(dict_data['red'], dict_data['nir'])]
        dict_data['gndvi'] = [calculate_gndvi(g, n) for g, n in zip(dict_data['green'], dict_data['nir'])]
        dict_data['bloom_dates'] = calculate_bloom_dates()

    return dict_data

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

    return dict_data

def fetch_climate_data(lat, lon, year):
    aoi = ee.Geometry.Point([lon, lat])

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
        .map(lambda img: ee.Image(mask_clouds(img)))
        .select(BANDS)
    )

    # Map the function over the ImageCollection and convert to a FeatureCollection.
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(BANDS))

    df_s2 = geemap.ee_to_df(samples_fc)

    if df_s2.empty:
        return {}

    # TODO: perform these additions in the dataframe directly, for efficiency and for data analytics purposes
    df_s2 = df_s2.rename(columns=RENAME_MAP)
    dict_data_s2 = df_s2.to_dict(orient='list')
    if dict_data_s2:
        dict_data_s2['ndvi'] = [calculate_ndvi(r, n) for r, n in zip(dict_data_s2['red'], dict_data_s2['nir'])]
        dict_data_s2['gndvi'] = [calculate_gndvi(g, n) for g, n in zip(dict_data_s2['green'], dict_data_s2['nir'])]
        dict_data_s2['bloom_dates'] = calculate_bloom_dates()



    # TODO: adjust end date limit based on most recent data
    date_start = f"{year}-01-01"
    date_end = f"{year}-12-31"
    date_start = '2017-03-28' if date_start < '2017-03-28' else date_start

    era5 = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select(CLIMATE_BANDS)
    )
    
    samples_fc = ee.FeatureCollection(era5.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(CLIMATE_BANDS))
    
    df_era5 = geemap.ee_to_df(samples_fc)
    df_era5 = df_era5.rename(columns={'date': 'dates'})
    df_era5 = df_era5[df_era5['dates'].isin(df_s2['dates'])]  # align dates with S2 data
    dict_data_era5 = df_era5.to_dict(orient='list')

    return {**dict_data_s2, **dict_data_era5}

def poll_data(lat, lon):
    print("Polling data...")
    
    aoi = ee.Geometry.Point([lon, lat])
    year = datetime.now().year

    date_start = f"{year}-01-01"
    date_end = f"{year}-12-31"

    # Filter Sentinel-2 harmonized dataset
    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .map(lambda img: ee.Image(mask_clouds(img)))
        .select(BANDS)
    )

    # Map the function over the ImageCollection and convert to a FeatureCollection.
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(BANDS))

    df_s2 = geemap.ee_to_df(samples_fc)

    if not df_s2.empty:
        df_s2 = df_s2.rename(columns=RENAME_MAP)
        dict_data_s2 = df_s2.to_dict(orient='list')
        if dict_data_s2:
            dict_data_s2['ndvi'] = [calculate_ndvi(r, n) for r, n in zip(dict_data_s2['red'], dict_data_s2['nir'])]

    era5 = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select(CLIMATE_BANDS)
    )
    
    samples_fc = ee.FeatureCollection(era5.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(CLIMATE_BANDS))
    
    df_era5 = geemap.ee_to_df(samples_fc)
    df_era5 = df_era5.rename(columns={'date': 'dates'})
    df_era5 = df_era5[df_era5['dates'].isin(df_s2['dates'])]  # align dates with S2 data
    dict_data_era5 = df_era5.to_dict(orient='list')

    new_data = False
    global last_polled_timestamp_s2
    if not df_s2.empty:
        latest_timestamp_s2 = max(df_s2['dates'])
        if latest_timestamp_s2 > last_polled_timestamp_s2:
            last_polled_timestamp_s2 = latest_timestamp_s2
            new_data = True
    global last_polled_timestamp_era5
    if not df_era5.empty:
        latest_timestamp_era5 = max(df_era5['dates'])
        if latest_timestamp_era5 > last_polled_timestamp_era5:
            last_polled_timestamp_era5 = latest_timestamp_era5
            new_data = True

    if not new_data:
        print("No new data found.")
        return {}
    else:
        print(f"New data found. Latest S2 timestamp: {last_polled_timestamp_s2}, Latest ERA5 timestamp: {last_polled_timestamp_era5}")
        return {
            "s2_data": dict_data_s2,
            "era5_data": dict_data_era5
        }
