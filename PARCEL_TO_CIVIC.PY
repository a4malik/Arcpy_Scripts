import arcpy
import os

sde_connection = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\00MALIKA@MERCATOR2_GIS_LOCAL.sde"
default_gdb_connection = r"C:\Users\malika\Documents\ArcGIS\Default.gdb"
spatial_reference = r"C:\Users\malika\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 12N.prj"
arcpy.env.workspace = default_gdb_connection
arcpy.env.overwriteOutput=True 

#INPUT
lld = '36\12\6175NY'

#CONVERT TO LAYER
arcpy.MakeFeatureLayer_management (sde_connection + r"\MERCATOR2.DBO.CADASTRAL_REFERENCE\MERCATOR2.DBO.SURVEY_PARCELS", "parcel_lyr")
arcpy.MakeFeatureLayer_management (sde_connection + r"\MERCATOR2.DBO.REFERENCE_DATA\MERCATOR2.DBO.ADDRESSES", "addr_lyr")

#SELECT BY ATTRIBUTES
arcpy.SelectLayerByAttribute_management ("parcel_lyr", "NEW_SELECTION", ("'[LEGAL]' = '" + lld + "'"))
arcpy.CopyFeatures_management('parcel_lyr', 'survey_parcel')

#SELECT BY LOCATION
arcpy.SelectLayerByLocation_management('addr_lyr', 'intersect', 'survey_parcel')
arcpy.CopyFeatures_management('addr_lyr', default_gdb_connection + r"\selected_addr")

print "Done"
