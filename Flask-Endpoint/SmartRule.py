import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import svm
import pickle
import os


############################### Data related methods #################################

def get_latest_training_data():
    subdir, dirs, files = os.walk('./')
    training_data_files = [file for file in files if file.startswith("SmartFiltersTrainingData-Hydchat")]


def read_data():
    raw_data = pd.read_csv("SmartFiltersTrainingData-HydChat.csv")

    # Replace Nan in output to 0.
    output_col = "Flats"
    raw_data = raw_data[["Subject", "Body", output_col]]
    raw_data = raw_data.rename(columns={output_col:"Output"})
    return raw_data


def clean_data(input_data):
    """
    :param input_data: Data frame with Subject, Body and Output columns.
    :return: Returns cleaned dataframe.
    This method replaces NaN with o or empty string.
    """
    input_data["Output"] = input_data["Output"].apply(lambda x: 0 if math.isnan(x) else x)
    input_data["Body"] = input_data["Body"].apply(lambda x: "" if x != x else x)
    return input_data


def oversample_minority(input_data):
    positive = len(input_data.query("Output==1").index)
    negative = len(input_data.query("Output==0").index)
    ratio = positive / ( positive + negative)
    if ratio > 0.5:
        pass

    # multiply positive sample such that ratio wil be at 30%
    mult = 50 / (ratio * 100)
    positive_records = input_data.query("Output==1")

    for x in range(int(mult)):
        input_data = input_data.append(positive_records)

    return input_data


def split_data(input_data):
    return train_test_split(input_data, test_size=0.33, shuffle=True)


def print_data_stats(input_data, prefix="Stats"):
    print("{0} : Number of samples = {1}".format(prefix, len(input_data.index)))
    print("{0} : Number of positive samples = {1}".format(prefix, len(input_data.query("Output==1").index)))
    print("{0} : Number of Negative samples = {1}".format(prefix, len(input_data.query("Output==0").index)))


def model_prediction_stats(actual, predictions):
    print(classification_report(actual, predictions))


def save_model(model):
    from SmartRule import SvmModel
    f = open("savedModels/model_v1.3.pkl", "wb")
    pickle.dump(model, f)
    f.close()


###################################### Model ###################################################


class BaseModel:
    """Model structure"""

    def train(self, features, output):
        pass

    def predict(self, features):
        pass


class NBModel(BaseModel):

    def __init__(self):
        self._cv = CountVectorizer()
        self._model = MultinomialNB()

    def train(self, features, output):
        body = features["Body"]
        encoded_x = self._cv.fit_transform(features["Body"])
        self._model.fit(encoded_x, np.ravel(output))

    def predict(self, features):
        encoded = self._cv.transform(features["Body"])
        return self._model.predict(encoded)


class SvmModel(BaseModel):

    def __init__(self):
        self._cv = CountVectorizer()
        self._tfidf = TfidfTransformer()
        self._model = svm.LinearSVC()


    def train(self, features, output):
        body = features["Body"]
        encoded_x = self._cv.fit_transform(body)
        encoded_x = self._tfidf.fit_transform(encoded_x)
        output = np.ravel(output)
        self._model.fit(encoded_x, output)

    def predict(self, features):
        body = features["Body"]
        encoded_x = self._cv.transform(body)
        encoded_x = self._tfidf.transform(encoded_x)
        return self._model.predict(encoded_x)


# adding other classifiers that are experimented


class RandomForestModel(BaseModel):
    def __init__(self):
        self._cv = TfidfVectorizer(['flats', 'flat', 'flatmate', 'flat for rent', 'flat sale'])
        self._model = RandomForestClassifier(max_leaf_nodes=1000)

    def train(self, features, output):
        body = features["Subject"]
        encoded_x = self._cv.fit_transform(body)
        output = np.ravel(output)
        self._model.fit(encoded_x, output)

    def predict(self, features):
        body = features["Subject"]
        encoded_x = self._cv.transform(body)
        return self._model.predict(encoded_x)


# SVM/Randomforeset models have performed better than K neighbors Model, keeping it for record


class KNeighborsModel(BaseModel):
    def __init__(self):
        self._cv = HashingVectorizer()
        self._model = KNeighborsClassifier()

    def train(self, features, output):
        body = features["Subject"]
        encoded_x = self._cv.fit_transform(body)
        output = np.ravel(output)
        self._model.fit(encoded_x, output)

    def predict(self, features):
        body = features["Subject"]
        encoded_x = self._cv.transform(body)
        return self._model.predict(encoded_x)


###################################### Main ###################################################


def train_model_from_file():
    # Read and clean data.
    data = read_data()
    data = clean_data(data)
    print_data_stats(data, "RawData")
    training_data, test_data = split_data(data)
    print_data_stats(training_data, "TrainingData")
    print_data_stats(test_data, "TestData")

    # Create and evaluate a model.
    training_data = oversample_minority(training_data)
    model = SvmModel()
    model.train(training_data[["Subject", "Body"]], training_data[["Output"]])
    predicted = model.predict(test_data[["Subject", "Body"]])
    model_prediction_stats(test_data["Output"], predicted)
    #save_model(model)


'''
Basic Naive Bayes mode accuracy. 

RawData : Number of samples = 4624
RawData : Number of positive samples = 702
RawData : Number of Negative samples = 3922
TrainingData : Number of samples = 3098
TrainingData : Number of positive samples = 469
TrainingData : Number of Negative samples = 2629
TestData : Number of samples = 1526
TestData : Number of positive samples = 233
TestData : Number of Negative samples = 1293
             precision    recall  f1-score   support

        0.0       0.97      0.91      0.94      1293
        1.0       0.62      0.83      0.71       233

avg / total       0.91      0.90      0.90      1526
'''

'''
SVM model accuracy 
Positive example accuracy increased from 0.62 to 0.73 but recall reduced 0.8 to 0.68 

RawData : Number of samples = 4624
RawData : Number of positive samples = 702
RawData : Number of Negative samples = 3922
TrainingData : Number of samples = 3098
TrainingData : Number of positive samples = 475
TrainingData : Number of Negative samples = 2623
TestData : Number of samples = 1526
TestData : Number of positive samples = 227
TestData : Number of Negative samples = 1299
             precision    recall  f1-score   support

        0.0       0.94      0.96      0.95      1299
        1.0       0.73      0.68      0.70       227

avg / total       0.91      0.92      0.91      1526


SVM model with over sampling(to reach 50% positive samples) 

RawData : Number of samples = 4624
RawData : Number of positive samples = 702
RawData : Number of Negative samples = 3922
TrainingData : Number of samples = 3098
TrainingData : Number of positive samples = 465
TrainingData : Number of Negative samples = 2633
TestData : Number of samples = 1526
TestData : Number of positive samples = 237
TestData : Number of Negative samples = 1289
             precision    recall  f1-score   support

        0.0       0.96      0.95      0.95      1289
        1.0       0.73      0.76      0.75       237

avg / total       0.92      0.92      0.92      1526

'''