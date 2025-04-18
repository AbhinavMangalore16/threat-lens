from threatlens.entity.artifact_entity import TrainingMetricArtifact
from threatlens.exception.exception import ThreatLensException

import sys
import os
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def get_clf_metrics(y_true, y_pred)-> TrainingMetricArtifact:
    try:
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        accuracy = accuracy_score(y_true, y_pred)

        metric_artifact = TrainingMetricArtifact(
            f1_score=f1,
            precision_score=precision,
            recall_score=recall,
            accuracy_score=accuracy
        )
        return metric_artifact
        
    except Exception as e:
        raise ThreatLensException(e, sys)