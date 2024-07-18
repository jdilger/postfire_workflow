# gee helpers

import ee
import math

UPPER_LEFT = 0
LOWER_LEFT = 1
LOWER_RIGHT = 2
UPPER_RIGHT = 3
PI = lambda: ee.Number(math.pi)
MAX_SATELLITE_ZENITH = 7.5

def line_from_coords(coordinates, fromIndex, toIndex):
    return ee.Geometry.LineString(ee.List([
        coordinates.get(fromIndex),
        coordinates.get(toIndex)]))


def line(start, end):
    return ee.Geometry.LineString(ee.List([start, end]))


def degToRad(deg):
    return deg.multiply(PI().divide(180))


def value(list, index):
    return ee.Number(list.get(index))


def radToDeg(rad):
    return rad.multiply(180).divide(PI())


def where(condition, trueValue, falseValue):
    trueMasked = trueValue.mask(condition)
    falseMasked = falseValue.mask(invertMask(condition))
    return trueMasked.unmask(falseMasked)


def invertMask(mask):
    return mask.multiply(-1).add(1)


def x(point):
    return ee.Number(ee.List(point).get(0))


def y(point):
    return ee.Number(ee.List(point).get(1))


def determine_footprint(image):
    footprint = ee.Geometry(image.get('system:footprint'))
    bounds = ee.List(footprint.bounds().coordinates().get(0))
    coords = footprint.coordinates()

    xs = coords.map(lambda item: x(item))
    ys = coords.map(lambda item: y(item))

    def findCorner(targetValue, values):
        diff = values.map(lambda value: ee.Number(value).subtract(targetValue).abs())
        minValue = diff.reduce(ee.Reducer.min())
        idx = diff.indexOf(minValue)
        return coords.get(idx)

    lowerLeft = findCorner(x(bounds.get(0)), xs)
    lowerRight = findCorner(y(bounds.get(1)), ys)
    upperRight = findCorner(x(bounds.get(2)), xs)
    upperLeft = findCorner(y(bounds.get(3)), ys)

    return ee.List([upperLeft, lowerLeft, lowerRight, upperRight, upperLeft])


def replace_bands(image, bands):
    result = image
    for band in bands:
        result = result.addBands(band, overwrite=True)
    return result


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
    c1_col = col.filterDate('1970-01-01',f'{c2_threshold-1}-12-31')
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

