from datetime import datetime,date

class LoggerApp:
    def __init__(self) -> None:
        pass
        
    def log(self,file_obj,message):
        self.now=datetime.now()
        self.date=date.today()
        self.time = self.now.strftime("%H:%M:%S")
        file_obj.write(
            str(self.date) + "/" + str(self.time) + "\t\t" + message +"\n")
