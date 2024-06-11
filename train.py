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

First_collection = tfeats.f
Second_collection = tfeats.s

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
    assert First_collection.first().bandNames().getInfo() == [
        "blue",
        "green",
        "red",
        "nir",
        "swir1",
        "swir2",
        "date",
        "year",
        "TDOMMask",
        "cloudMask",
        "count",
        "temp",
        "ND_blue_green",
        "ND_blue_red",
        "ND_blue_nir",
        "ND_blue_swir1",
        "ND_blue_swir2",
        "ND_green_red",
        "ND_green_nir",
        "ND_green_swir1",
        "ND_green_swir2",
        "ND_red_swir1",
        "ND_red_swir2",
        "ND_nir_red",
        "ND_nir_swir1",
        "ND_nir_swir2",
        "ND_swir1_swir2",
        "R_swir1_nir",
        "R_red_swir1",
        "EVI",
        "SAVI",
        "IBI",
        "brightness",
        "greenness",
        "wetness",
        "fourth",
        "fifth",
        "sixth",
        "tcAngleBG",
        "tcAngleGW",
        "tcAngleBW",
        "tcDistBG",
        "tcDistGW",
        "tcDistBW",
    ]
    assert training.first().getInfo() == {
        "type": "Feature",
        "geometry": None,
        "id": "0_0_000061eb44495ba2d582_0",
        "properties": {
            "First_EVI": 0.7114313244819641,
            "First_IBI": 0.08247651904821396,
            "First_ND_blue_green": -0.20219579339027405,
            "First_ND_blue_nir": -0.651199996471405,
            "First_ND_blue_red": -0.3418867886066437,
            "First_ND_blue_swir1": -0.6936050653457642,
            "First_ND_blue_swir2": -0.5809707045555115,
            "First_ND_green_nir": -0.517089307308197,
            "First_ND_green_red": -0.15006467700004578,
            "First_ND_green_swir1": -0.5715683102607727,
            "First_ND_green_swir2": -0.4291920065879822,
            "First_ND_nir_red": 0.39790043234825134,
            "First_ND_nir_swir1": -0.07733571529388428,
            "First_ND_nir_swir2": 0.11296845227479935,
            "First_ND_red_swir1": -0.46104881167411804,
            "First_ND_red_swir2": -0.2983425557613373,
            "First_ND_swir1_swir2": 0.18865598738193512,
            "First_R_red_swir1": 0.36887967586517334,
            "First_R_swir1_nir": 1.1676356792449951,
            "First_SAVI": 0.5967496037483215,
            "First_TDOMMask": 10000,
            "First_blue": 436,
            "First_brightness": 3421.535400390625,
            "First_cloudMask": 10000,
            "First_count": 32767,
            "First_date": 32767,
            "First_fifth": 651.4462890625,
            "First_fourth": -3.279099941253662,
            "First_green": 657,
            "First_greenness": 633.8825073242188,
            "First_nir": 2064,
            "First_red": 889,
            "First_sixth": -82.28780364990234,
            "First_stdDev": 1032.734245526422,
            "First_swir1": 2410,
            "First_swir2": 1645,
            "First_tcAngleBG": 0.058309804610394325,
            "First_tcAngleBW": -0.11363630573458026,
            "First_tcAngleGW": -0.353255659000736,
            "First_tcDistBG": 3479.75732421875,
            "First_tcDistBW": 3651.781005859375,
            "First_tcDistGW": 1424.9234619140625,
            "First_temp": 2947,
            "First_wetness": -1276.166015625,
            "First_year": 32767,
            "Second_EVI": 0.8117160201072693,
            "Second_IBI": 0.08165662735700607,
            "Second_ND_blue_green": -0.17409588396549225,
            "Second_ND_blue_nir": -0.6423889398574829,
            "Second_ND_blue_red": -0.30502477288246155,
            "Second_ND_blue_swir1": -0.6877583265304565,
            "Second_ND_blue_swir2": -0.5875682234764099,
            "Second_ND_green_nir": -0.527260422706604,
            "Second_ND_green_red": -0.13827160000801086,
            "Second_ND_green_swir1": -0.5835322141647339,
            "Second_ND_green_swir2": -0.4605873227119446,
            "Second_ND_nir_red": 0.4195782244205475,
            "Second_ND_nir_swir1": -0.08127928525209427,
            "Second_ND_nir_swir2": 0.08805789798498154,
            "Second_ND_red_swir1": -0.48434004187583923,
            "Second_ND_red_swir2": -0.3442389667034149,
            "Second_ND_swir1_swir2": 0.16813381016254425,
            "Second_R_red_swir1": 0.34740015864372253,
            "Second_R_swir1_nir": 1.1769400835037231,
            "Second_SAVI": 0.6292682886123657,
            "Second_TDOMMask": 10000,
            "Second_blue": 491,
            "Second_brightness": 3741.659912109375,
            "Second_cloudMask": 10000,
            "Second_count": 32767,
            "Second_date": 32767,
            "Second_fifth": 766.4069213867188,
            "Second_fourth": -60.436798095703125,
            "Second_green": 698,
            "Second_greenness": 705.0335083007812,
            "Second_nir": 2255,
            "Second_red": 922,
            "Second_sixth": -89.06909942626953,
            "Second_stdDev": 1109.0542168118075,
            "Second_swir1": 2654,
            "Second_swir2": 1890,
            "Second_tcAngleBG": 0.059283397422198104,
            "Second_tcAngleBW": -0.11911804418915202,
            "Second_tcAngleGW": -0.35760311991752125,
            "Second_tcDistBG": 3807.504638671875,
            "Second_tcDistBW": 4019.863037109375,
            "Second_tcDistGW": 1629.831787109375,
            "Second_temp": 3056,
            "Second_wetness": -1469.44873046875,
            "Second_year": 32767,
            "aspect": 199,
            "change_abs": 0,
            "change_norm": 0,
            "eastness": -0.32556816935539246,
            "elevation": 1438,
            "land_class": 1,
            "max_extent": 0,
            "northness": -0.9455185532569885,
            "occurrence": 0,
            "recurrence": 0,
            "seasonality": 0,
            "slope": 14,
            "transition": 0,
        },
    }
