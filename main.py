# Guilherme Braga Pinto
# 18/04/2023
# My Github: https://github.com/gui1080
# Task: https://gist.github.com/saluker/85c3edfe0b680a5325318aa9e80686b7

from urllib import request
import shutil
import os
import csv
import json
import time

# All modules imported belong to the basic Python installation
# https://docs.python.org/3/contents.html

def main():

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

    recent_occur = "1970-01-01"
    final_data = ""

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

                    # checks for missing value
                    if str(row[5]) != "OBS_VALUE":
        
                        points.append([str(row[1]), float(row[5])])
                    
                    # if value is missing, append "0"
                    else:
                    
                        points.append([str(row[1]), float(0)])
                
                else:

                    # if new data should be added
                    if (str(row[0]) == current_REF_AREA) and (str(row[2]) == current_ENERGY_PRODUCT) and (str(row[3]) == current_FLOW_BREAKDOWN) and (str(row[4]) == current_UNIT_MEASURE) and (str(row[6]) == current_ASSESSMENT_CODE):
                        
                        # checks for missing value
                        if str(row[5]) != "OBS_VALUE":
        
                            points.append([str(row[1]), float(row[5])])
                        
                        # if value is missing, append "0"
                        else:
                    
                            points.append([str(row[1]), float(0)])
                        
                    
                    # If this is a new group of data
                    # display current group and start a new one!
                    else:

                        # Only thing left to do is show the JSON output!
                        # Sort the values by their time 
                        points.sort(key=lambda x: x[1])

                        # update the time format
                        # ISO 8601 requires date format to be "YYYY-MM-DD"
                        # But my data only has year and month
                        # I'll assume every occurence happens on day "01"

                        for i in range(len(points)):
                            points[i][0] = points[i][0] + "-01"
                            if points[i][0] > recent_occur and points[i][0] != "TIME_PERIOD-01":
                                recent_occur = points[i][0]

                        data_dict = {
                            "series_id": series_id, 
                            "points": points,
                            "fields": {
                                "ref_area": current_REF_AREA,
                                "en_product": current_ENERGY_PRODUCT, 
                                "flow_breakd": current_FLOW_BREAKDOWN, 
                                "unit": current_UNIT_MEASURE, 
                                "code": current_ASSESSMENT_CODE
                            }
                        }

                        print("\n")
                        print("---------------")
                        print(json.dumps(data_dict, indent=4))
                        print("---------------")

                        final_data = final_data + json.dumps(data_dict, indent=4)

                        # -----------------------------------------

                        # start new group
                        current_REF_AREA = str(row[0])
                        current_ENERGY_PRODUCT = str(row[2])
                        current_FLOW_BREAKDOWN = str(row[3])
                        current_UNIT_MEASURE = str(row[4])
                        current_ASSESSMENT_CODE = str(row[6])

                        series_id = current_REF_AREA + "//" + current_ENERGY_PRODUCT + "//" + current_FLOW_BREAKDOWN + "//" + current_UNIT_MEASURE + "//" + current_ASSESSMENT_CODE
                        
                        points = []

                        # checks for missing value
                        if str(row[5]) != "OBS_VALUE":

                            points.append([str(row[1]), float(row[5])])
                        
                        # if value is missing, append "0"
                        else:
                    
                            points.append([str(row[1]), float(0)])
                        
            else:

                first_occur = False

    print("Latest data")
    print(recent_occur)
    print("---------------")

    with open("result.json", "w+") as outfile:
        outfile.write(final_data)

#-------------------------------------------

if __name__ == '__main__':
    
    # contabiliza o tempo de execução!
    start = time.time()
    main()
    end = time.time()

    time_script = (end - start)/60
    print("\n\n\nEnd!\n\nScript duration: %f minutes." % time_script)