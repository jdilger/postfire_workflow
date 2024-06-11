import ee
import ee.batch

import train_features as tfeats
import indices

ee.Initialize()


def defineClasses(fc: ee.FeatureCollection, yr: int):
    classDict = {
        "land_class": {
            "Evergreen Forest": 0,
            "Shrub/Scrub": 1,
            "Barren Land (Rock/Sand/Clay)": 2,
            "Developed": 3,
            "Grassland/Herbaceous": 4,
            "Open Water": 5,
            "Deciduous Forest": 6,
            "Woody Wetlands": 7,
        }
    }

    conifer = fc.filter(ee.Filter.gte("CCconifer", 20)).map(
        lambda f: f.set(
            "land_class", classDict["land_class"]["Evergreen Forest"], "Year", yr
        )
    )
    shrub = fc.filter(
        ee.Filter.And(ee.Filter.lt("CCconifer", 20), ee.Filter.gte("Cshrubs", 20))
    ).map(
        lambda f: f.set(
            "land_class", classDict["land_class"]["Shrub/Scrub"], "Year", yr
        )
    )
    barren = fc.filter(
        ee.Filter.And(ee.Filter.lt("CCconifer", 20), ee.Filter.lt("Cshrubs", 20))
    ).map(
        lambda f: f.set(
            "land_class",
            classDict["land_class"]["Barren Land (Rock/Sand/Clay)"],
            "Year",
            yr,
        )
    )
    return conifer.merge(shrub).merge(barren)


exportName = "CAFires_traning_data"

# ///////////////////////////////////////////////////////////////////////////////
# // STEP 1: DATA PREPARATION (USE CAUTION WHEN EDITING BELOW HERE)
# ///////////////////////////////////////////////////////////////////////////////

# // Settings
classFieldName = "land_class"
# // the attribute, column, with the land cover as integer.
classFieldType = "land_use_category"
# // the attribute, column, with the land cover as a string.
makeClassFieldName = False  # //identify if you need to build the ClassFieldName or not

# ////////////////////////////////////////////////////////////////////////////////
# // Load study area
studyArea = tfeats.studyArea

lc07 = defineClasses(tfeats.lc07, 2007)
lc08 = defineClasses(tfeats.lc08, 2008)
lc14 = defineClasses(tfeats.lc14, 2014)

_all_data = ee.FeatureCollection(
    [
        tfeats.vhr,
        tfeats.Developed,
        tfeats.conifer,
        tfeats.WoodyWetland,
        tfeats.blackoak,
        tfeats.water,
        tfeats.barren2,
        tfeats.deciduous,
        tfeats.ceo,
        tfeats.ceo2,
        tfeats.lc07,
        tfeats.lc08,
        tfeats.lc14,
    ]
).flatten()
data = _all_data.filter(
    # removes  developed (land class 3) and unknown (land class 8)
    # TODO: figure out what land class 8 is and remove upstream
    ee.Filter.And(ee.Filter.neq("land_class", 3), ee.Filter.neq("land_class", 8))
)

# //Only use year and the land class atrributes
data = data.select(["Year", classFieldName])


# images prior to 2022 are from collection 1 and have a different scaling factor than collection2
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

c2_threshold = 2021
First_collection = scale_by_collection_type(tfeats.f, c2_threshold)
Second_collection = scale_by_collection_type(tfeats.s, c2_threshold)

# ///////////////////////////////////////////////////////////////////////////////
# // CLASSIFICATION CODE
# ///////////////////////////////////////////////////////////////////////////////

# // define training variables
tcInputBands = ee.List(["blue", "green", "red", "nir", "swir1", "swir2"])
water = ee.Image("JRC/GSW1_0/GlobalSurfaceWater").mask(ee.Image(1))

# // Add common spectral indices
# // Add tasseled cap transformation, tasseled cap angles, and NDSV
First_collection = First_collection.map(indices.addIndices)
First_collection = First_collection.map(
    lambda img: indices.addTassels(img, tcInputBands)
)
Second_collection = Second_collection.map(indices.addIndices)
Second_collection = Second_collection.map(
    lambda img: indices.addTassels(img, tcInputBands)
)

