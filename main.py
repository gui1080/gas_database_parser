# Guilherme Braga Pinto
# 18/04/2023
# https://github.com/gui1080

from urllib import request
import shutil
import os
import csv
import json

# All modules imported belong to the basic Python installation
# https://docs.python.org/3/contents.html

#-------------------------------------------
# check if csv file exists

file_exists = False

for diretory, folders, files in os.walk(os.path.dirname(__file__)):
    for file in files:
        if "jodi_gas_beta.csv" in files:
            file_exists = True
            break

#-------------------------------------------
# if It does not exists, download It

if file_exists == False:

    url = "https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip"

    # hardcoded url download
    #-------------------------------------------

    print("Starting file retrieval!")

    try:

        response = request.urlretrieve(url, "jodi_gas_csv_beta.zip")

    except:

        print("It was not possible to retrieve file from " + url) 

    finally:

        print("File retrieval over!")

    # check if file was downloaded properly
    #-------------------------------------------

    for diretory, folders, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            if "jodi_gas_csv_beta.zip" in files:
                print("Correct file exists!")
                break

    # unzip
    #-------------------------------------------

    print("Unzip file!")

    try:

        shutil.unpack_archive(os.path.dirname(__file__) + "/jodi_gas_csv_beta.zip", os.path.dirname(__file__)) 

    except:

        print("There was a problem unzipping the file!\n" + str(os.path.dirname(__file__)) + "/jodi_gas_csv_beta.zip")

    finally:

        print("End of unzip step!")

# read and parse downloaded csv file!
#-------------------------------------------

first_occur = True

current_REF_AREA = ""
current_ENERGY_PRODUCT = ""
current_FLOW_BREAKDOWN = ""
current_UNIT_MEASURE = ""
current_ASSESSMENT_CODE = ""

with open('jodi_gas_beta.csv', 'r') as csv_file:
        
    # every "row" in reader is a list
    # that contains the data of a certain row
    reader = csv.reader(csv_file)

    # first you sort by REF_AREA, and then by ENERGY_PRODUCT
    sortedFile = sorted(reader, key=lambda row:(row[0], row[2], row[3], row[4], row[6]))

    # read "readme.md" for a decent explanation of the
    # parsing logic
    
    for row in sortedFile:
        
        if first_occur != True:
            
            # if It is the first data to be analysed
            if current_REF_AREA == "":
            
                current_REF_AREA = str(row[0])
                current_ENERGY_PRODUCT = str(row[2])
                current_FLOW_BREAKDOWN = str(row[3])
                current_UNIT_MEASURE = str(row[4])
                current_ASSESSMENT_CODE = str(row[6])

                series_id = current_REF_AREA + "//" + current_ENERGY_PRODUCT + "//" + current_FLOW_BREAKDOWN + "//" + current_UNIT_MEASURE + "//" + current_ASSESSMENT_CODE
                
                points = []

                if str(row[5]) != "OBS_VALUE":
    
                    points.append([str(row[0]), float(row[5])])
                    
                else:
                
                    points.append([str(row[0]), float(0)])
                    
            
            else:

                # if new data should be added
                if (str(row[0]) == current_REF_AREA) and (str(row[2]) == current_ENERGY_PRODUCT) and (str(row[3]) == current_FLOW_BREAKDOWN) and (str(row[4]) == current_UNIT_MEASURE) and (str(row[6]) == current_ASSESSMENT_CODE):
                    
                    if str(row[5]) != "OBS_VALUE":
    
                        points.append([str(row[0]), float(row[5])])
                    
                    else:
                
                        points.append([str(row[0]), float(0)])
                    
                
                # If this is a new group of data
                # display current group and start a new one!
                else:

                    # display json!

                    print("\n---------------")
                    print(series_id)
                    print("---------------")
                    print(current_REF_AREA)
                    print(current_ENERGY_PRODUCT)
                    print(current_FLOW_BREAKDOWN)
                    print(current_UNIT_MEASURE)
                    print(current_ASSESSMENT_CODE)
                    print("\n")
                    print(points)
                    print("\n")
                    print("---------------")

                    print("\n")
                    print("\n")
                    print("---------------\nJSON")
                    # MOSTRA EM JSON AQUI
                    print("---------------")


                    # start new group
                    current_REF_AREA = str(row[0])
                    current_ENERGY_PRODUCT = str(row[2])
                    current_FLOW_BREAKDOWN = str(row[3])
                    current_UNIT_MEASURE = str(row[4])
                    current_ASSESSMENT_CODE = str(row[6])

                    series_id = current_REF_AREA + "//" + current_ENERGY_PRODUCT + "//" + current_FLOW_BREAKDOWN + "//" + current_UNIT_MEASURE + "//" + current_ASSESSMENT_CODE
                    
                    points = []

                    if str(row[5]) != "OBS_VALUE":

                        points.append([str(row[0]), float(row[5])])
                    
                    else:
                
                        points.append([str(row[0]), float(0)])
                    
        else:

            first_occur = False

#-------------------------------------------