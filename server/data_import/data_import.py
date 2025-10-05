import ee
import geemap

from utils.utils import BANDS, CLIMATE_BANDS, RENAME_MAP, sample_point, calculate_ndvi, calculate_gndvi, calculate_bloom_dates

# TODO: handle cloud coverage filtering and other image quality issues

# mask helper: use SCL to remove cloud/shadow/cirrus
def mask_s2_scl(image):
    # SCL values: 3 = cloud shadow, 8 = medium prob cloud, 9 = high prob cloud,
    # 10 = thin cirrus, 11 = snow. Keep pixels that are NOT those classes.
    scl = image.select('SCL')
    good = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    # optional: remove very low-quality pixels (SCL == 1 or 2)
    good = good.And(scl.neq(1)).And(scl.neq(2))
    return image.updateMask(good)

# fallback using QA60 bitmask (for TOA collections that include QA60)
def mask_s2_qa60(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask)

# Example: combine masks (SCL preferred; if missing, use QA60)
def mask_clouds(image):
    # if SCL exists use it, otherwise fall back to QA60 if present
    def use_scl(img):
        return mask_s2_scl(img)
    def use_qa(img):
        return mask_s2_qa60(img)
    return ee.Algorithms.If(image.bandNames().contains('SCL'), use_scl(image), use_qa(image))

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

def fetch_climate_data(lat, lon):
    aoi = ee.Geometry.Point([lon, lat])

    # TODO: adjust end date limit based on most recent data
    # date_start = '1950-01-02'
    date_start = '2020-01-02'
    date_end = '2025-09-26'

    s2 = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select(CLIMATE_BANDS)
    )
    
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(CLIMATE_BANDS))
    df = geemap.ee_to_df(samples_fc)
    print(df.head())

    # dict_data = df.to_dict(orient='list')

    # return dict_data
