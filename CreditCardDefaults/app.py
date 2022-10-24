from flask import Flask, request, render_template,send_file
from flask_cors import CORS, cross_origin
from flask import Response
import os
from trainingValidation_Insertion import train_validation
from predictionValidation_Insertion import prediction_validation
from trainingModel import trainModel
from predictionModel import prediction
import xlsxwriter
from io import BytesIO

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/getProgress", methods=["GET"])
@cross_origin()
def getProgress():
    try:
        if request.args is not None:
            key = request.args.get("key")
            script_dir = os.path.dirname(__file__)
            log_path = ""
            if key == 'train':
                 log_path = script_dir+"\\"+"Training_Logs\\Training_Log.txt"
            else:
                log_path = script_dir+"\\"+"Prediction_Logs\\Prediction_Log.txt"

            f = open(log_path, "r")
            lines = f.readlines()
            return Response(lines)
    except Exception as e:
         return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:

        if request.form is not None:

            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, "Training_Batch_Files")

            files = request.files.getlist('file')

            for file in files:

                filename = file.filename
                file.save(os.path.join(file_path, filename))

            path = "Training_Batch_Files"

            log_path = script_dir+"\\"+"Training_Logs"
            db_path = script_dir+"\\"+"DB"

            log_file = log_path+"\\"+"Training_Log.txt"
            if os.path.exists(log_file):
                os.remove(log_file)

            if not os.path.isdir(log_path):
                os.makedirs(log_path)

            if not os.path.isdir(db_path):
                os.makedirs(db_path)

            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table

    except ValueError:
        return Response("Error Occurred %s" % ValueError)

    except KeyError:
        return Response("Error Occurred2 %s" % KeyError)

    except Exception as e:
        return Response("Error Occurred3 %s" % e)

    return Response("Training successfull!!")


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None:
            dirname = os.path.dirname(__file__)
            path = "Prediction_Batch_Files"
            file_path = os.path.join(dirname, path)

            log_path = dirname+"\\"+"Prediction_Logs"
            db_path = dirname+"\\"+"PredictionDB"
            log_file = log_path+"\\"+"Prediction_Log.txt"

            if os.path.exists(log_file):
                os.remove(log_file)

            if not os.path.isdir(log_path):
                os.makedirs(log_path)

            if not os.path.isdir(db_path):
                os.makedirs(db_path)

            files = request.files.getlist('file')

            for file in files:

                filename = file.filename
                file.save(os.path.join(file_path, filename))

            prediction_valObj = prediction_validation(
                path)  # object initialization
            prediction_valObj.prediction_validation()
            pred = prediction()
            # predicting for dataset present in database
            path = pred.predictionModel()
            
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return send_file(path,mimetype=mimetype)


    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

port = int(os.getenv("PORT", 5001))
if __name__ == '__main__':
    app.run()
