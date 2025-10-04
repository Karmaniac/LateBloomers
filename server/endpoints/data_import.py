import ee
import geemap
import datetime

def authenticate_service_account(service_account, private_key_path):
    credentials = ee.ServiceAccountCredentials(service_account, private_key_path)
    ee.Initialize(credentials=credentials)

def sample_point(img, aoi):
    # Compute mean over the AOI for each image. Use bestEffort to avoid failures
    # on very large geometries.
    mean = img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=10,
        bestEffort=True,
    )
    # Return a Feature with the band's mean values and the image date.
    return ee.Feature(None, mean).set('date', img.date().format('YYYY-MM-dd'))

def fetch_data_year(lat, lon, date):
    # Define area of interest (example coordinates)
    aoi = ee.Geometry.Point([lon, lat])  # or use a polygon for a field

    # TODO: adjust end date limit based on most recent data
    input_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_start = (input_date - datetime.timedelta(days=182)).strftime("%Y-%m-%d")
    date_end = (input_date + datetime.timedelta(days=183)).strftime("%Y-%m-%d")
    date_start = '2017-03-28' if date_start < '2017-03-28' else date_start
    date_end = '2025-10-04' if date_end > '2025-10-04' else date_end

    # Filter Sentinel-2 harmonized dataset
    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select('B3', 'B4')  # Green + red bands
    )

    # Sample each image at a point and bring results to pandas
    # Note: geemap.ee_to_df expects an ee.FeatureCollection. Mapping a function
    # over an ImageCollection that returns Features still yields an ImageCollection,
    # so we explicitly wrap the mapped results with ee.FeatureCollection(...).

    # Map the function over the ImageCollection and convert to a FeatureCollection.
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))

    # Optionally remove rows with null band values (e.g., if image doesn't cover AOI
    # or values are masked). Adjust band names as needed.
    samples_fc = samples_fc.filter(ee.Filter.notNull(['B3', 'B4']))

    # Convert to pandas DataFrame (make sure the collection is reasonably small).
    df = geemap.ee_to_df(samples_fc)

    # json_data = df.to_json()

    return df

def fetch_data_full(lat, lon):
    aoi = ee.Geometry.Point([lon, lat])

    # TODO: adjust end date limit based on most recent data
    date_start = '2017-03-28'
    date_end = '2025-10-04'

    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(aoi)
        .select('B3', 'B4')  # Green + red bands
    )
    
    samples_fc = ee.FeatureCollection(s2.map(lambda img: sample_point(img, aoi)))
    samples_fc = samples_fc.filter(ee.Filter.notNull(['B3', 'B4']))
    df = geemap.ee_to_df(samples_fc)

    return df
