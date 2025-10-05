import ee
import json
import math
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import geemap

BANDS = ['B3', 'B4', 'B8']  # Green + red + NIR bands
CLIMATE_BANDS = [
    'dewpoint_temperature_2m',
    'temperature_2m',
    'soil_temperature_level_1',
    'soil_temperature_level_2',
    'soil_temperature_level_3',
    'soil_temperature_level_4',
    'skin_reservoir_content',
    'volumetric_soil_water_layer_1',
    'volumetric_soil_water_layer_2',
    'volumetric_soil_water_layer_3',
    'volumetric_soil_water_layer_4',
    'evaporation_from_bare_soil_sum',
    'evaporation_from_the_top_of_canopy_sum',
    'evaporation_from_vegetation_transpiration_sum',
    'potential_evaporation_sum',
    'runoff_sum',
    'total_evaporation_sum',
    'u_component_of_wind_10m',
    'v_component_of_wind_10m',
    'surface_pressure',
    'total_precipitation_sum',
    'leaf_area_index_low_vegetation'
]
RENAME_MAP = {
    'B3': 'green',
    'B4': 'red',
    'B8': 'nir',
    'date': 'dates'
}

def print_json(data):
    data = json.loads(data)
    print(json.dumps(data, indent=2))

def calculate_ndvi(red, nir):
    # NDVI = (NIR - Red) / (NIR + Red)
    ndvi = (nir - red) / (nir + red)
    return ndvi

def calculate_gndvi(green, nir):
    # GNDVI = (Green - NIR) / (Green + NIR)
    gndvi = (green - nir) / (green + nir)
    return gndvi

def authenticate_service_account(service_account, private_key_path):
    credentials = ee.ServiceAccountCredentials(service_account, private_key_path)
    ee.Initialize(credentials=credentials)

def sample_point(img, aoi):
    # Sample each image at a point and bring results to pandas
    # Note: geemap.ee_to_df expects an ee.FeatureCollection. Mapping a function
    # over an ImageCollection that returns Features still yields an ImageCollection,
    # so we explicitly wrap the mapped results with ee.FeatureCollection(...).

    # Compute mean over the AOI for each image. Use bestEffort to avoid failures
    # on very large geometries.
    mean = img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=10,
        bestEffort=True,
    )
    # Return a Feature with the band's mean values and the image date.
    return ee.Feature(aoi, mean).set('date', img.date().format('YYYY-MM-dd'))

# TODO: implement calculate_bloom_dates
def calculate_bloom_dates():
    return []

def relative_humidity(temp_k, dewpoint_k):
    """Compute RH (%) from temperature and dew point in °K."""
    temp_c = temp_k - 273.15
    dewpoint_c = dewpoint_k - 273.15
    # Saturation vapor pressure (hPa)
    es = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    # Actual vapor pressure (hPa)
    e = 6.112 * math.exp((17.67 * dewpoint_c) / (dewpoint_c + 243.5))
    # Relative humidity (%)
    rh = 100 * (e / es)
    return rh

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

# def schedule_data_poll():
#     # Schedule a daily data poll at 5am
#     """Schedule poll_data once per day at 05:00 using APScheduler BackgroundScheduler.
#     Returns the started scheduler instance."""

#     print("Scheduling daily data poll at 05:00")
#     scheduler = BackgroundScheduler()
#     # run daily at 05:00 local time
#     scheduler.add_job(poll_data, 'cron', hour=10, minute=40, id='daily_poll')
#     scheduler.start()
     
#     # shutdown scheduler cleanly on exit
#     atexit.register(lambda: scheduler.shutdown(wait=False))
#     return scheduler
