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

with open('jodi_gas_beta.csv', 'r') as csv_file:

    # every "row" in reader is a list
    # that contains the data of a certain row
    reader = csv.reader(csv_file)

    # first you sort by REF_AREA, and then by ENERGY_PRODUCT
    sortedFile = sorted(reader, key=lambda row:(row[0], row[2], row[3], row[4], row[6]))

    # read "readme.md" for a decent explanation of the
    # parsing logic
    '''
    for row in sortedFile:
        print(row)
    '''

    
#-------------------------------------------