## Postfire vegetation monitoring system workflow

This repository holds the most production ready version of the Post [Fire Vegetation Moinitoring System](https://sig-gis.com/post-fire-vegetation-monitoring-system/) workflow and -in my general opinion- should be used over any JS alternatives. The workflow broadly relies on two files:

1. landsat_calfire.py
2. classification.ipynb

### landsat_calfire.py

This script produces the seasonal composites which are used in the classifier in (classification.ipynb). Currently, to export addditional composites minor editing is needed at the end of the script in the `if __name__ == "__main__"` section. Exporting in this section is controled by the function `export_composite`.

```
    export_composite(func, season, region, year, dry_run)

    Initializes an export of fall, summer, or both seasonal composites. 

    Args:
        func (class): The class that handels the preprocessing and compositing of Landsat imagery. 
        season (str): The season to export. Options are: 'Summer', 'Fall', 'both'
        region (ee.Geometery): The AOI to export.
        year (int): The year of the seasonal composite. 
        dry_run (bool, optional): Whether or not to export composites. If True images will not be exported. Defaults to True.
```
Example usage:
```python
studyArea = ee.FeatureCollection("users/TEST/CAFire/StudyAreas/finalStudyArea").geometry().bounds().buffer(5000)
funks = functions()
year = 2021
export_composite(funks, 'both',studyArea,year,True)
```