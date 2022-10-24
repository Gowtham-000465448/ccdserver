import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from logs.log_system import LoggerApp


class Raw_Data_validation:

   

    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = './schema_training.json'
        self.logger = LoggerApp()


    def valuesFromSchema(self):
        
        try:
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, self.schema_path)
            f = open(file_path)
            fileObj=json.load(f)    
            lengthOfDateStampInFile = fileObj['LengthOfDateStampInFile']
            lengthOfTimeStampInFile = fileObj['LengthOfTimeStampInFile']
            column_names = fileObj['ColName']
            numberofColumns = fileObj['NumberofColumns']

            """ file = open("Training_Logs/Training_Log.txt", 'a+')
            message ="LengthOfDateStampInFile:: %s" %lengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % lengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % numberofColumns + "\n"
            self.logger.log(file,message)
            file.close() """



        except ValueError:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return lengthOfDateStampInFile, lengthOfTimeStampInFile, column_names, numberofColumns


    def manualRegexCreation(self):
               
        regex = "['CreditCardPaymentHistory']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadRawData(self):

        
        try:
            path = os.path.join("Training_Raw_files_validated/", "TrainingFiles/")
            if not os.path.isdir(path):
                os.makedirs(path)            

        except OSError as ex:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def initializeTrainingFolder(self):       

        try:
            path = 'Training_Raw_files_validated/'           
            if os.path.isdir(path + 'TrainingFiles/'):
                shutil.rmtree(path + 'TrainingFiles/')
                file = open("Training_Logs/Training_Log.txt", 'a+')
                self.logger.log(file,"Directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    
   
    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
      
        self.initializeTrainingFolder()
        #create new directories
        self.createDirectoryForGoodBadRawData()
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, self.Batch_Directory)
        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy(file_path +"\\"+ filename, "Training_Raw_files_validated/TrainingFiles")
                            self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:                            
                            self.logger.log(f,"Invalid File Name :: %s" % filename)
                    else:                        
                        self.logger.log(f,"Invalid File Name :: %s" % filename)
                else:                    
                    self.logger.log(f, "Invalid File Name :: %s" % filename)

            f.close()

        except Exception as e:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e


    def validateColumnLength(self,NumberofColumns):
       
        try:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f,"Column Length Validation Started!!")
            for file in listdir('Training_Raw_files_validated/TrainingFiles/'):
                csv = pd.read_csv("Training_Raw_files_validated/TrainingFiles/" + file)
                if csv.shape[1] == NumberofColumns:
                    pass
                else:
                    if os.path.exists(file):
                        os.remove(file)
                    self.logger.log(f, "Invalid Column Length for the file!! File removed :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")
        except OSError:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()

    def validateMissingValuesInWholeColumn(self):
       
        try:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f,"Missing Values Validation Started!!")

            for file in listdir('Training_Raw_files_validated/TrainingFiles/'):
                csv = pd.read_csv("Training_Raw_files_validated/TrainingFiles/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        if os.path.exists(file):
                            os.remove(file)
                        self.logger.log(f,"Invalid Column for the file!! File removed :: %s" % file)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("Training_Raw_files_validated/TrainingFiles/" + file, index=None, header=True)
        except OSError:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()












