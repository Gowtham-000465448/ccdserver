from flask import Flask,request, render_template
from flask_cors import CORS, cross_origin
from flask import Response
import os
from training_Validation_Insertion import train_validation
from trainingModel import trainModel

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
   try:
        if request.json['filepath'] is not None:            
            path = request.json['filepath']
            print(path)
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


   except ValueError:
     return Response("Error Occurred %s" % ValueError)
    
   except KeyError:
    return Response("Error Occurred2 %s" % KeyError)

   except Exception as e:
        return Response("Error Occurred3 %s" % e)

   return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == '__main__':
    app.run()

