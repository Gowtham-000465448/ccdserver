
from sklearn.model_selection import train_test_split
from dataPreprocessing import Preprocessor
from clustering import KMeans,KMeansClustering,KneeLocator
from tuner import Model_Finder
from file_methods import File_Operation
from logs import log_system
import numpy as np
import pandas as pd
import os

#Creating the common Logging object


class prediction:

    def __init__(self):
        self.log_writer = log_system.LoggerApp()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')

    def getData(self):
        training_file='Prediction_FileFromDB/InputFile.csv'
        data=pd.read_csv(training_file)       
        return data

    def predictionModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Prediction')
        path="Prediction_Output_File/Predictions.csv"
        try:
            if os.path.exists('Prediction_Output_File/Predictions.csv'):
                os.remove('Prediction_Output_File/Predictions.csv')

            # Getting the data from the source
            data=self.getData()

            preprocessor = Preprocessor(self.file_object, self.log_writer)

            # check if missing values are present in the dataset
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            # if missing values are there, replace them appropriately.
            if (is_null_present):
                data = preprocessor.impute_missing_values(data, cols_with_missing_values)  # missing value imputation

            # Proceeding with more data pre-processing steps
            X = preprocessor.scale_numerical_columns(data)


            file_loader=File_Operation(self.file_object,self.log_writer)
            kmeans=file_loader.load_model('KMeans')


            clusters=kmeans.predict(X)#drops the first column for cluster prediction
            X['clusters']=clusters
            clusters=X['clusters'].unique()           
            for i in clusters:
                cluster_data= X[X['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result=(model.predict(cluster_data))

            final= result
            data["Predictions"]=final            
            data.to_csv(path,header=True,mode='a+') #appends result to prediction file
            self.log_writer.log(self.file_object,'End of Prediction')

            # logging the successful Training
            self.log_writer.log(self.file_object, 'Successful End of Prediction')
            self.file_object.close()
            return path

        except Exception as e:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Prediction')
            self.file_object.close()
            raise Exception