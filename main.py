from sensor.exception import SensorException,sys
from sensor.logger import logging
import pandas as pd
import numpy as np
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.ml.model.estimator import TargetValueMapping,ModelResolver
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.utils.main_utils import load_object,read_yaml_file
import os,sys
import pandas as pd
import numpy as np


import uvicorn
from fastapi import FastAPI,File,UploadFile,Response
from sensor.constant.application import APP_HOST, APP_PORT
from uvicorn import run as app_run
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()
origins =['*']



#cross-origin Resource sharing (cors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"]) # to check the authentication on main page
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        training_pipeline = TrainingPipeline()
        
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
    


@app.get("/predict")
async def predict():
    try:
        #get data from user
        #convert data into dataframe
        #run prediction
        #return the result
        file_path= r'D:\Vaibhav_PC\Python\Project\SensorFault\aps_failure_training_set.csv'
        feature_drop= read_yaml_file(filepath=r'D:\Vaibhav_PC\Python\Project\SensorFault\config\schema.yaml')
        
        df=pd.read_csv(file_path)
        df= df.drop('class', axis=1)
        df.replace('na',np.NaN, inplace=True)
        
        
        df= df.drop(feature_drop["drop_columns"],axis=1)
        df=np.array(df.iloc[0]).reshape(1,-1)
        
        


        # df=df.iloc[0].values.reshape(1,-1)

    
        print(df.shape)
        
        Model_resolver =ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not Model_resolver.is_model_exists():
            return Response("Model is not available")
        best_model_path = Model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column']=y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        return Response("Prediction successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")





def main():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()

    except Exception as e:
        error_message = SensorException(e, sys)
        logging.info(error_message)
        raise error_message




if __name__ == '__main__':  #it will run progm on only this page other import will restrict
    
    try:
        uvicorn.run(app, host=APP_HOST, port=APP_PORT)
        
        
    except SensorException as e:
        print(e)
    



# if __name__ == '__main__':  #it will run progm on only this page other import will restrict
    
#     try:
#         train_pipeline = TrainingPipeline()
#         train_pipeline.run_pipeline()
        
        
#     except SensorException as e:
#         print(e)
