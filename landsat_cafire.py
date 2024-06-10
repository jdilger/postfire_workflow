# Sentinel-2 package

import ee
# from Py6S import *
import math
import datetime
import os, sys
from utils import *
import sun_angles
import view_angles
import time

PROJECT = "john-ee-282116"
#need auth_mode gcloud-legacy for exporting to legacy assets
# ee.Authenticate(force=True,auth_mode='gcloud-legacy') 
ee.Initialize()


class env(object):

    def __init__(self):
        """Initialize the environment."""

        # Initialize the Earth Engine object, using the authentication credentials.
        

        self.dem = ee.Image("JAXA/ALOS/AW3D30_V1_1").select(["AVE"])
        self.epsg = "EPSG:26910"
        self.dryRun = False

        ##########################################
        # variable for the landsat data request #
        ##########################################
        self.metadataCloudCoverMax = 80;

        ##########################################
        # Export variables		  		         #
        ##########################################

        self.assetId = "projects/earthengine-legacy/assets/users/TEST/CAFire/SeasonComposites/"
        self.name = "LS_"
        self.exportScale = 30

        ##########################################
        # variable for the shadowMask  algorithm #
        ##########################################

        # zScoreThresh: Threshold for cloud shadow masking- lower number masks out
        # less. Between -0.8 and -1.2 generally works well
        self.zScoreThresh = -0.8

        # shadowSumThresh: Sum of IR bands to include as shadows within TDOM and the
        # shadow shift method (lower number masks out less)
        self.shadowSumThresh = 0.35;

        # contractPixels: The radius of the number of pixels to contract (negative buffer) clouds and cloud shadows by. Intended to eliminate smaller cloud
        #    patches that are likely errors (1.5 results in a -1 pixel buffer)(0.5 results in a -0 pixel buffer)
        # (1.5 or 2.5 generally is sufficient)
        self.contractPixels = 1.5;

        # dilatePixels: The radius of the number of pixels to dilate (buffer) clouds
        # and cloud shadows by. Intended to include edges of clouds/cloud shadows
        # that are often missed (1.5 results in a 1 pixel buffer)(0.5 results in a 0 pixel buffer)
        # (2.5 or 3.5 generally is sufficient)
        self.dilatePixels = 3;

        ##########################################
        # variable for cloudScore  algorithm     #
        ##########################################

        # 9. Cloud and cloud shadow masking parameters.
        # If cloudScoreTDOM is chosen
        # cloudScoreThresh: If using the cloudScoreTDOMShift method-Threshold for cloud
        #    masking (lower number masks more clouds.  Between 10 and 30 generally works best)
        self.cloudScoreThresh = 10;

        # Percentile of cloud score to pull from time series to represent a minimum for
        # the cloud score over time for a given pixel. Reduces commission errors over
        # cool bright surfaces. Generally between 5 and 10 works well. 0 generally is a bit noisy
        self.cloudScorePctl = 8;
        self.hazeThresh = 250

        ##########################################
        # variable for terrain  algorithm        #
        ##########################################

        self.terrainScale = 600

        ##########################################
        # variable band selection  		         #
        ##########################################

        self.divideBands = ee.List(['blue', 'green', 'red', 'nir', 'swir1', 'swir2'])
        self.bandNamesLandsat = ee.List(
            ['blue', 'green', 'red', 'nir', 'swir1', 'temp', 'swir2', 'sr_atmos_opacity', 'pixel_qa', 'radsat_qa'])
        self.sensorBandDictLandsatSR = ee.Dictionary({'L8': ee.List(["SR_B3","SR_B4","SR_B5","SR_B6","SR_B7", "ST_B10", "SR_B7", "SR_QA_AEROSOL", "QA_PIXEL", "QA_RADSAT"]), \
                                                      'L7': ee.List([0, 1, 2, 3, 4, 5, 6, 7, 9, 10]), \
                                                      'L5': ee.List([0, 1, 2, 3, 4, 5, 6, 7, 9, 10]), \
                                                      'L4': ee.List([0, 1, 2, 3, 4, 5, 6, 7, 9, 10])})

        ##########################################
        # enable / disable modules 		         #
        ##########################################
        self.maskSR = True
        self.cloudMask = True
        self.hazeMask = True
        self.shadowMask = True
        self.brdfCorrect = True
        self.terrainCorrection = True



