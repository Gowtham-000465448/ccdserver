from datetime import datetime
from os import listdir
import pandas
from logs.log_system import LoggerApp


class dataTransform:

     
     def __init__(self):
          self.dataPath = "Prediction_Raw_files_validated/PredictionFiles"
          self.logger = LoggerApp()

     def replaceMissingWithNull(self):         

          log_file = open("Prediction_Logs/Prediction_Log.txt", 'a+')
          try:
               onlyfiles = [f for f in listdir(self.dataPath)]
               for file in onlyfiles:
                    data = pandas.read_csv(self.dataPath + "/" + file)
                    data.to_csv(self.dataPath + "/" + file, index=None, header=True)
                    self.logger.log(log_file, " %s: Quotes added successfully!!" % file)
               #log_file.write("Current Date :: %s" %date +"\t" + "Current time:: %s" % current_time + "\t \t" +  + "\n")
          except Exception as e:
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               #log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data Transformation failed because:: %s" % e + "\n")
               log_file.close()
          log_file.close()
