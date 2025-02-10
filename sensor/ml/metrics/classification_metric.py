# it will check the accuracy score


from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sensor.exception import SensorException
from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score
import os,sys

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        model_accuracy_score = accuracy_score(y_true, y_pred)
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classsification_metric =  ClassificationMetricArtifact(
                    accuracy_score=model_accuracy_score,
                    f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classsification_metric
    except Exception as e:
        raise SensorException(e,sys)