import arcpy
import os
import config

sde_connection = config.sde_connection
#default_gdb_connection = r"C:\Users\malika\Documents\ArcGIS\Default.gdb"
#arcpy.env.workspace = default_gdb_connection
arcpy.env.overwriteOutput=True 

#INPUTS - Address feature class and buffer distance
addr = arcpy.GetParameterAsText(0) 
distance = arcpy.GetParameterAsText(1)

#CONVERT TO LAYER
addressFC = os.path.join(sde_connection, config.address)
arcpy.MakeFeatureLayer_management (addressFC, "addr_lyr")

titleFC = os.path.join(sde_connection, config.title_parcel)
arcpy.MakeFeatureLayer_management (titleFC, "title_lyr")

spatial_reference = arcpy.Describe(titleFC).spatialReference

#TABLE VIEW
titles_table = os.path.join(sde_connection, config.owner_table)
arcpy.MakeTableView_management (titles_table, "table_titles")

#SELECT BY LOCATION
arcpy.SelectLayerByLocation_management("title_lyr", "WITHIN_A_DISTANCE", addr, distance, "NEW_SELECTION")
#arcpy.CopyFeatures_management('title_lyr', "in_memory/selected_title")

#TABLE JOIN TITLE PARCELS
owners_fl = arcpy.AddJoin_management ("title_lyr", "PID", "table_titles", "PID")
#arcpy.CopyFeatures_management("title_lyr", "tableTest")

#FORMAT THE TABLE TO A STANDARD FORMAT WE USE - EXPORT AS A RECORD SET
owners_table = arcpy.CreateTable_management("in_memory", "owners_table")

#ADD FIELDS TO THE TABLE
fields = [
   ("PID","TEXT"),
   ("owner_count","TEXT"),
   ("owner_name","TEXT"),
   ("owner_address","TEXT"),
   ("postal_code","TEXT"),
   ("province","TEXT")
]

for field in fields:
   arcpy.AddField_management(*(owners_table,) + field)

fieldList = arcpy.ListFields("title_lyr")
##for f in fieldList:
##    print f.name

#print titles_table


#print fieldList

icursor = arcpy.InsertCursor(owners_table)

for row in arcpy.SearchCursor(owners_fl):
    irow = icursor.newRow()
    icursor.insertRow(irow)
    owner_count = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_count")
    pid = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.PID")
    for x in range(1, int(owner_count)  + 1):
        ownerName = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_" + str (x))
        postalCode = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_" + str (x) + "_Postal_Code")
        province = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_" + str (x) + "_Province")

        ownerAddress = ""
        

        if x == 1:
            ownerAddress = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_" + str (x) + "__Address")

        else:
            ownerAddress = row.getValue("MERCATOR2.DBO.TITLED_OWNERS.Owner_" + str (x) + "_Address")
            
        irow = icursor.newRow()
        irow.setValue("PID", pid)
        irow.setValue("owner_name", ownerName)
        irow.setValue("owner_address", ownerAddress)
        irow.setValue("postal_code", postalCode)
        irow.setValue("province", province)
        icursor.insertRow(irow)
        
recordSet = arcpy.RecordSet(owners_table)
print arcpy.GetCount_management(recordSet)
arcpy.SetParameter(2, recordSet)

desc = arcpy.Describe(recordSet)
        #arcpy.AddMessage(desc.pjson)
print desc.pjson


