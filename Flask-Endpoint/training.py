import pickle
from SmartRule import SvmModel
import pandas as pd
import numpy as np
from filter import filterNameToModels, save_filter_name_to_model_map_to_disk
import os.path
import flask

def predict_output(input_dict):
    input_pd = pd.DataFrame(data=input_dict, index=[0])
    # input_pd = pd.Series(input_dict).to_frame()
    result = {}

    for key in filterNameToModels.keys():
        print("Predicting for " + key)
        filter_model, canRun = filterNameToModels[key]
        if canRun:
            prediction = filter_model.predict(input_pd)
            result[key] = int(prediction[0])

    print(str(result))

    return result


def incremental_train_model(filterName, subject, body, output):

    if not (filterName in filterNameToModels):
        return 1

    # Append new record in data file.
    dataFile = "Training_Data/{0}-Data.csv".format(filterName)
    if not os.path.exists(dataFile):
        flask.abort(500, "Error: File not found " + dataFile)
        return

    # Clean input data
    body = body.replace("\n", "\\n")
    body = body.replace("\r", "\\r")
    body = body.replace(",", "")
    subject = subject.replace(",", "")

    # Append line to csv file.
    data_df = pd.read_csv(dataFile, encoding="utf-8")
    newRow = pd.DataFrame({
                "Subject" : [subject],
                "Body" : [body],
                "Output" : [output]
            })
    data_df = data_df.append(newRow, sort=False)
    data_df.to_csv(dataFile, encoding='utf-8', index=False)

    # Check if we can run model
    ones = len(data_df.query("Output==1").index)
    zeros = len(data_df.query("Output==0").index)
    if ones == 0 or zeros == 0:
        print("Not training.")
        return 1

    # Create new model and train.
    data_df = oversample_minority(data_df)
    new_model = SvmModel()
    features_df = data_df[["Subject", "Body"]]
    output_df = data_df["Output"].astype('int')
    print(features_df.head())
    print("Training.........")
    new_model.train(features_df, output_df)

    # Update new model in map.
    filterNameToModels[filterName] = [new_model, True]

    # Save model to disk.
    save_filter_name_to_model_map_to_disk()

    return 1


def oversample_minority(input_data):
    positive = len(input_data.query("Output==1").index)
    negative = len(input_data.query("Output==0").index)
    pos_ratio = positive / ( positive + negative)
    neg_ratio = negative / (positive + negative)
    if pos_ratio < 0.3:
        # multiply positive sample such that ratio wil be at 30%
        mult = 50 / (pos_ratio * 100)
        positive_records = input_data.query("Output==1")

        for x in range(int(mult)):
            input_data = input_data.append(positive_records)
    elif neg_ratio < 0.3:
        mult = 50 / (pos_ratio * 100)
        negative_records = input_data.query("Output==0")
        for x in range(int(mult)):
            input_data = input_data.append(negative_records)

    return input_data


#body = "2BHK available for Rent in Aparna Hill Park Lake Breeze,Hi\n\n \n\nA newly constructed furnished 2 BHK is available for rent in Chandanagar from March 5th .  \n\n \n\nExcellent view of lake garden swimming pool and the local area from the house itself. This could be one of the best view of about 72 Acres of lake right from the balcony. Open Ventilation for sunlight and air in all rooms including kitchen. \n\n \n\nPics of the house is available here <https://1drv.ms/f/s!AnYVI0nMGF6iyW1Nlb6GV9Oju-54> \n\n \n\n \n\nProperty Name\n\nAparna Hill Park Lake Breeze\n\nLocation\n\nAparna Lake Breeze Behind R. S. Brothers Chandanagar\n\nCarpet Area\n\n1295 SQFT\n\n# of Bedrooms\n\n2\n\n# of Bathrooms\n\n2 all western\n\n# Balcony\n\n1\n\nReserved Car Parking\n\n1 Closed parking\n\nBlock\n\nBlock I\n\nFloor\n\n3rd Floor\n\nFurnished State\n\nMedium Furnished\n\nAdditional Set up\n\n*  Modular Kitchen\n* Full wood work done in both bedrooms with wardrobes from top to down.\n*   1 King size bed in Master Bed room with Sleepwell mattress and dressing table\n*   Geyser in Master Bathroom\n*   Mosquito Mesh in all bed room and living room\n*   Internet Connection provision\n*   Fans in all rooms and living area\n*   LED Lights and bulbs in all places\n*  Split AC provision in both rooms\n*    Gas Connection available (Piped gas)\n\nWater\n\n24 hours Drinking and Bore water\n\nPower Backup\n\n* Inbuilt power backup for all power points except for AC and Geyser\n*  Inbuilt power backup for elevator common area lighting and water pumps\n\nProximity to Amenities\n\n*  2 km from main Mumbai highway road\n*  2 km from main R S Brothers\n* 3 km from the proposed Miyapur metro station\n*    12 km point to point from home to Financial District. \n*  3 km to Chandanagar railway Station\n* 4 km to Lingampally  railway station\n*    2.5 km to nearest hospital(s) grocery stores restaurants Schools pharmacy Shopping centers etc.\n* Multiple options of restaurants schools and grocery stores in close proximity.\n*  Vijetha store right outside the society.\n\nAmenities in Community\n\n*    Well Equipped Clubhouse\n* Full-size gym with trainers\n* Steam room\n*  Sauna room\n*  Community hall\n*  2 Swimming pools (large and medium)\n* Volleyball court\n*    Basketball court\n*    Tennis Court\n*    Community theatre/cinema hall (can accommodate 25 people). Just plug a USB and watch a movie on big screen\n*  Multiple Kids play area\n* 1 shuttle court\n* 1 open area stage and screening area\n*    Intercom facility in all flats\n*   In house Laundry service\n*   Naturals salon\n*  Free Shuttle operating from complex to Main road every 30 minutes throughout the day.\n\nSociety Maintenance\n\nNo Maintenance till May 2018. Post that Maintenance as per Society rules\n\nRent\n\n21000 INR per month\n\nAdvance\n\n2 Months\n\n \n\nPlease email or ping me or call me @ +1 425 209 6710.\n\n \n\nRegards\n\nDeepak\n\n"
#incremental_train_model({'Body':body, 'Subject': "flatmate required for vihanga", "Output": "1"})


