'''find rain data 3rd dekad march 1989-2019'''

import geopandas as gp
import numpy as np
import os
from osgeo import gdal
from shapely.geometry import Point
inputPath = 'C:/projects/wfp/rfb_blended_moz_dekad'
adminBoundariesPath = 'C:/projects/wfp/geoBoundaries-MOZ-ADM2.geojson'

def main():
    '''run the workflow'''
    # find files
    rainFileNames = findFiles()
    # get 95th percentile of all the data
    percentile95 = get95thPercentile(rainFileNames)
    # get the mean, per administrative area, for 3rd dekad March 2024
    gdf = pixelsToPoints('mozrfb202403d3.tif')
    adminAreasGdf = gp.GeoDataFrame.from_file(adminBoundariesPath)
    # spatial join
    adminWithData = adminAreasGdf.sjoin(gdf, how="inner", predicate='intersects')
    # get mean for each shapeName
    means = adminWithData.groupby(['shapeName'])['values'].mean()
    with open('C:/projects/wfp/outputs','w') as f:
        f.write('Task 1 95th percentile: {}'.format(percentile95))
        f.write('Task 2 means: {}'.format(means))

def pixelsToPoints(fileName):
    '''create points for every pixel in a geotif'''
    r = gdal.Open(os.path.join(inputPath,fileName))
    b = r.GetRasterBand(1)
    data = b.ReadAsArray()

    GT = list(r.GetGeoTransform())
    rasterXSize = r.RasterXSize
    rasterYSize = r.RasterYSize

    points = []
    values = []
    
    # translate each pixel location to coordinates
    for x in range(0,rasterXSize - 1):
        for y in range(0,rasterYSize - 1):
            X_geo = GT[0] + x * GT[1] + y * GT[2]
            Y_geo = GT[3] + x * GT[4] + y * GT[5]
            coord = Point(X_geo,Y_geo)
            value = data[y,x]
            if value < 0:
                value = 0

            points.append(coord)
            values.append(value)

    pointData = { 'values': values, 'geometry': points}
    gdf = gp.GeoDataFrame(pointData, crs="EPSG:4326")
    
    return gdf

def get95thPercentile(fileNames):
    '''open each rain data file and v stack'''
    rainFallMeasurements = []

    for file in fileNames:
        r = gdal.Open(os.path.join(inputPath,file))
        b = r.GetRasterBand(1)
        data = b.ReadAsArray()
        flatData = data.flatten()
        # remove negative values (probably no data)
        cleanData = [value for value in flatData.tolist() if value > 0]
        rainFallMeasurements.extend(cleanData)
        # clean up
        r = None
        b = None

    return np.percentile(rainFallMeasurements,95)

def findFiles():
    '''find file names for 3rd dekad march 1989-2019'''
    fileNames = []
    for file in os.listdir(inputPath):
        if 'd3' in file and int(file[6:10]) > 1988 and int(file[6:10]) < 2020:
            fileNames.append(file)
    return fileNames

if __name__ == '__main__':
    main()
