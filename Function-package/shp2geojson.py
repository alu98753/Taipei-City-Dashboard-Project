from osgeo import gdal
from osgeo import ogr
import os

def shp2geojson_gdal(shp_file, geojson_file):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    src_ds = ogr.Open(shp_file)
    src_layer = src_ds.GetLayer(0)

    basename = os.path.basename(geojson_file)
    dst_driver = ogr.GetDriverByName('GeoJSON')
    dst_ds = dst_driver.CreateDataSource(geojson_file)
    if dst_ds.GetLayer(basename):
        dst_ds.DeleteLayer(basename)
    dst_layer = dst_ds.CreateLayer(basename, src_layer.GetSpatialRef())
    dst_layer.CreateFields(src_layer.schema)
    dst_feat = ogr.Feature(dst_layer.GetLayerDefn())

    for feature in src_layer:
        dst_feat.SetGeometry(feature.geometry())
        for j in range(feature.GetFieldCount()):
            dst_feat.SetField(j, feature.GetField(j))
        dst_layer.CreateFeature(dst_feat)

    del dst_ds
    del src_ds
    print("successfully convert shapefile to geojson")

if __name__ == '__main__':
    shp2geojson_gdal('D:\TaipeiProgramming\parking_lot_OutOfRoad\park05_202405021642.shp', 'D:\TaipeiProgramming\parking_lot_OutOfRoad\poking_lot.geojson')