import ee

import train_features as tfeats

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

lc07 = defineClasses(tfeats.lc07,2007)
lc08 = defineClasses(tfeats.lc08,2008)
lc14 = defineClasses(tfeats.lc14,2014)

if __name__ == "__main__":
    # dev tests
    assert lc07.first().getInfo()['properties']['land_class'] == 0
    assert lc07.first().getInfo()['properties']['CCconifer'] >= 20