# // Get list of unique years in data
year_list = data.aggregate_array("Year").distinct()


def create_training_by_year(
    yr: ee.Number,
    First_collection: ee.ImageCollection,
    Second_collection: ee.ImageCollection,
):
    yr = ee.Number(yr)

    #   // Get seasonal composites for year
    First_composite_yr = ee.Image(
        First_collection.filterDate(
            ee.Date.fromYMD(yr, 1, 1), ee.Date.fromYMD(yr, 12, 31)
        ).first()
    )
    Second_composite_yr = ee.Image(
        Second_collection.filterDate(
            ee.Date.fromYMD(yr, 1, 1), ee.Date.fromYMD(yr, 12, 31)
        ).first()
    )

    stdDevBands = ee.List(
        [
            "blue",
            "green",
            "red",
            "nir",
            "swir1",
            "temp",
            "swir2",
            "ND_nir_red",
            "ND_nir_swir2",
            "ND_green_swir1",
        ]
    )
    First_stdDevComposite = First_composite_yr.select(stdDevBands).reduce(
        ee.Reducer.stdDev()
    )
    Second_stdDevComposite = Second_composite_yr.select(stdDevBands).reduce(
        ee.Reducer.stdDev()
    )

    #   // Combine all bands with mask and count bands
    First_composite_yr = First_composite_yr.addBands(First_stdDevComposite)
    Second_composite_yr = Second_composite_yr.addBands(Second_stdDevComposite)

    #   // Prepare composites
    First_composite_yr = indices.renameBands(First_composite_yr, "First")
    Second_composite_yr = indices.renameBands(Second_composite_yr, "Second")

    #   // Combine composites
    composite_yr = First_composite_yr.addBands(Second_composite_yr).addBands(water)
    composite_yr = indices.addTopography(composite_yr, studyArea)

    #   // Get reference data for year
    data_yr = data.filter(ee.Filter.eq("Year", yr))

    #   // Sample values from composite at data points
    training_yr = composite_yr.sampleRegions(
        collection=data_yr, properties=[classFieldName], scale=30
    )

    return training_yr


training_list = year_list.map(
    lambda yr: create_training_by_year(
        yr, First_collection=First_collection, Second_collection=Second_collection
    )
)

training = ee.FeatureCollection(training_list).flatten()
training = training.map(lambda f: f.setGeometry(ee.Geometry.Point([0,0])))
dst = "CAFires_traning_data_dev_6_1_2024"
ee.batch.Export.table.toAsset(
    collection=training,
    description=dst,
    assetId=f"projects/sig-ee/PostFireVeg/{dst}"
).start()


