"""-------------------------------------------------------------------------------
Name:       Image Log Data Extraction
Purpose:    Data logs for the Imagery are stored on Lizardtech Server. Copy/download
            the logs from the server on to your local computer into a folder with the
            name that incldes the download date. The logs will be used to run the code
            and generate polygons. Lizardtech server does not have ArcGIS, hence the
            code needs to run where it can access ArcGIS software.

            Once the logs are processed archieve the folder containing logs.

Author:     malika

Created:    04/12/2015
Copyright:  (c) malika 2015
------------------------------------------------------------------------------"""

import arcpy
import os
import csv

imageGdb = r"C:\Users\malika\Documents\ArcGIS\ImageExtents.gdb"
imagery_template = r"C:\Users\malika\Documents\ArcGIS\Default.gdb\ImageryExtents"
dirpath = r"C:\Users\malika\Desktop\Tesera\Imagery\Compressed_logs"

def getAttributes(data, findAttribute):#defining a function to get attributes. Passing in the data string and findAttribute is the data that we need for the attributes.
    start = data.find(findAttribute)# First occurance of the attribute, position of the first letter of the attribute.
    result = ''# what needs to be returned
    if start != -1:# if the attribute is found
        end = data.find('&',start)# The end of the attribute that needs to be extracted.  Finds position of W
        result = data[start + len(findAttribute):end]# WIDTH=757&. Finds the length from Width to after =.Trying to extract 757
    return result

def craetePolygon(coordinates):

    inXmin = float(coordinates[0])
    inYmin = float(coordinates[1])
    inXmax = float(coordinates[2])
    inYmax = float(coordinates[3])

    pntLL = arcpy.Point(inXmin,inYmin)
    pntLR = arcpy.Point(inXmax, inYmin)
    pntUR = arcpy.Point(inXmax, inYmax)
    pntUL = arcpy.Point(inXmin, inYmax)

    array = arcpy.Array()

    # Create the bounding box
    array.add(pntLL)
    array.add(pntLR)
    array.add(pntUR)
    array.add(pntUL)

    #Create the polygon object
    polygon = arcpy.Polygon(array)
    array.removeAll()
    return polygon

#Iterating through the log files in the Folder
for filename in os.listdir(dirpath):

    #THE CSV READER OBJECT IS KIND OF LIKE A CURSOR. IT CAN BE USED AS A METHOD TO GO TO
    #   THE NEXT LINE. YOU CAN ALSO USE IT WITH A FOR LOOP.
    #CREATE CSV READER OBJECT AND RECOGNIZES SPACE DELIMITER
    filepath = os.path.join(dirpath, filename)

    linecounter = 0
    with open(filepath, 'r') as csvfile:
        print filename

        #THE CSV READER OBJECT IS KIND OF LIKE A CURSOR. IT CAN BE USED AS A METHOD TO GO TO
        #THE NEXT LINE. YOU CAN ALSO USE IT WITH A FOR LOOP.
        #CREATE CSV READER OBJECT AND RECOGNIZES SPACE DELIMITER
        csvReader = csv.reader(csvfile, delimiter=' ')
        for line in csvReader:
            linecounter = linecounter + 1
            if line[0] == '#Fields:':
                header = line
                break #BREAKS OUT OF THE LOOP. THE NEXT LINE WILL NOT BE EXECUTED.


        #READ HEADERS
        #WHILE READING IGNORE THE FIRST 3 LINES THAT START WITH # AND FOR THE 4TH LINE START AFTER "FIELDS:"
        #IGNORE THE FIRST LINE AFTER THE HEADER
        #TO MOVE THE FIELDS TO THE LEFT SO EVERYTHING ALINGS WITH THE DATA.
        if header != "":

            dateIndex = header.index("date")-1
            timeIndex = header.index("time")-1
            cipIndex = header.index("c-ip")-1
            dataIndex = header.index("cs-uri-query")-1

        #NEDD TO FIND THE BOUNDING BOX NUMBERS WITHIN THE "cs-uri-query" FIELD
        #MAKE AN EMPTY LIST AND LOOP THRUGH THE LINES TO GRAB VALUES.
        #loglist = []

            for row in csvReader:
                linecounter = linecounter + 1
                if not row[0].startswith('#'):
                    date = row[dateIndex]
                    time = row[timeIndex]
                    ip = row[cipIndex]
                    data = row[dataIndex]
                    width = row[dataIndex]
                    height = row[dataIndex]
                    layers = row[dataIndex]

                extents = getAttributes(data, 'BBOX=')
                coordinates = extents.split(',')

                #To find where epsg starts within the data string
                if extents != '': #checking to make sure the epsg data is there
                    try:
                        widthdata = getAttributes(data, 'WIDTH=')
                        heightdata = getAttributes(data, 'HEIGHT=')
                        layerdata = getAttributes(data, 'LAYERS=')
                        epsg = getAttributes(data, 'EPSG:')

                        if epsg == '':
                            epsg = getAttributes(data, 'EPSG%3A')
                            if epsg == '':
                                print'weird epsg'

                        sr = arcpy.SpatialReference(int(epsg))

                        #Check if the fc exists with the given EPSG
                        logextentsfc = "extents_" + epsg
                        fc = os.path.join(imageGdb, logextentsfc)


                        if arcpy.Exists(fc) != True:
                            arcpy.CreateFeatureclass_management(imageGdb, logextentsfc, "POLYGON", imagery_template, "DISABLED", "DISABLED", sr)



                        with arcpy.da.InsertCursor(fc, ["SHAPE@", "Date", "Time", "IP", "Width", "Height", "Layers"]) as cursor:

                            polygon = craetePolygon(coordinates)
                            cursor.insertRow([polygon, date, time, ip, widthdata, heightdata, layerdata])

                    #If the code breaks and fails will give the message for the error
                    except Exception:
                        e = sys.exc_info()[1]
                        print(e.args[0])
                        print row
                        pass#This tells the code to keep running after the error is reported



