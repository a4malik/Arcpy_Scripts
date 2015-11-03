import arcpy
import os

#VARIABLES

# SDE Location
sde_connection = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\00MALIKA@MERCATOR2_GIS_LOCAL.sde"
# Default Geodatabase
default_gdb_connection = r"C:\Users\malika\Documents\ArcGIS\Default.gdb"
# Reference to Spatial Coordinates file
spatial_ref_location = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 12N.prj"
# My Default work space, where the output will be saved
arcpy.env.workspace = default_gdb_connection
# Overwrites feature classes if one exists
arcpy.env.overwriteOutput=True 

if arcpy.Exists("point_fc"):
    arcpy.Delete_management("point_fc")

#STEP 1----CREATE A POINT FROM X AND Y COORDINATES

#MAKE EVENT (X AND Y) LAYER FILES
arcpy.MakeXYEventLayer_management("Point_Table", "x_point", "y_point", "point_Temp",spatial_ref_location, "")

#CREATE A POINT FEATURE CLASS FROM LAYER
arcpy.FeatureToPoint_management("point_temp", default_gdb_connection + "\point_fc",
                                "INSIDE")

#STEP 2----SELECT SURVEY PARCEL BASED ON THE POINT CREATED ABOVE

#FIRST MAKE A LAYER FROM FEATURE CLASS

#CREATE A LAYER
arcpy.MakeFeatureLayer_management(sde_connection + "\MERCATOR2.DBO.CADASTRAL_REFERENCE\MERCATOR2.DBO.SURVEY_PARCELS", "parcel_lyr")

#SELECT BY LOCATION
arcpy.SelectLayerByLocation_management('parcel_lyr', 'intersect', 'POINT_FC')

#CONVERT LAYER TO FEATURE CLASS
arcpy.CopyFeatures_management('parcel_lyr', 'selected_parcel')

#CONVERT TO FEATURE SET

print "Complete"

