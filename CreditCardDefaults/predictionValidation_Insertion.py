from datetime import datetime
from  logs import log_system
import os
from rawDataValidationPrediction import Raw_Data_validation
from dataTransformationPrediction import dataTransform
from dbOperationPrediction import dbOperationDB

class prediction_validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dbOperationDB()   
        self.cwd=os.getcwd()       
        self.file_object = open(self.cwd+"\Prediction_Logs\Prediction_Log.txt", 'a+')
        self.log_writer = log_system.LoggerApp()

    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Validation files for Training')
           
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            
            regex = self.raw_data.manualRegexCreation()
            
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            
            self.raw_data.validateColumnLength(noofcolumns)
           
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Data Validation Complete!!")

            self.log_writer.log(self.file_object, "Starting Data Transforamtion!!")

            self.dataTransform.replaceMissingWithNull()

            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")

            self.log_writer.log(self.file_object,
                                "Creating Training_Database and tables on the basis of given schema!!!")

            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "Table creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")

            # insert csv files in the table
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            #self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Prediction')

            self.file_object.close()

        except Exception as e:
            raise e









