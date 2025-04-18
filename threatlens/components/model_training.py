from threatlens.entity.artifact_entity import DataTransformArtifact, ModelTrainingArtifact
from threatlens.entity.config_entity import ModelTrainingConfig
from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger
from threatlens.utils.mains.utils import read_yaml, write_yaml, save_numpy, save_pickle, load_numpy, load_pickle
from threatlens.utils.learning.model.classifier import ThreatLensModel
from threatlens.utils.learning.metrics.clf_metrics import get_clf_metrics
from threatlens.utils.learning.metrics.evaluate_metrics import model_evaluation

import os
import sys
import logging

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score
import xgboost as xgb
import lightgbm as lgb

class ModelTraining:
    def __init__(self, model_training_config: ModelTrainingConfig, data_transform_artifact: DataTransformArtifact):
        try:
            self.model_training_config = model_training_config
            self.data_transform_artifact = data_transform_artifact
        except Exception as e:
            raise ThreatLensException(e, sys)
    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Logistic Regression": LogisticRegression(),
            "AdaBoost": AdaBoostClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "Random Forest": RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "KNeighbors": KNeighborsClassifier(),
            "XGBoost": xgb.XGBClassifier(verbose=1),
            "LightGBM": lgb.LGBMClassifier(verbose=1)
        }

        parameters = {
            "Logistic Regression": {
                "penalty": ["l2"],
                # "C": [0.01, 0.1, 1, 10],
                # "solver": ["liblinear", "lbfgs"],
                # "max_iter": [100, 200]
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200],
                # "learning_rate": [0.01, 0.1, 1]
            },
            "Gradient Boosting": {
                "n_estimators": [100, 150],
                # "learning_rate": [0.05, 0.1],
                # "max_depth": [3, 5],
                # "subsample": [0.8, 1.0]
            },
            "Random Forest": {
                "n_estimators": [8,16,32,64,128],
                # "max_depth": [None, 10, 20],
                # "min_samples_split": [2, 5],
                # "min_samples_leaf": [1, 2]
            },
            "Decision Tree": {
                "criterion": ["gini", "entropy"],
                # "max_depth": [None, 10, 20],
                # "min_samples_split": [2, 5],
                # "min_samples_leaf": [1, 2]
            },
            "KNeighbors": {
                "n_neighbors": [3, 5, 7],
                # "weights": ["uniform", "distance"],
                # "algorithm": ["auto", "ball_tree", "kd_tree"]
            },
            "XGBoost": {
                "n_estimators": [100, 200],
                # "max_depth": [3, 5],
                # "learning_rate": [0.05, 0.1],
                # "subsample": [0.8, 1.0],
                # "colsample_bytree": [0.8, 1.0]
            },
            "LightGBM": {
                "n_estimators": [100, 200],
                # "max_depth": [3, 5],
                # "learning_rate": [0.05, 0.1],
                # "num_leaves": [31, 64],
                # "boosting_type": ["gbdt", "dart"]
            }
        }
        model_report:dict = model_evaluation(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=parameters, report_dir=self.model_training_config.model_training_report)
        best_model_score = max(model_report.values(), key=lambda x: x['Test Accuracy'])
        best_model_name = max(
            model_report.items(),
            key=lambda item: item[1]['Test Accuracy']
        )[0]
        best_model = models[best_model_name]    
        y_train_pred = best_model.predict(X_train)
        clf_train_metric = get_clf_metrics(y_train, y_train_pred)
        y_test_pred = best_model.predict(X_test)
        clf_test_metric = get_clf_metrics(y_test, y_test_pred)

        preprocessor = load_pickle(self.data_transform_artifact.transform_object_file_path)
        model_dir_path = os.path.dirname(self.model_training_config.model_trained_file_path)
        os.makedirs(model_dir_path, exist_ok = True)
        threatlens_model = ThreatLensModel(preprocessor=preprocessor, model=best_model)
        save_pickle(self.model_training_config.model_trained_file_path, threatlens_model)

        model_training_artifact = ModelTrainingArtifact(
            trained_model_file_path=self.model_training_config.model_trained_file_path,
            training_metric_artifact=clf_train_metric,
            testing_metric_artifact=clf_test_metric,
        )
        logging.info(f"Model training artifact: {model_training_artifact}")
        logging.info(f"Model training report: {model_report}")
        logging.info(f"Best model name: {best_model_name}")
        return model_training_artifact

    def init_model_training(self) -> ModelTrainingArtifact:
        try:
            train_file = self.data_transform_artifact.transform_train_file_path
            test_file = self.data_transform_artifact.transform_test_file_path
            training_array = load_numpy(train_file)
            testing_array = load_numpy(test_file)

            X_train, y_train, X_test, y_test = training_array[:, :-1], training_array[:, -1], testing_array[:, :-1], testing_array[:, -1]

            phishing_model = self.train_model(X_train, y_train, X_test, y_test)
            return phishing_model
        except Exception as e:
            raise ThreatLensException(e, sys)