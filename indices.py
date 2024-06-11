import ee
import math

# ///////////////////////////////////////////////////////////////////////////////
# // Function to add common (and less common) spectral indices to an image.
# // Includes the Normalized Difference Spectral Vector from (Angiuli and Trianni, 2014)
def addIndices(img):
    # // Add Normalized Difference Spectral Vector (NDSV)
    img = img.addBands(img.normalizedDifference(['blue','green']).rename('ND_blue_green'));
    img = img.addBands(img.normalizedDifference(['blue','red']).rename('ND_blue_red'));
    img = img.addBands(img.normalizedDifference(['blue','nir']).rename('ND_blue_nir'));
    img = img.addBands(img.normalizedDifference(['blue','swir1']).rename('ND_blue_swir1'));
    img = img.addBands(img.normalizedDifference(['blue','swir2']).rename('ND_blue_swir2'));

    img = img.addBands(img.normalizedDifference(['green','red']).rename('ND_green_red'));
    img = img.addBands(img.normalizedDifference(['green','nir']).rename('ND_green_nir')); #//NDWBI
    img = img.addBands(img.normalizedDifference(['green','swir1']).rename('ND_green_swir1'));# //NDSI, MNDWI
    img = img.addBands(img.normalizedDifference(['green','swir2']).rename('ND_green_swir2'));

    img = img.addBands(img.normalizedDifference(['red','swir1']).rename('ND_red_swir1'));
    img = img.addBands(img.normalizedDifference(['red','swir2']).rename('ND_red_swir2'));

    img = img.addBands(img.normalizedDifference(['nir','red']).rename('ND_nir_red')); #//NDVI
    img = img.addBands(img.normalizedDifference(['nir','swir1']).rename('ND_nir_swir1')); #//NDWI, LSWI, -NDBI
    img = img.addBands(img.normalizedDifference(['nir','swir2']).rename('ND_nir_swir2')); #//NBR, MNDVI

    img = img.addBands(img.normalizedDifference(['swir1','swir2']).rename('ND_swir1_swir2'));

    # // Add ratios
    img = img.addBands(img.select('swir1').divide(img.select('nir')).rename('R_swir1_nir')); #//ratio 5/4
    img = img.addBands(img.select('red').divide(img.select('swir1')).rename('R_red_swir1')); #// ratio 3/5

    # // Add Enhanced Vegetation Index (EVI)
    evi = img.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'NIR': img.select('nir'),
      'RED': img.select('red'),
      'BLUE': img.select('blue')
    }).float();
    img = img.addBands(evi.rename('EVI'));

    # // Add Soil Adjust Vegetation Index (SAVI)
    # // using L = 0.5;
    savi = img.expression(
    '(NIR - RED) * (1 + 0.5)/(NIR + RED + 0.5)', {
      'NIR': img.select('nir'),
      'RED': img.select('red')
    }).float();
    img = img.addBands(savi.rename('SAVI'));
  
    # // Add Index-Based Built-Up Index (IBI)
    ibi_a = img.expression(
    '2*SWIR1/(SWIR1 + NIR)', {
      'SWIR1': img.select('swir1'),
      'NIR': img.select('nir')
    }).rename('IBI_A');
    ibi_b = img.expression(
    '(NIR/(NIR + RED)) + (GREEN/(GREEN + SWIR1))', {
      'NIR': img.select('nir'),
      'RED': img.select('red'),
      'GREEN': img.select('green'),
      'SWIR1': img.select('swir1')
    }).rename('IBI_B');
    ibi_a = ibi_a.addBands(ibi_b);
    ibi = ibi_a.normalizedDifference(['IBI_A','IBI_B']);
    img = img.addBands(ibi.rename('IBI'));

    return img

# ///////////////////////////////////////////////////////////////////////////////
# // Function to compute the Tasseled Cap transformation and return an image
# // with the following bands added: ['brightness', 'greenness', 'wetness', 
# // 'fourth', 'fifth', 'sixth']
def getTasseledCap(image,bands):
    
  # // Kauth-Thomas coefficients for Thematic Mapper data
    coefficients = ee.Array([
        [0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863],
        [-0.2848, -0.2435, -0.5436, 0.7243, 0.0840, -0.1800],
        [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572],
        [-0.8242, 0.0849, 0.4392, -0.0580, 0.2012, -0.2768],
        [-0.3280, 0.0549, 0.1075, 0.1855, -0.4357, 0.8085],
        [0.1084, -0.9022, 0.4120, 0.0573, -0.0251, 0.0238]
      ]);
  # // Make an Array Image, with a 1-D Array per pixel.
    arrayImage1D = image.select(bands).toArray();

  # // Make an Array Image with a 2-D Array per pixel, 6x1.
    arrayImage2D = arrayImage1D.toArray(1);

    componentsImage = ee.Image(coefficients)\
    .matrixMultiply(arrayImage2D)\
    .arrayProject([0])\
    .arrayFlatten([['brightness', 'greenness', 'wetness', 'fourth', 'fifth', 'sixth']]).float();

    return image.addBands(componentsImage);


# // Function to add Tasseled Cap angles and distances to an image.
# // Assumes image has bands: 'brightness', 'greenness', and 'wetness'.
def addTCAngles(image):
    # // Select brightness, greenness, and wetness bands
    brightness = image.select(['brightness']);
    greenness = image.select(['greenness']);
    wetness = image.select(['wetness']);

    # // Calculate Tasseled Cap angles and distances
    tcAngleBG = brightness.atan2(greenness).divide(math.pi).rename('tcAngleBG');
    tcAngleGW = greenness.atan2(wetness).divide(math.pi).rename('tcAngleGW');
    tcAngleBW = brightness.atan2(wetness).divide(math.pi).rename('tcAngleBW');
    tcDistBG = brightness.hypot(greenness).rename('tcDistBG');
    tcDistGW = greenness.hypot(wetness).rename('tcDistGW');
    tcDistBW = brightness.hypot(wetness).rename('tcDistBW');
    image = image.addBands(tcAngleBG).addBands(tcAngleGW)\
        .addBands(tcAngleBW).addBands(tcDistBG).addBands(tcDistGW)\
        .addBands(tcDistBW);
    return image

def addTassels(img, tcInputBands):
    img = getTasseledCap(img,tcInputBands)
    img = addTCAngles(img)
    return img

# // Function to add a prefix to all bands in an image
def renameBands(image,prefix):
    bandnames = image.bandNames();
    def addCat(band):
        band = ee.String(prefix).cat('_').cat(band);
        return band
  
    bandnames = bandnames.map(addCat)
    image = image.rename(bandnames);
    return image


def addTopography(img,region):
    elevation = ee.Image("JAXA/ALOS/AW3D30_V1_1").select('MED').rename('elevation')
    # // Import ALOS World 3D - 30m (AW3D30) global digital surface model (DSM) 
    # // Calculate slope, aspect, and hillshade
    topo = ee.Algorithms.Terrain(elevation);
    # topo = topo.clip(region);
    # // From aspect (a), calculate eastness (sin a), northness (cos a)
    deg2rad = ee.Number(math.pi).divide(180);
    aspect = topo.select('aspect');
    aspect_rad = aspect.multiply(deg2rad);
    eastness = aspect_rad.sin().rename('eastness').float();
    northness = aspect_rad.cos().rename('northness').float();
    # // Add topography bands to image
    topo = topo.select('elevation','slope','aspect').addBands(eastness).addBands(northness);
    img = img.addBands(topo);
    return img;

