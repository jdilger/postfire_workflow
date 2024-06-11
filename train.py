import ee

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
year_list = data.aggregate_array('Year').distinct()


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