class functions():
    def __init__(self):
        """Initialize the Surfrace Reflectance app."""

        # get the environment
        self.env = env()

    def main(self, studyArea, startDate, endDate, startDay, endDay, week, regionName, **kwargs):

        self.env.startDate = startDate
        self.env.endDate = endDate

        self.env.startDoy = startDay
        self.env.endDoy = endDay
        self.regionName = regionName
        
        self.studyArea = studyArea
        if regionName == 'Fall':
            self.assetId = self.env.assetId + r'Fall_Full/'
        elif regionName == 'Summer':
            self.assetId = self.env.assetId + r'Summer_Full/'
        else:
            raise Exception("Season name must be either: Summer, Fall")
        
        if 'dryRun' in kwargs.keys():
            assert type(kwargs['dryRun']) is bool
            self.env.dryRun = kwargs['dryRun']
            
            if self.env.dryRun == True:
                runtype = 'dry run'
            else:
                runtype = 'live run'
            print(f'------------{runtype}-------------------')

        landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate(self.env.startDate,
                                                                           self.env.endDate).filterBounds(studyArea)
        landsat8 = landsat8.filterMetadata('CLOUD_COVER', 'less_than', self.env.metadataCloudCoverMax)
        landsat8 = landsat8.select(self.env.sensorBandDictLandsatSR.get('L8'), self.env.bandNamesLandsat)

        landsat5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').filterDate(self.env.startDate,
                                                                           self.env.endDate).filterBounds(studyArea)
        landsat5 = landsat5.filterMetadata('CLOUD_COVER', 'less_than', self.env.metadataCloudCoverMax)
        landsat5 = landsat5.select(self.env.sensorBandDictLandsatSR.get('L5'), self.env.bandNamesLandsat).map(
            self.defringe)

        landsat7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2').filterDate(self.env.startDate,
                                                                           self.env.endDate).filterBounds(studyArea)
        landsat7 = landsat7.filterMetadata('CLOUD_COVER', 'less_than', self.env.metadataCloudCoverMax)
        landsat7 = landsat7.select(self.env.sensorBandDictLandsatSR.get('L7'), self.env.bandNamesLandsat)

        landsat = landsat5.merge(landsat7).merge(landsat8)

        print('Number of imgs :',landsat.size().getInfo())
        if landsat.size().getInfo() > 0:

            # mask clouds using the QA band
            if self.env.maskSR == True:
                # print "removing clouds"
                landsat = landsat.map(self.CloudMaskSRL8)

            # mask clouds using cloud mask function
            if self.env.hazeMask == True:
                # print "removing haze"
                landsat = landsat.map(self.maskHaze)

            # mask clouds using cloud mask function
            if self.env.shadowMask == True:
                # print "shadow masking"
                self.fullCollection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterBounds(studyArea).select(
                    self.env.sensorBandDictLandsatSR.get('L8'), self.env.bandNamesLandsat)
                landsat = self.maskShadows(landsat)

            landsat = landsat.map(self.scaleLandsat).map(self.addDateYear)

            # mask clouds using cloud mask function
            if self.env.cloudMask == True:
                # print "removing some more clouds"
                landsat = landsat.map(self.maskClouds)

            if self.env.brdfCorrect == True:
                landsat = landsat.map(self.brdf)

            if self.env.terrainCorrection == True:
                landsat = ee.ImageCollection(landsat.map(self.terrain))

            print("calculating medoid")
            img = self.medoidMosaic(landsat)

            print("rescale")
            img = self.reScaleLandsat(img)

            print("set MetaData")
            img = self.setMetaData(img)

            print("exporting composite")
            self.exportMap(img, studyArea, week)


    def addDateYear(self, img):
        # add a date and year band
        date = ee.Date(img.get("system:time_start"))

        day = date.getRelative('day', 'year').add(1);
        yr = date.get('year');
        mk = img.mask().reduce(ee.Reducer.min());

        img = img.addBands(ee.Image.constant(day).mask(mk).uint16().rename('date'));
        img = img.addBands(ee.Image.constant(yr).mask(mk).uint16().rename('year'));

        return img;

    def CloudMaskSRL8(self, img):
        """apply cf-mask Landsat"""
        QA = img.select("pixel_qa")

        shadow = QA.bitwiseAnd(8).neq(0);
        cloud = QA.bitwiseAnd(32).neq(0);
        return img.updateMask(shadow.Not()).updateMask(cloud.Not()).copyProperties(img)
    def scaleLandsat(self, img):
        """Landsat is scaled using Collection 2 factors."""

        # Apply scaling and offset for optical bands
        optical_bands = img.select(self.env.divideBands).multiply(0.0000275).add(-0.2)
        # Apply scaling and offset for the thermal band
        thermal_band = img.select(ee.List(['temp'])).multiply(0.00341802).add(149.0)
        
        # Combine the scaled bands with the original TDOMMask
        scaled_image = img.select(['TDOMMask']).addBands(optical_bands).addBands(thermal_band)

        return scaled_image
 
    def reScaleLandsat(self, img):
        """Reverts the scaling applied to Landsat Collection 2 data."""
        # Define band names for optical and thermal bands
        optical_bands = self.env.divideBands
        thermal_band = ee.List(['temp'])
        
        # Reverse scaling and offset for optical bands
        optical_scaled = img.select(optical_bands).subtract(-0.2).divide(0.0000275)
        # Reverse scaling and offset for the thermal band
        thermal_scaled = img.select(thermal_band).subtract(149.0).divide(0.00341802)
        
        # Combine the rescaled bands and convert to int16
        rescaled_image = ee.Image(optical_scaled.addBands(thermal_scaled)).int16()

        return rescaled_image.copyProperties(img)
    def maskHaze(self, img):
        """ mask haze """
        opa = ee.Image(img.select(['sr_atmos_opacity']))
        haze = opa.gt(self.env.hazeThresh)
        return img.updateMask(haze.Not())

    def maskClouds(self, img):
        """
        Computes spectral indices of cloudyness and take the minimum of them.

        Each spectral index is fairly lenient because the group minimum
        is a somewhat stringent comparison policy. side note -> this seems like a job for machine learning :)
        originally written by Matt Hancher for Landsat imageryadapted to Sentinel by Chris Hewig and Ian Housman
        """

        score = ee.Image(1.0);
        # Clouds are reasonably bright in the blue band.
        blue_rescale = img.select('blue').subtract(ee.Number(0.1)).divide(ee.Number(0.3).subtract(ee.Number(0.1)))
        score = score.min(blue_rescale);

        # Clouds are reasonably bright in all visible bands.
        visible = img.select('red').add(img.select('green')).add(img.select('blue'))
        visible_rescale = visible.subtract(ee.Number(0.2)).divide(ee.Number(0.8).subtract(ee.Number(0.2)))
        score = score.min(visible_rescale);

        # Clouds are reasonably bright in all infrared bands.
        infrared = img.select('nir').add(img.select('swir1')).add(img.select('swir2'))
        infrared_rescale = infrared.subtract(ee.Number(0.3)).divide(ee.Number(0.8).subtract(ee.Number(0.3)))
        score = score.min(infrared_rescale);

        # Clouds are reasonably cool in temperature.
        temp_rescale = img.select('temp').subtract(ee.Number(300)).divide(ee.Number(290).subtract(ee.Number(300)))
        score = score.min(temp_rescale);

        # However, clouds are not snow.
        ndsi = img.normalizedDifference(['green', 'swir1']);
        ndsi_rescale = ndsi.subtract(ee.Number(0.8)).divide(ee.Number(0.6).subtract(ee.Number(0.8)))
        score = score.min(ndsi_rescale).multiply(100).byte();
        mask = score.lt(self.env.cloudScoreThresh).rename(['cloudMask']);
        img = img.updateMask(mask).addBands([mask]);

        return img;

    def maskShadows(self, collection):

        def TDOM(image):
            zScore = image.select(shadowSumBands).subtract(irMean).divide(irStdDev)
            irSum = image.select(shadowSumBands).reduce(ee.Reducer.sum())
            TDOMMask = zScore.lt(self.env.zScoreThresh).reduce(ee.Reducer.sum()).eq(2) \
                .And(irSum.lt(self.env.shadowSumThresh)).Not()
            TDOMMask = TDOMMask.focal_min(self.env.contractPixels).focal_max(self.env.dilatePixels).rename(['TDOMMask'])

            image = image.addBands([TDOMMask])

            return image.updateMask(TDOMMask)

        shadowSumBands = ['nir', 'swir1']

        # Get some pixel-wise stats for the time series
        irStdDev = self.fullCollection.select(shadowSumBands).reduce(ee.Reducer.stdDev())
        irMean = self.fullCollection.select(shadowSumBands).reduce(ee.Reducer.mean())

        # Mask out dark dark outliers
        collection_tdom = collection.map(TDOM)

        return collection_tdom

    def terrain(self, img):

        degree2radian = 0.01745;
        otherBands = img.select(['temp', 'date', 'year', 'TDOMMask', 'cloudMask'])

        def topoCorr_IC(img):
            dem = self.env.dem

            # Extract image metadata about solar position
            solar_zenith_angle = ee.Number(90).subtract(ee.Number(img.get('SUN_ELEVATION')))
            SZ_rad = ee.Image.constant(solar_zenith_angle).multiply(degree2radian).clip(
                img.geometry().buffer(10000));
            SA_rad = ee.Image.constant(ee.Number(img.get('SUN_AZIMUTH'))).multiply(degree2radian).clip(
                img.geometry().buffer(10000));

            # Creat terrain layers
            slp = ee.Terrain.slope(dem).clip(img.geometry().buffer(10000));
            slp_rad = ee.Terrain.slope(dem).multiply(degree2radian).clip(img.geometry().buffer(10000));
            asp_rad = ee.Terrain.aspect(dem).multiply(degree2radian).clip(img.geometry().buffer(10000));

            # Calculate the Illumination Condition (IC)
            # slope part of the illumination condition
            cosZ = SZ_rad.cos();
            cosS = slp_rad.cos();
            slope_illumination = cosS.expression("cosZ * cosS", \
                                                 {'cosZ': cosZ, 'cosS': cosS.select('slope')});

            # aspect part of the illumination condition
            sinZ = SZ_rad.sin();
            sinS = slp_rad.sin();
            cosAziDiff = (SA_rad.subtract(asp_rad)).cos();
            aspect_illumination = sinZ.expression("sinZ * sinS * cosAziDiff", \
                                                  {'sinZ': sinZ, \
                                                   'sinS': sinS, \
                                                   'cosAziDiff': cosAziDiff});

            # full illumination condition (IC)
            ic = slope_illumination.add(aspect_illumination);

            # Add IC to original image
            img_plus_ic = ee.Image(img.addBands(ic.rename(['IC'])).addBands(cosZ.rename(['cosZ'])).addBands(
                cosS.rename(['cosS'])).addBands(slp.rename(['slope'])));

            return ee.Image(img_plus_ic);

        def topoCorr_SCSc(img):
            img_plus_ic = img;
            mask1 = img_plus_ic.select('nir').gt(-0.1);
            mask2 = img_plus_ic.select('slope').gte(5) \
                .And(img_plus_ic.select('IC').gte(0)) \
                .And(img_plus_ic.select('nir').gt(-0.1));

            img_plus_ic_mask2 = ee.Image(img_plus_ic.updateMask(mask2));

            bandList = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'];  # Specify Bands to topographically correct

            def applyBands(image):
                blue = apply_SCSccorr('blue').select(['blue'])
                green = apply_SCSccorr('green').select(['green'])
                red = apply_SCSccorr('red').select(['red'])
                nir = apply_SCSccorr('nir').select(['nir'])
                swir1 = apply_SCSccorr('swir1').select(['swir1'])
                swir2 = apply_SCSccorr('swir2').select(['swir2'])
                return replace_bands(image, [blue, green, red, nir, swir1, swir2])

            def apply_SCSccorr(band):
                method = 'SCSc';

                out = ee.Image(1).addBands(img_plus_ic_mask2.select('IC', band)).reduceRegion(
                    reducer=ee.Reducer.linearRegression(2, 1), \
                    geometry=ee.Geometry(img.geometry().buffer(-5000)), \
                    scale=self.env.terrainScale, \
                    bestEffort=True,
                    maxPixels=1e10)

                # out_a = ee.Number(out.get('scale'));
                # out_b = ee.Number(out.get('offset'));
                # out_c = ee.Number(out.get('offset')).divide(ee.Number(out.get('scale')));

                fit = out.combine({"coefficients": ee.Array([[1], [1]])}, False);

                # Get the coefficients as a nested list,
                # cast it to an array, and get just the selected column
                out_a = (ee.Array(fit.get('coefficients')).get([0, 0]));
                out_b = (ee.Array(fit.get('coefficients')).get([1, 0]));
                out_c = out_a.divide(out_b)

                # apply the SCSc correction
                SCSc_output = img_plus_ic_mask2.expression("((image * (cosB * cosZ + cvalue)) / (ic + cvalue))", {
                    'image': img_plus_ic_mask2.select([band]),
                    'ic': img_plus_ic_mask2.select('IC'),
                    'cosB': img_plus_ic_mask2.select('cosS'),
                    'cosZ': img_plus_ic_mask2.select('cosZ'),
                    'cvalue': out_c});

                return ee.Image(SCSc_output);

            # img_SCSccorr = ee.Image([apply_SCSccorr(band) for band in bandList]).addBands(img_plus_ic.select('IC'));
            img_SCSccorr = applyBands(img).select(bandList).addBands(img_plus_ic.select('IC'))

            bandList_IC = ee.List([bandList, 'IC']).flatten();

            img_SCSccorr = img_SCSccorr.unmask(img_plus_ic.select(bandList_IC)).select(bandList);

            return img_SCSccorr.unmask(img_plus_ic.select(bandList))

        img = topoCorr_IC(img)
        img = topoCorr_SCSc(img)

        return img.addBands(otherBands)

    def defringe(self, img):

        # threshold for defringing landsat5 and 7
        fringeCountThreshold = 279

        k = ee.Kernel.fixed(41, 41,
                            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]);

        m = ee.Image(img).mask().reduce(ee.Reducer.min())
        sum = m.reduceNeighborhood(ee.Reducer.sum(), k, 'kernel')
        mask = sum.gte(fringeCountThreshold)

        return img.updateMask(mask)

    def brdf(self, img):

        import sun_angles
        import view_angles

        def _apply(image, kvol, kvol0):
            blue = _correct_band(image, 'blue', kvol, kvol0, f_iso=0.0774, f_geo=0.0079, f_vol=0.0372)
            green = _correct_band(image, 'green', kvol, kvol0, f_iso=0.1306, f_geo=0.0178, f_vol=0.0580)
            red = _correct_band(image, 'red', kvol, kvol0, f_iso=0.1690, f_geo=0.0227, f_vol=0.0574)
            nir = _correct_band(image, 'nir', kvol, kvol0, f_iso=0.3093, f_geo=0.0330, f_vol=0.1535)
            swir1 = _correct_band(image, 'swir1', kvol, kvol0, f_iso=0.3430, f_geo=0.0453, f_vol=0.1154)
            swir2 = _correct_band(image, 'swir2', kvol, kvol0, f_iso=0.2658, f_geo=0.0387, f_vol=0.0639)
            return replace_bands(image, [blue, green, red, nir, swir1, swir2])

        def _correct_band(image, band_name, kvol, kvol0, f_iso, f_geo, f_vol):
            """fiso + fvol * kvol + fgeo * kgeo"""
            iso = ee.Image(f_iso)
            geo = ee.Image(f_geo)
            vol = ee.Image(f_vol)
            pred = vol.multiply(kvol).add(geo.multiply(kvol)).add(iso).rename(['pred'])
            pred0 = vol.multiply(kvol0).add(geo.multiply(kvol0)).add(iso).rename(['pred0'])
            cfac = pred0.divide(pred).rename(['cfac'])
            corr = image.select(band_name).multiply(cfac).rename([band_name])
            return corr

        def _kvol(sunAz, sunZen, viewAz, viewZen):
            """Calculate kvol kernel.
            From Lucht et al. 2000
            Phase angle = cos(solar zenith) cos(view zenith) + sin(solar zenith) sin(view zenith) cos(relative azimuth)"""

            relative_azimuth = sunAz.subtract(viewAz).rename(['relAz'])
            pa1 = viewZen.cos() \
                .multiply(sunZen.cos())
            pa2 = viewZen.sin() \
                .multiply(sunZen.sin()) \
                .multiply(relative_azimuth.cos())
            phase_angle1 = pa1.add(pa2)
            phase_angle = phase_angle1.acos()
            p1 = ee.Image(PI().divide(2)).subtract(phase_angle)
            p2 = p1.multiply(phase_angle1)
            p3 = p2.add(phase_angle.sin())
            p4 = sunZen.cos().add(viewZen.cos())
            p5 = ee.Image(PI().divide(4))

            kvol = p3.divide(p4).subtract(p5).rename(['kvol'])

            viewZen0 = ee.Image(0)
            pa10 = viewZen0.cos() \
                .multiply(sunZen.cos())
            pa20 = viewZen0.sin() \
                .multiply(sunZen.sin()) \
                .multiply(relative_azimuth.cos())
            phase_angle10 = pa10.add(pa20)
            phase_angle0 = phase_angle10.acos()
            p10 = ee.Image(PI().divide(2)).subtract(phase_angle0)
            p20 = p10.multiply(phase_angle10)
            p30 = p20.add(phase_angle0.sin())
            p40 = sunZen.cos().add(viewZen0.cos())
            p50 = ee.Image(PI().divide(4))

            kvol0 = p30.divide(p40).subtract(p50).rename(['kvol0'])

            return (kvol, kvol0)

        date = img.date()
        footprint = determine_footprint(img)
        (sunAz, sunZen) = sun_angles.create(date, footprint)
        (viewAz, viewZen) = view_angles.create(footprint)
        (kvol, kvol0) = _kvol(sunAz, sunZen, viewAz, viewZen)
        return _apply(img, kvol.multiply(PI()), kvol0.multiply(PI()))

    def medoidMosaic(self, collection):
        """ medoid composite with equal weight among indices """
        nImages = ee.ImageCollection(collection).select([0]).count().rename('count')
        bandNames = ee.Image(collection.first()).bandNames()
        otherBands = bandNames.removeAll(self.env.divideBands)

        others = collection.select(otherBands).reduce(ee.Reducer.mean()).rename(otherBands);

        collection = collection.select(self.env.divideBands)

        bandNumbers = ee.List.sequence(1, self.env.divideBands.length());

        median = ee.ImageCollection(collection).median()

        def subtractmedian(img):
            diff = ee.Image(img).subtract(median).pow(ee.Image.constant(2));
            return diff.reduce('sum').addBands(img);

        medoid = collection.map(subtractmedian)

        medoid = ee.ImageCollection(medoid).reduce(ee.Reducer.min(self.env.divideBands.length().add(1))).select(
            bandNumbers, self.env.divideBands);

        return medoid.addBands(others).addBands(nImages);

    def medianMosaic(self, collection):

        """ median composite """
        median = collection.select(medianIncludeBands).median();
        othersBands = bandNames.removeAll(medianIncludeBands);
        others = collection.select(otherBands).mean();

        return median.addBands(others)

    def setMetaData(self, img):

        img = ee.Image(img).set({'regionName': str(self.regionName),
                                 'startDOY': str(self.env.startDoy),
                                 'endDOY': str(self.env.endDoy),
                                 'assetId': str(self.env.assetId),
                                 'compositingMethod': 'medoid',
                                 'toaOrSR': 'SR',
                                 'epsg': str(self.env.epsg),
                                 'exportScale': str(self.env.exportScale),
                                 'shadowSumThresh': str(self.env.shadowSumThresh),
                                 'maskSR': str(self.env.maskSR),
                                 'cloudMask': str(self.env.cloudMask),
                                 'hazeMask': str(self.env.hazeMask),
                                 'shadowMask': str(self.env.shadowMask),
                                 'brdfCorrect': str(self.env.brdfCorrect),
                                 'terrainCorrection': str(self.env.terrainCorrection),
                                 'contractPixels': str(self.env.contractPixels),
                                 'dilatePixels': str(self.env.dilatePixels),
                                 'metadataCloudCoverMax': str(self.env.metadataCloudCoverMax),
                                 'cloudScorePctl': str(self.env.cloudScorePctl),
                                 'hazeThresh': str(self.env.hazeThresh),
                                 'terrainScale': str(self.env.terrainScale),
                                 'system:time_start': self.env.startDate})

        return img



    def exportMap(self, img, studyArea, week):

        geom = studyArea.getInfo();
        sd = str(self.env.startDate.getRelative('day', 'year').getInfo()).zfill(3);
        ed = str(self.env.endDate.getRelative('day', 'year').getInfo()).zfill(3);
        year = str(self.env.startDate.get('year').getInfo());
        regionName = self.regionName.replace(" ", '_') + "_"

        task_ordered = ee.batch.Export.image.toAsset(image=img,
                                                     description=self.env.name + regionName + year + sd + ed,
                                                     assetId=self.assetId + self.env.name + regionName + year + sd + ed,
                                                     region=geom['coordinates'],
                                                     maxPixels=1e13,
                                                     crs=self.env.epsg,
                                                     scale=self.env.exportScale)
        
        if self.env.dryRun:
            print('Image will export to :')
            print(self.env.assetId + self.env.name + regionName + year + sd + ed)
        else:
            print('order started')
            task_ordered.start()
        

