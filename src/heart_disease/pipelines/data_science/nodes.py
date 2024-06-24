"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.5
"""
import logging
import wandb
import random
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, accuracy_score, precision_recall_curve, roc_curve, roc_auc_score


def split_data(data: pd.DataFrame):
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters_data_science.yml.
    Returns:
        Split data.
    """
    global label
    
    label = data.columns[1:]

    X = data.drop('HeartDisease', axis=1)  # 'HeartDisease' is the target column
    y = data['HeartDisease']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """

   
    model_rfc = RandomForestClassifier(n_estimators=100, random_state=42)
    model_rfc.fit(X_train, y_train)

    


    return model_rfc


def evaluate_model(random_forest_classifier: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series, X_train, y_train):
    """Calculates and logs the coefficient of determination.
    
    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    
    y_pred_rfc = random_forest_classifier.predict(X_test)
    score = accuracy_score(y_test, y_pred_rfc)
    logger = logging.getLogger(__name__)
    logger.info("Model has a coefficient prediction of %.3f on test data.", score)



    wandb.login(key="7cedcc8572677253cbaf3974533bf4979bb5e496")

    wandb.init(
        # set the wandb project where this run will be logged
        project="asi-grupa-6"
    )
    params = random_forest_classifier.get_params()
    n_estimators = params['n_estimators']
    wandb.log({"accuracy":score})
    wandb.log({"n_estimators":n_estimators})
    print("----------------------------------")
    print(label)

    y_pred = random_forest_classifier.predict(X_test)
    proba = random_forest_classifier.predict_proba(X_test)

    wandb.sklearn.plot_classifier(random_forest_classifier, X_train, X_test, y_train, y_test, y_pred, proba, label, is_binary=True, model_name='Randomforest')


def autoML(data: pd.DataFrame):
    predictor = TabularPredictor(label="HeartDisease", eval_metric='roc_auc').fit(data)
    
    return predictor