if __name__ == "__main__":
    # dev tests

    assert lc07.first().getInfo()["properties"]["land_class"] == 0
    assert lc07.first().getInfo()["properties"]["CCconifer"] >= 20
    assert year_list.getInfo() == [2018, 2018, 2015, 2010, 2007, 2008, 2014]
    assert First_collection.first().bandNames().getInfo() == ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'temp', 'ND_blue_green', 'ND_blue_red', 'ND_blue_nir', 'ND_blue_swir1', 'ND_blue_swir2', 'ND_green_red', 'ND_green_nir', 'ND_green_swir1', 'ND_green_swir2', 'ND_red_swir1', 'ND_red_swir2', 'ND_nir_red', 'ND_nir_swir1', 'ND_nir_swir2', 'ND_swir1_swir2', 'R_swir1_nir', 'R_red_swir1', 'EVI', 'SAVI', 'IBI', 'brightness', 'greenness', 'wetness', 'fourth', 'fifth', 'sixth', 'tcAngleBG', 'tcAngleGW', 'tcAngleBW', 'tcDistBG', 'tcDistGW', 'tcDistBW']
    assert training.first().getInfo() == {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [0, 0]}, 'id': '0_0_000061eb44495ba2d582_0', 'properties': {'First_EVI': 0.20792044699192047, 'First_IBI': 0.08247651904821396, 'First_ND_blue_green': -0.20219579339027405, 'First_ND_blue_nir': -0.651199996471405, 'First_ND_blue_red': -0.3418867886066437, 'First_ND_blue_swir1': -0.6936050653457642, 'First_ND_blue_swir2': -0.5809707045555115, 'First_ND_green_nir': -0.517089307308197, 'First_ND_green_red': -0.15006467700004578, 'First_ND_green_swir1': -0.5715683102607727, 'First_ND_green_swir2': -0.4291920065879822, 'First_ND_nir_red': 0.39790043234825134, 'First_ND_nir_swir1': -0.07733571529388428, 'First_ND_nir_swir2': 0.11296845227479935, 'First_ND_red_swir1': -0.46104881167411804, 'First_ND_red_swir2': -0.2983425557613373, 'First_ND_swir1_swir2': 0.18865598738193512, 'First_R_red_swir1': 0.36887966804979255, 'First_R_swir1_nir': 1.1676356589147288, 'First_SAVI': 0.22161448001861572, 'First_blue': 0.0436, 'First_brightness': 0.34215354919433594, 'First_fifth': 0.0651446282863617, 'First_fourth': -0.0003279100055806339, 'First_green': 0.06570000000000001, 'First_greenness': 0.06338825076818466, 'First_nir': 0.2064, 'First_red': 0.0889, 'First_sixth': -0.008228779770433903, 'First_stdDev': 88.38534652818791, 'First_swir1': 0.24100000000000002, 'First_swir2': 0.1645, 'First_tcAngleBG': 0.058309803116990425, 'First_tcAngleBW': -0.11363630101807953, 'First_tcAngleGW': -0.3532556565836019, 'First_tcDistBG': 0.3479757606983185, 'First_tcDistBW': 0.36517810821533203, 'First_tcDistGW': 0.14249233901500702, 'First_temp': 294.7, 'First_wetness': -0.12761659920215607, 'Second_EVI': 0.23627211153507233, 'Second_IBI': 0.08165662735700607, 'Second_ND_blue_green': -0.17409588396549225, 'Second_ND_blue_nir': -0.6423889398574829, 'Second_ND_blue_red': -0.30502477288246155, 'Second_ND_blue_swir1': -0.6877583265304565, 'Second_ND_blue_swir2': -0.5875682234764099, 'Second_ND_green_nir': -0.527260422706604, 'Second_ND_green_red': -0.13827160000801086, 'Second_ND_green_swir1': -0.5835322141647339, 'Second_ND_green_swir2': -0.4605873227119446, 'Second_ND_nir_red': 0.4195782244205475, 'Second_ND_nir_swir1': -0.08127928525209427, 'Second_ND_nir_swir2': 0.08805789798498154, 'Second_ND_red_swir1': -0.48434004187583923, 'Second_ND_red_swir2': -0.3442389667034149, 'Second_ND_swir1_swir2': 0.16813381016254425, 'Second_R_red_swir1': 0.3474001507159005, 'Second_R_swir1_nir': 1.176940133037694, 'Second_SAVI': 0.24452733993530273, 'Second_blue': 0.049100000000000005, 'Second_brightness': 0.37416601181030273, 'Second_fifth': 0.07664068788290024, 'Second_fourth': -0.006043680012226105, 'Second_green': 0.0698, 'Second_greenness': 0.0705033466219902, 'Second_nir': 0.2255, 'Second_red': 0.0922, 'Second_sixth': -0.008906910195946693, 'Second_stdDev': 91.65316989183968, 'Second_swir1': 0.2654, 'Second_swir2': 0.189, 'Second_tcAngleBG': 0.05928339077620633, 'Second_tcAngleBW': -0.11911803272637615, 'Second_tcAngleGW': -0.3576031210226578, 'Second_tcDistBG': 0.38075047731399536, 'Second_tcDistBW': 0.401986300945282, 'Second_tcDistGW': 0.16298317909240723, 'Second_temp': 305.6, 'Second_wetness': -0.14694486558437347, 'aspect': 199, 'change_abs': 0, 'change_norm': 0, 'eastness': -0.32556816935539246, 'elevation': 1438, 'land_class': 1, 'max_extent': 0, 'northness': -0.9455185532569885, 'occurrence': 0, 'recurrence': 0, 'seasonality': 0, 'slope': 14, 'transition': 0}}
