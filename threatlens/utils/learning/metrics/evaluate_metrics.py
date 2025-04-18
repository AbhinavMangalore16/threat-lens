from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger



import yaml
import logging
import os
import sys
import numpy as np
import pickle
import dill

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score


def model_evaluation(X_train, X_test, y_train, y_test, models, params, report_dir=None, report_file_name="model_evaluation_report.yaml"):
    try:
        logger.info("Starting model evaluation...")

        report_summary = {}
        model_m = list(models.values())
        model_n = list(models.keys())

        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
            logger.info(f"Saving consolidated report to {report_dir}")

        for m in range(len(models)):
            model = model_m[m]
            name = model_n[m]
            param = params.get(name, {})

            logger.info(f"Training model: {name}")
            rs = RandomizedSearchCV(model, param_distributions=param, n_iter=10, cv=3, verbose=2, n_jobs=-1)
            rs.fit(X_train, y_train)

            logger.info(f"Best parameters for {name}: {rs.best_params_}")
            model.set_params(**rs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = accuracy_score(y_train, y_train_pred)
            test_score = accuracy_score(y_test, y_test_pred)
            overfit_gap = abs(train_score - test_score)

            model_report = {
                "Train Accuracy": float(train_score),
                "Test Accuracy": float(test_score),
                "F1 Score": float(f1_score(y_test, y_test_pred, average='weighted')),
                "Precision": float(precision_score(y_test, y_test_pred, average='weighted')),
                "Recall": float(recall_score(y_test, y_test_pred, average='weighted')),
                "Overfitting Indicator": float(overfit_gap),
                "Best Parameters": rs.best_params_
            }

            report_summary[name] = model_report

        best_model_name, best_model_metrics = max(report_summary.items(), key=lambda item: item[1]['Test Accuracy'])

        final_report = {
            "models": report_summary,
            "best_model": {
                "name": best_model_name,
                "metrics": best_model_metrics
            }
        }

        if report_dir:
            full_path = os.path.join(report_dir, report_file_name)
            with open(full_path, 'w') as f:
                yaml.dump(final_report, f)
            logger.info(f"Final evaluation report saved to {full_path}")

        return report_summary

    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        raise ThreatLensException(e, sys)