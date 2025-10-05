import ee
import json
import math

BANDS = ['B3', 'B4', 'B8']  # Green + red + NIR bands
CLIMATE_BANDS = []
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
