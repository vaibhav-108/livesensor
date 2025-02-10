from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from sensor.entity.config_entity import DataValidationConfig,TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig
from sensor.entity.config_entity import ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from sensor.constant import training_pipeline
from sensor.utils.main_utils import read_yaml_file,write_yaml_file,save_numpy_array_data,load_numpy_array_data
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_deployment import ModelPusher
from sensor.constant.training_pipeline import SAVED_MODEL_DIR


from sensor.cloud_storage.s3_syncer import S3Sync
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME



class TrainingPipeline:
    is_pipeline_running = False
    self.s3_sync=S3Sync()
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            # self.data_ingestion = DataIngestion(data_ingestion_config=self.training_pipeline_config.data_ingestion_config)
            # self.data_validation = DataValidation(data_validation_config=self.training_pipeline_config.data_validation_config)
            
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            logging.info("Reading data from config file")
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)    
            self.data_ingestion= DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            logging.info("Reading data from config file")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation= DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed and artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
        
        
    def start_data_Transformation(self,data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
        
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            logging.info("Starting model trainer")

            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model trainer completed and artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
        
  
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                 model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            logging.info("Starting model evaluation")

            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(data_validation_artifact=data_validation_artifact, 
                                               model_trainer_artifact=model_trainer_artifact,
                                               model_evaluation_config=model_evaluation_config)
                                               
            model_evaluation_artifact = model_evaluation.start_model_evaluation()
            logging.info("Model evaluation completed and artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
                           
        try:
            logging.info("Starting model pusher")

            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                       model_eval_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model pusher completed and artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    #to send directory to S3
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)

        
        
  


    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running = True
            self.s3_sync=S3Sync()
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_Transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                                                     model_trainer_artifact=model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)
            
            self.sync_artifact_dir_to_s3()
            self.syn_saved_model_dir_to_s3()
            
            TrainingPipeline.is_pipeline_running = False
            logging.info("Training pipeline completed")
           
        except Exception as e:
            self.sync_artifact_dir_to_s3()  #to raise the error
            TrainingPipeline.is_pipeline_running = False
            raise SensorException(e, sys)