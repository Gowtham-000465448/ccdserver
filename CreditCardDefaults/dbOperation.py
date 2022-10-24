import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from logs.log_system import LoggerApp

class dbOperationDB:
    def __init__(self) :
        self.path='DB/'        
        self.filePath = "Training_Raw_files_validated/TrainingFiles"
        self.logger = LoggerApp()

    def intializeDBConnection(self,name):
        try:
            conn = sqlite3.connect(self.path+name+'.db')

            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % name)
            file.close()
        except ConnectionError:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self,name,column_names):
       
        try:
            conn = self.intializeDBConnection(name)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
                file = open("Training_Logs/Training_Log.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/Training_Log.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % name)
                file.close()

            else:

                for key in column_names.keys():
                    type = column_names[key]
                    
                    try:                       
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

                conn.close()

                file = open("Training_Logs/Training_Log.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/Training_Log.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % name)
                file.close()

        except Exception as e:
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/Training_Log.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % name)
            file.close()
            raise e

    def insertIntoTableGoodData(self,Database):
        
        conn = self.intializeDBConnection(Database)
        goodFilePath= self.filePath        
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Training_Logs/Training_Log.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                #self.logger.log(log_file," %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.logger.log(log_file,"Error while creating table: %s " % e)                
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()

        conn.close()
        log_file.close()


    def selectingDatafromtableintocsv(self,Database):
       

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/Training_Log.txt", 'a+')
        try:
            conn = self.intializeDBConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()