def get_dates_season(seasonName:str, year_ee:ee.Date):
    if seasonName == 'Fall':
        startDay = 244
        endDay = 304
    elif seasonName == 'Summer':
        startDay = 182
        endDay = 243
    else:
        print("Season name was not correctly selected: Summer, Fall")
        return 1
    startDate = year_ee.advance(startDay, "day")
    endDate = year_ee.advance(endDay, "day")
    return startDay, endDay, startDate, endDate

def export_composite(func, season:str, region, year:int,dry_run:bool=True):
    '''Initializes an export of fall, summer, or both seasonal composites. 

    Args:
        func (class): The class that handels the preprocessing and compositing of Landsat imagery. 
        season (str): The season to export. Options are: 'Summer', 'Fall', 'both'
        region (ee.Geometery): The AOI to export.
        year (int): The year of the seasonal composite. 
        dry_run (bool, optional): Whether or not to export composites. If True images will not be exported. Defaults to True.
    '''
    startWeek = 1 #TODO don't really need startweek delete next time there is time
    year_ee = ee.Date(f"{str(year)}-01-01")
    season_options = ['Summer','Fall']
    if season in season_options:
        startDay, endDay, startDate, endDate = get_dates_season(season, year_ee)
        func.main(region, startDate, endDate, startDay, endDay, startWeek, season,dryRun=dry_run)
    elif season.lower() == 'both':
        for s in season_options:
                startDay, endDay, startDate, endDate = get_dates_season(s, year_ee)
                func.main(region, startDate, endDate, startDay, endDay, startWeek, s,dryRun=dry_run)


if __name__ == "__main__":
    # TODO date got lost somewhere need to set that up again...
    studyArea = ee.FeatureCollection("users/TEST/CAFire/StudyAreas/finalStudyArea").geometry().bounds().buffer(
            5000)
    funks = functions()
    year = 2022
    export_composite(funks, 'Summer',studyArea,year,False)
   