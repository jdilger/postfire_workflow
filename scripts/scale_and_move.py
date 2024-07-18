import ee
import ee.batch
#need auth_mode gcloud-legacy for exporting to legacy assets
# ee.Authenticate(force=True,auth_mode='gcloud-legacy')
ee.Initialize()
def scaleLandsatC2(img):
    """Landsat is scaled using Collection 2 factors."""

    # Apply scaling and offset for optical bands
    optical_bands = img.select(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']).multiply(0.0000275).add(-0.2)
    # Apply scaling and offset for the thermal band
    thermal_band = img.select(ee.List(['temp'])).multiply(0.00341802).add(149.0)

    # Combine the scaled bands with the original TDOMMask
    scaled_image = optical_bands.addBands(thermal_band)

    return scaled_image.set('system:time_start',img.date())
def scaleLandsatC1(img):
    """Landast is scaled by factor 0.0001 """
    thermal_band = img.select(ee.List(['temp'])).multiply(0.1)
    optical_bands = img.select(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']).multiply(ee.Number(0.0001))
    scaled_image = optical_bands.addBands(thermal_band)
    return scaled_image.set('system:time_start',img.date())

def scale_by_collection_type(col, c2_threshold:int)->ee.ImageCollection:
    c1_col = col.filterDate('1970-01-01',f'{c2_threshold}-12-31')
    c2_col = col.filterDate(f'{c2_threshold+1}-01-01','2050-01-01')
    c1_col = c1_col.map(scaleLandsatC1)
    c2_col = c2_col.map(scaleLandsatC2)
    return c1_col.merge(c2_col)
def scale_pfvms(col:ee.ImageCollection)->ee.ImageCollection:
    """The summer and fall pfvms images are stored in unscaled values. Originally,they used Landsat Collection 1
    which has a different scaling factor than the images retrieved after 2021 which are from Collection 2. This helper function
    scales each image to it's correct SR value.

    Args:
        col (ee.ImageCollection): Image collection (Summer_Full or Fall_Full)

    Returns:
        ee.ImageCollection: Image collection scaled to SR values.
    """
    c2_start_year = 2021
    scaled = scale_by_collection_type(col, c2_start_year)
    return scaled

ee_legacy_root = 'projects/earthengine-legacy/assets'
src_summer = f'{ee_legacy_root}/projects/sig-ee/PostFireVeg/SeasonComposites/Summer_Full'
src_fall = f'{ee_legacy_root}/projects/sig-ee/PostFireVeg/SeasonComposites/Fall_Full'
dst_summer = f'{src_summer}_SR'
dst_fall = f'{src_fall}_SR'

summer_unscaled = ee.ImageCollection(src_summer)
fall_unscaled = ee.ImageCollection(src_fall)

c2_threshold = 2021
summer_scaled = scale_by_collection_type(summer_unscaled, c2_threshold)
fall_scaled = scale_by_collection_type(fall_unscaled, c2_threshold)


def export_each_image(col, dst):
    studyArea = ee.FeatureCollection("users/TEST/CAFire/StudyAreas/finalStudyArea").geometry().bounds().buffer(
        5000).getInfo()['coordinates']
    image_ids = col.aggregate_array("system:index").getInfo()

    for image_id in image_ids:
        img = col.filter(ee.Filter.eq('system:index', image_id)).first()
        assetId=f"{dst}/{image_id[2:]}"

        ee.batch.Export.image.toAsset(
            image=img,
            description=image_id,
            assetId=assetId,
            region=studyArea,
            scale=30,
            crs="EPSG:26910",
            maxPixels=1e13,

         ).start()
        print('started', assetId)
        
export_each_image(summer_scaled, dst_summer)
export_each_image(fall_scaled, dst_fall)
