import pickle
from SmartRule import SvmModel
import os.path
import csv


filter_model_saved_file = "filter_models.pkl"
filterNameToModels = {}

# Public methods
def create_new_filter(input_dict):
    filter_name = input_dict["filterName"]
    if filter_name not in dict.keys(filterNameToModels):
        filterNameToModels[filter_name] = [SvmModel(), False]
        print("model create for "+filter_name)
        save_filter_name_to_model_map_to_disk()
        create_csv_file(filter_name)
    else:
        print("model already exists")
        return "exists"
    print("filter model map : "+str(filterNameToModels))
    return "success"


def list_filters():
    print(filterNameToModels.keys())
    return list(filterNameToModels.keys())

# Private methods
def create_csv_file(filter_name):
    file_name = "Training_Data"+"\\"+filter_name+"-Data.csv"
    data = [["Subject", "Body", "Output"]]
    file = open(file_name, 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(data)


def create_predefined_filters():
    create_hydchat_flats_predefined_filter()


def create_hydchat_flats_predefined_filter():
    hydChatEmailsModel = read_hyd_chat_emails_model()
    filterNameToModels['HydChat-FlatEmails'] = [hydChatEmailsModel, True]

def read_hyd_chat_emails_model():
    with open("model_v1.3.pkl", "rb") as model_bytes:
        return pickle.load(model_bytes)

def save_filter_name_to_model_map_to_disk():
    pickle.dump(filterNameToModels, open(filter_model_saved_file, "wb"))

def load_filter_name_to_model_map_from_disk():
    if not os.path.isfile(filter_model_saved_file):
        print("Could not find file " + filter_model_saved_file + " ignoring.")
        return

    with open(filter_model_saved_file, "rb") as model_bytes:
        loadedFilterNameToModelMap = pickle.load(model_bytes)
        for filterName, model in loadedFilterNameToModelMap.items():
            filterNameToModels[filterName] = model
        print("loaded filter models :"+str(filterNameToModels))


# Execute it when module is imported.
load_filter_name_to_model_map_from_disk()
create_predefined_filters()

