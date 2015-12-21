#IMPORT LIBRARIES
import arcpy
import os

#SET ENVIRONMENT VARIABLES
sde_connection = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\00MALIKA@MERCATOR2_GIS_LOCAL.sde"
default_gdb_connection = r"C:\Users\malika\Documents\ArcGIS\Default.gdb"
spatial_reference = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 12N.prj"
arcpy.env.workspace = default_gdb_connection
arcpy.env.overwriteOutput=True 

#INPUT
parcel = r"C:\Users\malika\Documents\ArcGIS\Default.gdb\survey_parcel" 

#CONVERT TO LAYER
arcpy.MakeFeatureLayer_management (parcel , "parcel_lyr")
arcpy.MakeFeatureLayer_management (sde_connection + r"\MERCATOR2.DBO.REFERENCE_DATA\MERCATOR2.DBO.ADDRESSES", "addr_lyr")

#SELECT BY LOCATION
arcpy.SelectLayerByLocation_management('addr_lyr', 'intersect', 'parcel_lyr')
#arcpy.CopyFeatures_management('addr_lyr', default_gdb_connection + r"\selected_addr")

#CONVERT TO FEATURE CLASS
feature_class = arcpy.CreateFeatureclass_management(
    "in_memory", "tempfc", "addr_lyr")
arcpy.CopyFeatures_management('addr_lyr', default_gdb_connection + r"\selected_addr")


#arcpy.FeatureSet(selected_addr)

print "Done"
