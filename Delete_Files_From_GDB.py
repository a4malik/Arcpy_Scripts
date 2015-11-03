#This script lists and deletes feature classes in a geodatabase.  It does not delete rasters or tables.
# It does not delte those inside a feature data set.


import arcpy  
arcpy.env.workspace = r"C:\Users\malika\Documents\ArcGIS\Default.gdb"

#this uses arcpy  to automatically create the list of FCs to be deleted.
for objFeatureClass in arcpy.ListFeatureClasses():  
    #this deletes the fc's one by one. 
    arcpy.Delete_management(objFeatureClass)
    print "deleted   " + objFeatureClass
